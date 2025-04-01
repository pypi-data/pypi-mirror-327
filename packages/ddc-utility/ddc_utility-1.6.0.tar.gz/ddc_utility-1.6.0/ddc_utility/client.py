import os
import json
import platform
import time

from importlib.metadata import version
from enum import Enum

import pandas as pd
import requests
import s3fs
import xarray as xr
from shapely.geometry.multipolygon import MultiPolygon
from shapely.geometry.polygon import Polygon
from pydantic import SecretStr

from ddc_utility.auth import OAuth2BearerHandler
from ddc_utility.constants import (DEFAULT_AOI_BUCKET, DEFAULT_DDC_BUCKET,
                                   DEFAULT_DDC_HOST)
from ddc_utility.cube import open_cube
from ddc_utility.errors import (BadRequest, DdcClientError, DdcException,
                                DdcRequestError, Forbidden, HTTPException,
                                NotFound, ServerError, TooManyRequests,
                                Unauthorized)
from ddc_utility.utils import Geometry, TimeRange, AccesToken
from ddc_utility.logger import log

try:
    package_version = version("ddc-utility")
except Exception:
    package_version = ""

class ReturnType(Enum):
    DICT = "dict"
    DATAFRAME = "dataframe"

output_data_type_map = {
    ReturnType.DATAFRAME: ReturnType.DATAFRAME,
    ReturnType.DICT: ReturnType.DICT,
    1: ReturnType.DATAFRAME,
    2: ReturnType.DICT
}

def authorize_request(method):
    def wrapper(self, *args, **kwargs):
        now = round(time.time())
        if self._auth is None or (self._auth.expires_at - now < 60):
            token = self.fetch_token()
            self._auth = OAuth2BearerHandler(
                token.access_token.get_secret_value(), token.expires_at)

        return method(self, *args, **kwargs)
    return wrapper


def authorize_s3_access(method):
    def wrapper(self, *args, **kwargs):
        now = round(time.time())

        if self._aws_s3 is None or (self._aws_session_exp - now < 60):
            temp_cred = self.fetch_temporary_credentials()
            self._aws_s3 = s3fs.S3FileSystem(
                key=temp_cred["AccessKeyId"],
                secret=temp_cred["SecretKey"],
                token=temp_cred["SessionToken"])
            self._aws_session_exp = temp_cred["expires_at"]

        return method(self, *args, **kwargs)
    return wrapper


class BaseClient:
    
    def __init__(
            self,
            client_id: str | None = None,
            client_secret: SecretStr | str | None = None,
            host: str | None = None,
            wait_on_rate_limit: bool = False
            ) -> None:

        if not isinstance(client_secret, SecretStr):
            client_secret = SecretStr(client_secret)

        self.client_id = client_id
        self.client_secret = client_secret
        self.host = host
        self.wait_on_rate_limit = wait_on_rate_limit

        self._auth = None
        self._session = requests.Session()
        self._user_agent = (
            f"Python/{platform.python_version()} "
            f"Requests/{requests.__version__} "
            f"ddc_cube/{package_version}"
        )

    def request(
        self,
        method: str,
        route: str,
        params: dict | None = None,
        data: dict | None = None,
        content_type: str | None = None,
        accept: str | None = None
        ) -> requests.Response:

        headers = {
            "User-Agent": self._user_agent,
            "client_id": self.client_id
        }
        if content_type is not None:
            headers["Content-Type"] = content_type
        if accept is not None:
            headers["Accept"] = accept

        url = self.host + route

        log.debug(
            f"\nMaking API request: {method} {url}\n"
            f"Parameters: {params}\n"
            f"Headers: {headers}"
        )

        with self._session.request(
                method, url, params=params, data=data, headers=headers, auth=self._auth) as response:

            log.debug(
                "\nReceived API response: "
                f"{response.status_code} {response.reason}\n"
                f"Headers: {response.headers}\n"
            )

            if response.status_code == 400:
                raise BadRequest(response)
            if response.status_code == 401:
                raise Unauthorized(response)
            if response.status_code == 403:
                raise Forbidden(response)
            if response.status_code == 404:
                raise NotFound(response)
            if response.status_code == 429:
                if self.wait_on_rate_limit:
                    reset_time = int(response.headers["x-rate-limit-reset"])
                    sleep_time = reset_time - int(time.time()) + 1
                    if sleep_time > 0:
                        log.warning(
                            "Rate limit exceeded. "
                            f"Sleeping for {sleep_time} seconds."
                        )
                        time.sleep(sleep_time)
                    return self.request(method, route, params, data, content_type, accept)
                else:
                    raise TooManyRequests(response)
            if response.status_code >= 500:
                raise ServerError(response)
            if not 200 <= response.status_code < 300:
                raise HTTPException(response)
            
            if b"Error" in response.content or b'error' in response.content:
                raise HTTPException(response)

            return response


class DdcClient(BaseClient):
    """DdcClient class for interacting with the DDC API.

    Attributes:
        client_id (str | None, optional): Danube Data Cube client id.
          If None, it will use DDC_CLIENT_ID env variable. Defaults to None.
        client_secret (str | None, optional): Danube Data Cube client secret.
          If None, it will use DDC_CLIENT_SECRET env variable. Defaults to None.
        host (str | None, optional): Alternative Danube Data Cube host url.
          If None, it will use DEFAULT_DDC_HOST constant. Defaults to None.

    Methods:
        get_all_aoi: Retrieve all AOIs for the user.
        get_aoi_by_id: Retrieve an AOI by its ID.
        create_aoi: Create a new AOI.
        get_data_layers: Get available data layers.
        get_data_selections: Get available data selections.
        get_crop_types: Get available crop types.
        create_crop_type: Create a new crop type.
        get_crop_variety: Get available crop varieties.
        create_crop_variety: Create a new crop variety.
        get_crop_models: Get available crop models.
        run_crop_model: Run a crop model simulation.
        get_growing_season: Get growing seasons for an AOI.
        create_growing_season: Create a growing season for an AOI.
        open_aoi_cube: Open an AOI cube as an xarray.Dataset.
        open_ddc_cube: Open a DDC dataset as an xarray.Dataset.
        fetch_token: Fetch an authentication token.
        fetch_temporary_credentials: Fetch temporary AWS credentials.
    """

    def __init__(
        self,
        client_id: str | None = None,
        client_secret: str | None = None,
        host: str | None = None
        ) -> None:

        """Initializes the DdcClient instance..

        Args:
            client_id (str | None, optional): Danube Data Cube client id.
              If None, it will use DDC_CLIENT_ID env variable. Defaults to None.
            client_secret (str | None, optional): Danube Data Cube client secret.
              If None, it will use DDC_CLIENT_SECRET env variable. Defaults to None.
            host (str | None, optional): Alternative Danube Data Cube host url.
              If None, it will use DEFAULT_DDC_HOST constant. Defaults to None.

        Raises:
            DdcException: If both `client_id` and `client_secret` are not provided.
        """
        client_id = client_id or os.environ.get('DDC_CLIENT_ID')
        client_secret = client_secret or os.environ.get('DDC_CLIENT_SECRET')
        host = host or DEFAULT_DDC_HOST

        if not client_id or not client_secret:
            raise DdcException(
                'both `client_id` and `client_secret` must be provided, '
                'consider setting environment variables '
                'DDC_CLIENT_ID and DDC_CLIENT_SECRET.'
            )

        self._aws_s3 = None
        self._aws_session_exp = 0
        
        super().__init__(client_id, client_secret, host, False)

    @authorize_request
    def get_all_aoi(
        self,
        with_geometry: bool = True,
        output_data_type: ReturnType | int = ReturnType.DATAFRAME,
        limit: int | None = None,
        offset: int | None = None
        ) -> pd.DataFrame | list[dict]:
        """Retrieve all areas of interests (AOI) for the user.

        Args:
            with_geometry (bool, optional): Indicates whether to include geometry data. Defaults to True.
            output_data_type (ReturnType | int, optional): Specifies the format of the returned data,
              either as a pandas.DataFrame (ReturnType.DATAFRAME) or a list of dictionaries (ReturnType.DICT).
              Defaults to ReturnType.DATAFRAME.
            limit (int | None, optional): Maximum number of records to retrieve. Defaults to None.
            offset (int | None, optional): Number of records to skip before starting to collect the result set.
              Defaults to None.

        Returns:
            pd.DataFrame | list[dict]: AOIs information.
            
        Raises:
            DdcRequestError: If an error occurs during the request process.
        """
        route = "/aoi_manager/get_aoi"
        accept = "application/json"
        params = {'user_id': self.client_id,
                  'with_geometry': with_geometry,
                  'limit': limit,
                  'offset': offset}

        try:
            response = self.request(
                "GET", route, params=params, accept=accept)

        except HTTPException as error:
            raise DdcRequestError(
                f"Couldn't get AOIs with HTTP exception: {error}"
            ) from None
        
        return self._process_response_json(response, output_data_type_map.get(output_data_type, ReturnType.DATAFRAME))

    @authorize_request
    def get_aoi_by_id(
        self,
        aoi_id: int,
        output_data_type: ReturnType | int = ReturnType.DATAFRAME
        ) -> pd.DataFrame | list[dict]:
        """Retrieve an areas of interests (AOI) for the user by ID.

        Args:
            aoi_id (int): ID of the AOI.
            output_data_type (ReturnType | int, optional): Specifies the format of the returned data,
              either as a pandas.DataFrame (ReturnType.DATAFRAME) or a list of dictionaries (ReturnType.DICT).
              Defaults to ReturnType.DATAFRAME.

        Returns:
            pd.DataFrame | list[dict]: AOI information.

        Raises:
            DdcRequestError: If an error occurs during the request process.
        """
        route = "/aoi_manager/get_aoi"
        accept = "application/json"
        params = {'user_id': self.client_id,
                  'aoi_id': aoi_id}

        try:
            response = self.request(
                "GET", route, params=params, accept=accept)

        except HTTPException as error:
            raise DdcRequestError(
                "Couldn't get AOI with id {aoi_id} with HTTP exception: {error}"
            ) from None
        
        return self._process_response_json(response, output_data_type_map.get(output_data_type, ReturnType.DATAFRAME))

    @authorize_request
    def create_aoi(
        self,
        name: str,
        geometry: Geometry | Polygon | MultiPolygon | str,
        time_range: TimeRange | tuple[pd.Timestamp, pd.Timestamp] | tuple[str, str],
        layer_selection_id:  int | None = None,
        layer_ids: list[int] | None = None,
        is_dynamic: bool = False,
        output_data_type: ReturnType | int = ReturnType.DATAFRAME
        ) -> pd.DataFrame | list[dict]:
        """Create an area of interests (AOI).

        Args:
            name (str): The name of the area of interest.
            geometry (Geometry | Polygon | MultiPolygon | str): The geometry of the area of interest in WGS84 
              coordinate system. This can be provided as a `ddc_utility.Geometry` object, a `shapely.Polygon`, a `shapely.MultiPolygon`, or as a WKT string.
            time_range (TimeRange | tuple[pd.Timestamp, pd.Timestamp] | tuple[str, str]):
              The time range for which the area of interest is defined.
              This can be provided as a `ddc_utility.TimeRange` object, a tuple of two `pandas.Timestamp` objects,
              or a tuple of two strings representing dates.
            layer_selection_id (int | None, optional): Layer selection ID. If both,  
              layer_selection_id and layer_ids are provided, only layer_selection_id will be use. Defaults to None.
            layer_ids (list[int] | None, optional): List of layer IDs. If both, layer_selection_id and layer_ids are 
              provided, only layer_selection_id will be use. Defaults to None.
            is_dynamic (bool, optional): Whether the AOI is dynamic (True) or static (False).
                Defaults to False.
            output_data_type (ReturnType | int, optional): Specifies the format of the returned data,
              either as a pandas.DataFrame (ReturnType.DATAFRAME) or a list of dictionaries (ReturnType.DICT).
              Defaults to ReturnType.DATAFRAME.

        Returns:
            pd.DataFrame | list[dict]: Created AOI information.

        Raises:
            DdcRequestError: If an error occurs during the request process.

        """
        if not isinstance(time_range, TimeRange):
            time_range = TimeRange(*time_range)
        time_range_str = time_range.to_string(only_date=True)

        if not isinstance(geometry, Geometry):
            geometry = Geometry(geometry)
        geometry_str = geometry.to_string()

        if layer_ids:
            layer_ids_str = ','.join(str(x) for x in layer_ids)

        route = "/aoi_manager/create_aoi"
        accept = "application/json"
        content_type = "application/json"
        data = {
            "user_id": self.client_id,
            "name": name,
            "geometry": geometry_str,
            "start_date": time_range_str[0],
            "end_date": time_range_str[1],
            "is_dynamic": is_dynamic
        }
        if layer_selection_id:
            data["layer_selection_id"] = layer_selection_id
        else:
            data["layer_ids"] = layer_ids_str
        data = json.dumps(data)
        
        try:
            response = self.request(
                "POST", route, data=data, content_type=content_type, accept=accept)

        except HTTPException as error:
            raise DdcRequestError(
                f"Couldn't create AOI with HTTP exception: {error}"
            ) from None

        return self._process_response_json(response, output_data_type_map.get(output_data_type, ReturnType.DATAFRAME))

    @authorize_request
    def get_data_layers(
        self,
        output_data_type: ReturnType | int = ReturnType.DATAFRAME
        ) -> pd.DataFrame | list[dict]:
        """Retrieve available data layers.

        Args:
            output_data_type (ReturnType | int, optional): Specifies the format of the returned data,
              either as a pandas.DataFrame (ReturnType.DATAFRAME) or a list of dictionaries (ReturnType.DICT).
              Defaults to ReturnType.DATAFRAME.

        Returns:
            pd.DataFrame | list[dict]: Available data layers information.

        Raises:
            DdcRequestError: If an error occurs during the request process.
        """

        params = {'user_id': self.client_id}

        route = "/aoi_manager/data_layers"
        accept = "application/json"

        try:
            response = self.request(
                "GET", route, params=params, accept=accept)

        except HTTPException as error:
            raise DdcRequestError(
                f"Couldn't get data layers with HTTP exception: {error}"
            ) from None

        return self._process_response_json(response, output_data_type_map.get(output_data_type, ReturnType.DATAFRAME))

    @authorize_request
    def get_data_selections(
        self,
        output_data_type: ReturnType | int = ReturnType.DATAFRAME
        ) -> pd.DataFrame | list[dict]:
        """Retrieve available data selections.

        Args:
            output_data_type (ReturnType | int, optional): Specifies the format of the returned data,
              either as a pandas.DataFrame (ReturnType.DATAFRAME) or a list of dictionaries (ReturnType.DICT).
              Defaults to ReturnType.DATAFRAME.

        Returns:
            pd.DataFrame | list[dict]: Available data selections information.

        Raises:
            DdcRequestError: If an error occurs during the request process.
        """

        params = {'user_id': self.client_id}

        route = "/aoi_manager/data_selections"
        accept = "application/json"

        try:
            response = self.request(
                "GET", route, params=params, accept=accept)

        except HTTPException as error:
            raise DdcRequestError(
                f"Couldn't get data selections with HTTP exception: {error}"
            ) from None

        return self._process_response_json(response, output_data_type_map.get(output_data_type, ReturnType.DATAFRAME))
    
    @authorize_request
    def get_crop_types(
        self,
        output_data_type: ReturnType | int = ReturnType.DATAFRAME
        ) -> pd.DataFrame | list[dict]:
        """Retrieve available crop types.

        Args:
            output_data_type (ReturnType | int, optional): Specifies the format of the returned data,
              either as a pandas.DataFrame (ReturnType.DATAFRAME) or a list of dictionaries (ReturnType.DICT).
              Defaults to ReturnType.DATAFRAME.

        Returns:
            pd.DataFrame | list[dict]: Available crop types information.

        Raises:
            DdcRequestError: If an error occurs during the request process.
        """

        params = {'user_id': self.client_id}

        route = "/crop/get_type"
        accept = "application/json"

        try:
            response = self.request(
                "GET", route, params=params, accept=accept)

        except HTTPException as error:
            raise DdcRequestError(
                f"Couldn't get crop types with HTTP exception: {error}"
            ) from None

        return self._process_response_json(response, output_data_type_map.get(output_data_type, ReturnType.DATAFRAME))

    @authorize_request
    def create_crop_type(
        self,
        crop_type_name: str,
        output_data_type: ReturnType | int = ReturnType.DATAFRAME
        ) -> pd.DataFrame | list[dict]:
        """Create crop type.

        Args:
            crop_type_name (str): Name of the crop type.
            output_data_type (ReturnType | int, optional): Specifies the format of the returned data,
              either as a pandas.DataFrame (ReturnType.DATAFRAME) or a list of dictionaries (ReturnType.DICT).
              Defaults to ReturnType.DATAFRAME.

        Returns:
             pd.DataFrame | list[dict]: Created crop type information.

        Raises:
            DdcRequestError: If an error occurs during the request process.
        """
        route = "/crop/create_type"
        accept = "application/json"
        content_type = "application/json"
        data = {
            "user_id": self.client_id,
            "crop_type_name": crop_type_name
        }
        data = json.dumps(data)

        try:
            response = self.request(
                "POST", route, data=data, content_type=content_type, accept=accept)

        except HTTPException as error:
            raise DdcRequestError(
                f"Couldn't create crop type with HTTP exception: {error}"
            ) from None

        return self._process_response_json(response, output_data_type_map.get(output_data_type, ReturnType.DATAFRAME))

    @authorize_request
    def get_crop_variety(
        self,
        crop_type_id: int,
        output_data_type: ReturnType | int = ReturnType.DATAFRAME
        ) -> pd.DataFrame | list[dict]:
        """Retrieve available crop varieties.

        Args:
            crop_type_id (int): ID of crop type.
            output_data_type (ReturnType | int, optional): Specifies the format of the returned data,
              either as a pandas.DataFrame (ReturnType.DATAFRAME) or a list of dictionaries (ReturnType.DICT).
              Defaults to ReturnType.DATAFRAME.

        Returns:
            pd.DataFrame | list[dict]: Available crop variety information.

        Raises:
            DdcRequestError: If an error occurs during the request process.
        """

        params = {'user_id': self.client_id,
                  'crop_type_id': crop_type_id}

        route = "/crop/get_variety"
        accept = "application/json"

        try:
            response = self.request(
                "GET", route, params=params, accept=accept)

        except HTTPException as error:
            raise DdcRequestError(
                f"Couldn't get crop varieties with crop type id {crop_type_id} with HTTP exception: {error}"
            ) from None

        return self._process_response_json(response, output_data_type_map.get(output_data_type, ReturnType.DATAFRAME))

    @authorize_request
    def create_crop_variety(
        self,
        crop_type_id: id,
        crop_variety_name: str,
        output_data_type: ReturnType | int = ReturnType.DATAFRAME
        ) -> pd.DataFrame | list[dict]:
        """Create crop variety for a given crop type.

        Args:
            crop_type_id (id): ID of crop type.
            crop_variety_name (str): Name of the crop variety.
            output_data_type (ReturnType | int, optional): Specifies the format of the returned data,
              either as a pandas.DataFrame (ReturnType.DATAFRAME) or a list of dictionaries (ReturnType.DICT).
              Defaults to ReturnType.DATAFRAME.

        Returns:
            pd.DataFrame | list[dict]: Created crop variety information.

        Raises:
            DdcRequestError: If an error occurs during the request process.

        """
        route = "/crop/create_variety"
        accept = "application/json"
        content_type = "application/json"
        data = {
            "user_id": self.client_id,
            "crop_type_id": crop_type_id,
            "crop_variety_name": crop_variety_name
        }
        data = json.dumps(data)

        try:
            response = self.request(
                "POST", route, data=data, content_type=content_type, accept=accept)

        except HTTPException as error:
            raise DdcRequestError(
                f"Couldn't create crop variety with HTTP exception: {error}"
            ) from None

        return self._process_response_json(response, output_data_type_map.get(output_data_type, ReturnType.DATAFRAME))

    @authorize_request
    def get_crop_models(
        self,
        crop_type_id: int,
        output_data_type: ReturnType | int = ReturnType.DATAFRAME
        ) -> pd.DataFrame | list[dict]:
        """Retrieve available crop model list.

        Args:
            crop_type_id (int): ID of crop type.
            output_data_type (ReturnType | int, optional): Specifies the format of the returned data,
              either as a pandas.DataFrame (ReturnType.DATAFRAME) or a list of dictionaries (ReturnType.DICT).
              Defaults to ReturnType.DATAFRAME.

        Returns:
            pd.DataFrame | list[dict]: Available crop models information.

        Raises:
            DdcRequestError: If an error occurs during the request process.
        """

        params = {'user_id': self.client_id,
                  'crop_type_id': crop_type_id}

        route = "/crop/get_model"
        accept = "application/json"

        try:
            response = self.request(
                "GET", route, params=params, accept=accept)

        except HTTPException as error:
            raise DdcRequestError(
                f"Couldn't get crop models with crop type id {crop_type_id} with HTTP exception: {error}"
            ) from None

        return self._process_response_json(response, output_data_type_map.get(output_data_type, ReturnType.DATAFRAME))

    @authorize_request
    def run_crop_model(
        self,
        aoi_id: int,
        time_range: TimeRange | tuple[pd.Timestamp, pd.Timestamp] | tuple[str, str],
        sowing_date: pd.Timestamp | str,
        crop_model_name: str,
        init_water_content: float | None = None,
        growing_season_id: int | None = None,
        seasonal_trajectory: bool = False,
        soil_type: str | None = None,
        irrigation: str | None = None,
        output_data_type: ReturnType | int = ReturnType.DATAFRAME
        ) -> pd.DataFrame | list[dict]:
        """
        Run crop model.

        Args:
            aoi_id (int): ID of the AOI.
            time_range (TimeRange | tuple[pd.Timestamp, pd.Timestamp] | tuple[str, str]): Time range for the simulation.
              This can be provided as a `ddc_utility.TimeRange` object, a tuple of two `pandas.Timestamp` objects,
              or a tuple of two strings representing dates.
            sowing_date (pd.Timestamp | str): Sowing date for the simulation.
            crop_model_name (str): Name of the crop model.
            init_water_content (float | None, optional): Initial water content for the simulation.
            growing_season_id (int | None, optional): ID of the growing season.
            seasonal_trajectory (bool, optional): Flag for utilization of CLMS PPI ST in the modelling process
            soil_type (str | None, optional): USDA soil type definition  
            irrigation (str | None, optional): Irrigation schedule for the simulation in [(date, value), ... ,(date, 
              value)] format, expected as a formatted string. Dates are expecetd to be in YYYY-mm-dd format. Values are in mm. 
            output_data_type (ReturnType | int, optional): Specifies the format of the returned data,
              either as a pandas.DataFrame (ReturnType.DATAFRAME) or a list of dictionaries (ReturnType.DICT).
              Defaults to ReturnType.DATAFRAME.

        Returns:
            pd.DataFrame | list[dict]: Crop model run information.

        Raises:
            DdcRequestError: If an error occurs during the request process.
        """

        if not isinstance(time_range, TimeRange):
            time_range = TimeRange(*time_range)
        time_range_str = time_range.to_string(only_date=True)

        if not isinstance(sowing_date, pd.Timestamp):
            sowing_date = pd.Timestamp(sowing_date)
        sowing_date_str = sowing_date.isoformat(sep='T').split('T')[0]

        route = "/crop_model/run"
        accept = "application/json"
        params = {
            "user_id": self.client_id,
            "aoi_id": aoi_id,
            "start_date": time_range_str[0],
            "end_date": time_range_str[1],
            "sowing_date": sowing_date_str,
            "crop_model_name": crop_model_name,
            "seasonal_trajectory": seasonal_trajectory,
            "growing_season_id": growing_season_id,
            "init_water_content": init_water_content,
            "soil_type": soil_type,
            "irrigation": irrigation
        }

        try:
            response = self.request(
                "GET", route, params=params, accept=accept)

        except HTTPException as error:
            raise DdcRequestError(
                f"Couldn't run crop model with HTTP exception: {error}"
            ) from None

        return self._process_response_json(response, output_data_type_map.get(output_data_type, ReturnType.DATAFRAME))

    @authorize_request
    def get_growing_season(
        self,
        aoi_id: int,
        output_data_type: ReturnType | int = ReturnType.DATAFRAME
        ) -> pd.DataFrame | list[dict]:
        """Retrieve growing seasons for AOI.

        Args:
            aoi_id (int): ID of the AOI.
            output_data_type (ReturnType | int, optional): Specifies the format of the returned data,
              either as a pandas.DataFrame (ReturnType.DATAFRAME) or a list of dictionaries (ReturnType.DICT).
              Defaults to ReturnType.DATAFRAME.

        Returns:
            pd.DataFrame | list[dict]: Growing season information.

        Raises:
            DdcRequestError: If an error occurs during the request process.
        """

        route = "/growing_season/get_season"
        accept = "application/json"
        params = {'user_id': self.client_id,
                  'aoi_id': aoi_id}


        try:
            response = self.request(
                "GET", route, params=params, accept=accept)

        except HTTPException as error:
            raise DdcRequestError(
                f"Couldn't get growing season for AOI with id {aoi_id} with HTTP exception: {error}"
            ) from None

        return self._process_response_json(response, output_data_type_map.get(output_data_type, ReturnType.DATAFRAME))

    @authorize_request
    def create_growing_season(
        self,
        aoi_id: int,
        time_range: TimeRange | tuple[pd.Timestamp, pd.Timestamp] | tuple[str, str],
        sowing_date: pd.Timestamp | str,
        crop_type_id: int,
        crop_variety_id: int,
        crop_model_id: int,
        output_data_type: ReturnType | int = ReturnType.DATAFRAME
        ) -> pd.DataFrame | list[dict]:
        """Create growing season for AOI.

        Args:
            aoi_id (int): ID of the AOI.
            time_range (TimeRange | tuple[pd.Timestamp, pd.Timestamp] | tuple[str, str]):
                The time range for which the growing season is defined.
                This can be provided as a `ddc_utility.TimeRange` object, a tuple of two `pandas.Timestamp` objects,
                or a tuple of two strings representing dates.
            sowing_date (pd.Timestamp | str): The date when the crop is sown.
            crop_type_id (int): ID of crop type.
            crop_variety_id (int): ID of crop variety.
            crop_model_id (int): ID of crop model.
            output_data_type (ReturnType | int, optional): Specifies the format of the returned data,
              either as a pandas.DataFrame (ReturnType.DATAFRAME) or a list of dictionaries (ReturnType.DICT).
              Defaults to ReturnType.DATAFRAME.

        Returns:
            pd.DataFrame | list[dict]: Created growing season information.

        Raises:
            DdcRequestError: If an error occurs during the request process.

        """

        if not isinstance(time_range, TimeRange):
            time_range = TimeRange(*time_range)
        time_range_str = time_range.to_string(only_date=True)

        if not isinstance(sowing_date, pd.Timestamp):
            sowing_date = pd.Timestamp(sowing_date)
        sowing_date_str = sowing_date.isoformat(sep='T').split('T')[0]

        route = "/growing_season/create_season"
        accept = "application/json"
        content_type = "application/json"
        data = {
            "user_id": self.client_id,
            "aoi_id": aoi_id,
            "start_date": time_range_str[0],
            "end_date": time_range_str[1],
            "sowing_date": sowing_date_str,
            "crop_type_id": crop_type_id,
            "crop_variety_id": crop_variety_id,
            "crop_model_id": crop_model_id
        }
        data = json.dumps(data)

        try:
            response = self.request(
                "POST", route, data=data, content_type=content_type, accept=accept)

        except HTTPException as error:
            raise DdcRequestError(
                f"Couldn't create growing season with HTTP exception: {error}"
            ) from None

        return self._process_response_json(response, output_data_type_map.get(output_data_type, ReturnType.DATAFRAME))

    @authorize_s3_access
    def open_aoi_cube(
        self,
        aoi_id: int,
        bucket_name: str = DEFAULT_AOI_BUCKET,
        group: str | None = None
        ) -> xr.Dataset:
        """Open AOI cube as an xarray.Dataset.

        Args:
            aoi_id (int): ID of the AOI.
            bucket_name (str, optional): Name of the S3 bucket where the zarr cube is stored.
                Defaults to `DEFAULT_AOI_BUCKET`.
            group (str, optional): Zarr group of the dataset. Defaults to None.

        Returns:
            xr.Dataset: AOI dataset.

        Raises:
            DdcClientError: If user don't have access to the bucket.
            DdcRequestError: If an error occurs during opening the cube.

        """

        zarr_path = f"s3://{bucket_name}/{aoi_id}_{self.client_id}.zarr"

        try:
            cube = open_cube(path=zarr_path, fs=self._aws_s3, group=group)
        except PermissionError as error:
            raise DdcClientError(
                f"User don't have access for this operation: {error}") from None
        except FileNotFoundError as error:
            raise DdcRequestError(
                f"Invalid aoi_id, no such aoi cube: {error}") from None
        except Exception as error:
            raise DdcRequestError(
                f"Couldn't open AOI dataset with id {aoi_id} with HTTP exception: {error}"
            ) from None
        return cube

    @authorize_s3_access
    def open_ddc_cube(
        self,
        zarr_path: str,
        zarr_group: str | None = None,
        bucket_name: str = DEFAULT_DDC_BUCKET
        ) -> xr.Dataset:
        """Open DDC dataset as an xarray.Dataset.

        Args:
            zarr_path (str): Zarr path to the dataset.
            zarr_group (str, optional): Zarr group of the dataset.
            bucket_name (str, optional): Name of the S3 bucket where the zarr cube is stored.
                Defaults to `DEFAULT_DDC_BUCKET`.

        Returns:
            xr.Dataset: DDC dataset.

        Raises:
            DdcClientError: If user don't have access to the bucket.
            DdcRequestError: If an error occurs during opening the cube.
        """

        zarr_path = f"s3://{bucket_name}/{zarr_path}"

        try:
            cube = open_cube(path=zarr_path,
                             fs=self._aws_s3,
                             group=zarr_group)
        except PermissionError as error:
            raise DdcClientError(
                f"User don't have access for this operation: {error}") from None
        except Exception as error:
            raise DdcRequestError(
                f"Couldn't open DDC dataset with HTTP exception: {error}"
            ) from None
        return cube

    
    def _process_response_json(self, response: requests.Response, output_data_type: ReturnType):
        
        data = response.json()

        if output_data_type == ReturnType.DATAFRAME:
            if isinstance(data, list):
                return pd.DataFrame(data)
            if isinstance(data, dict):
                return pd.DataFrame([data])
            else:
                raise ValueError(
                    f"Can't post-process API response -- {type(data)} is invalid with output_data_type of {output_data_type}")
        else:
            return data
    
    def fetch_token(self) -> AccesToken:
        """Fetch token from a remote token endpoint."""
    
        def custom_serializer(obj):
            if isinstance(obj, SecretStr):
                return obj.get_secret_value()  # Convert datetime to string
            raise TypeError(f"Type {type(obj)} not serializable")
        
        route = "/get_token"
        accept = "application/json"
        content_type = "application/json"
        data = {
            "client_id": self.client_id,
            "client_secret": self.client_secret
        }
        
        data = json.dumps(data, default=custom_serializer)

        try:
            response = self.request(
                "POST", route, data=data, content_type=content_type, accept=accept)
        except HTTPException as error:
            raise DdcRequestError(f"Couldn't fetch token with HTTP exception: {error}") from None

        result = response.json()
        token = AccesToken(**result)

        return token

    @authorize_request
    def fetch_temporary_credentials(self) -> dict:
        """Fetch token from a remote token endpoint."""

        route = "/get_temp_cred"
        accept = "application/json"
        params = {'user_id': self.client_id}

        try:
            response = self.request(
                "GET", route, params=params, accept=accept)

        except HTTPException as error:
            raise DdcRequestError(
                f"Couldn't fetch temporary credentials with HTTP exception: {error}"
            ) from None

        result = response.json()
        credentials = result["Credentials"]

        credentials["expires_at"] = int(time.mktime(time.strptime(
            credentials.pop("Expiration"), "%Y-%m-%dT%H:%M:%SZ")))

        return credentials
