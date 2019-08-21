# Copyright 2019 Yuhui
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

"""Common library for interacting with all of the APIs."""

import backoff
import requests

from singstat import timezone
from singstat.exceptions import APIError

def send_request(url, **kwargs):
    """Send a request to an endpoint.

    Arguments:
        url (str):
            The endpoint URL to send the request to.
        kwargs (dict):
            (optional) Attribute-value arguments to be passed as parameters
            to the endpoint URL.

    Returns:
        (object) Response JSON content of the request.
    """
    params = {}
    for attribute, value in kwargs.items():
        # remove empty parameters
        if value is None or value == '':
            pass
        else:
            params[attribute] = value

    headers = {
        'accept': 'application/json',
    }
    response = __send_request(url, params=params, headers=headers)

    response_json = response.json()
    response_content = __sanitise_timestamps(response_json)

    return response_content

# private

def __sanitise_timestamps(dictionary):
    """Convert timestamp strings to datetime objects and
    return the dictionary.
    """
    for key in dictionary:
        val = dictionary[key]
        if isinstance(val, str):
            try:
                dictionary[key] = timezone.datetime_from_string(val)
            except Exception:
                pass
        elif isinstance(val, dict):
            dictionary[key] = __sanitise_timestamps(val)
        elif isinstance(val, list):
            dictionary[key] = [
                __sanitise_timestamps(v) if isinstance(v, dict) else v \
                    for v in val
            ]

    return dictionary

@backoff.on_exception(backoff.expo, APIError, max_tries=2)
def __send_request(url, params=None, headers=None, error_callback=None):
    """Send a request to an endpoint.

    Arguments:
        url (str):
            The endpoint URL to send the request to.
        params (dict):
            (optional) Parameters to send with the URL.
        headers (dict:
            (optional) HTTP headers to send with the request.
        error_callback (function):
            (optional) Run this function when the API responds with an error.

    Returns:
        (Response) response of the request.

    Raises:
        AssertionException:
            Raised if response_type is specified but is not of an
            accepted value.
        APIError:
            Raised if the API responds with an error and
            there is no error_callback function.
    """
    response = requests.get(url, params=params, headers=headers)
    if response.status_code != requests.codes['ok']:
        response.raise_for_status()

    # handle errors in response
    response_json = response.json()
    if 'code' in response_json:
        response_code = int(response_json['code'])
        if response_code is not requests.codes['ok']:
            if error_callback is not None:
                error_callback(response_json)
            else:
                raise APIError(
                    response_json['message'],
                    response_json,
                )

    return response
