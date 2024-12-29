# Copyright 2019-2024 Yuhui
#
# Licensed under the GNU General Public License, Version 3.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.gnu.org/licenses/gpl-3.0.html
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Client mixin for interacting with all of the API endpoints."""

from typing import Any, Optional

from requests import codes as requests_codes
from requests.adapters import HTTPAdapter, Retry
from requests_cache import BaseCache, CachedSession
from typeguard import check_type, typechecked

from .constants import (
    CACHE_NAME,
    CACHE_TWELVE_HOURS,
    DATA_KEYS_TO_SANITISE,
    USER_AGENT,
)
from .exceptions import APIError
from .timezone import datetime_from_string
from .types import Url

class SingStat:
    """Common library for other API Clients.

    Normally, it does not need to be created by applications. But \
        applications may use the public methods provided here.

    The constructor sets the following:

    - Connection retries using exponential backoff. \
        (Reference: https://stackoverflow.com/a/35504626.)
    - Cache to expire after 12 hours.
    - User-agent header.

    :param cache_backend: Cache backend name or instance to use. Refer to \
        https://requests-cache.readthedocs.io/en/stable/user_guide/backends.html \
        for more information and allowed values. Defaults to "sqlite".
    :type cache_backend: str | BaseCache

    :param is_test_api: Whether to use SingStat's test API. If this is set to \
        True, then ``isTestApi=true`` is added to the parameters when calling \
        ``send_request()``. Defaults to False.
    :type is_test_api: bool
    """

    is_test_api: bool

    @typechecked
    def __init__(
        self,
        cache_backend: str | BaseCache='sqlite',
        is_test_api: bool=False,
    ) -> None:
        """Constructor method"""
        self.is_test_api = is_test_api

        retries = Retry(
            total=5,
            backoff_factor=0.1,
            status_forcelist=[500, 502, 503, 504]
        )

        expire_after = CACHE_TWELVE_HOURS
        self.session = CachedSession(
            CACHE_NAME,
            backend=cache_backend,
            expire_after=expire_after,
            stale_if_error=False,
        )
        self.session.mount('https://', HTTPAdapter(max_retries=retries))
        self.session.headers.update({
            'Accept': 'application/json',
            'User-Agent': USER_AGENT,
        })

    @typechecked
    def __repr__(self) -> str:
        """String representation"""
        return f'{self.__class__}'

    @typechecked
    def build_params(
        self,
        params_expected_type: Any,
        original_params: dict,
        default_params: dict | None=None,
    ) -> dict:
        """Build the list of parameters that are compatible for use with the \
            endpoint URLs, e.g. camelCase parameter names instead of Python's \
            snake_case.

        :param params_expected_type: The expected type of \
            ``original_params``. Should be one of the importable types from \
            ``singstat.types_args``.
        :type params_expected_type: Any

        :param original_params: The set of parameters to use for building.
        :type original_params: dict

        :param default_params: The set of parameters' default values. Should \
            be of the same type as what is specified in \
            ``params_expected_type``. Defaults to None.
        :type default_params: dict or None

        :return: The set of parameters that can be used with the API endpoints.
        :rtype: dict
        """
        if default_params is None:
            default_params = {}
        joined_params = default_params | original_params

        # Ensure that the parameters match the expected input parameter types.
        _ = check_type(joined_params, params_expected_type)

        params: dict = {}
        for key, value in joined_params.items():
            # Convert the snake_case key to camelCase param
            # because that is what the endpoints require.
            # Ref: https://www.geeksforgeeks.org/python-convert-snake-case-string-to-camel-case/
            words = key.split('_')
            param = words[0] + ''.join(word.title() for word in words[1:])

            params[param] = value

        return params

    @typechecked
    def sanitise_data(
        self,
        value: Any,
        iterate: bool=True,
    ) -> Any:
        """Convert the following:

        - String that is like date or datetime: convert to ``datetime.date`` \
            or ``datetime.datetime`` object respectively.
        - String value of specific ``dict`` keys: convert to integer or \
            2-value tuple. The ``dict`` keys are: "between", \
            "dataLastUpdated", "dateGenerated", "limit", "offset", "rowNo", \
            "total"

        :param value: Value to sanitise.
        :type value: Any

        :param iterate: If true, then ``list`` and ``dict`` objects are \
            sanitised recursively. Defaults to True.
        :type iterate: bool

        :return: The sanitised value.
        :rtype: Any
        """
        sanitised_value: Any = value

        if iterate and isinstance(value, list):
            sanitised_value = [
                self.sanitise_data(v, iterate=iterate) \
                    if isinstance(v, (list, dict)) else v
                    for v in value
            ]
        elif iterate and isinstance(value, dict):
            sanitised_value = {}
            for k, v in value.items():
                if k in DATA_KEYS_TO_SANITISE or isinstance(v, (dict, list)):
                    sanitised_value[k] = self.sanitise_data(v, iterate=iterate)
                else:
                    sanitised_value[k] = v
        elif isinstance(value, str):
            try:
                # pylint: disable=broad-exception-caught

                # Convert to a date/datetime.
                sanitised_value = datetime_from_string(value)
            except Exception:
                try:
                    # Convert to an integer
                    sanitised_value = int(value)
                except Exception:
                    try:
                        # Convert to tuple with 2 integer values.
                        split_value = value.split(',')
                        if len(split_value) == 2:
                            tuple_value = tuple(
                                self.sanitise_data(v.strip(), iterate=False) \
                                    for v in split_value
                            )
                            if all((isinstance(v, int) for v in tuple_value)):
                                sanitised_value = tuple_value
                    except Exception:
                        pass

        return sanitised_value

    @typechecked
    def send_request(
        self,
        url: Url,
        params: Optional[dict]=None,
        sanitise: bool=True,
    ) -> Any:
        """Send a request to an endpoint.

        Normally, this method does not need to be called directly. However, \
            if SingStat were to change their API specification but this \
            package has not yet been updated to support that change, then \
            applications may use this method to call the changed endpoints.

        If the client had been instantiated with ``is_test_api=True``, then \
            ``isTestApi=true`` is added to the list of parameters to send to \
            the endpoint.

        :param url: The endpoint URL to send the request to.
        :type url: Url

        :param params: List of parameters to be passed to the endpoint URL. \
            Parameter names **must** match the names required by the \
            endpoints, particularly with typecase (e.g. camelCase). Defaults \
            to None.
        :type params: dict

        :param sanitise: If true, then the response's values are sanitised \
            using the ``sanitise_data()`` method. Defaults to True.
        :type iterate: bool

        :raises APIError: "No data records returned" when count of data is 0.
        :raises HTTPError: Error occurred during the request process.

        :return: Response JSON content of the request.
        :rtype: Any
        """
        data: Any

        if params is None:
            params = {}

        # Add ``isTestApi`` parameter, if necessary.
        if self.is_test_api:
            params['isTestApi'] = 'true'

        response = self.session.get(url, params=params)
        if response.status_code != requests_codes['ok']:
            response.raise_for_status()

        response_json = {}
        try:
            response_json = response.json()
        except ValueError:
            pass

        data = self.sanitise_data(response_json) if sanitise else response_json

        data_count = response_json['DataCount'] \
            if 'DataCount' in response_json else 0
        if data_count == 0:
            raise APIError('No data records returned', data=response_json)

        return data

__all__ = [
    'SingStat',
]
