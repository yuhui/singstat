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

# pylint: disable=invalid-name,missing-function-docstring,redefined-outer-name,unused-argument

"""Test that the net functions are working properly."""

from datetime import date

import pytest
from requests import HTTPError
from requests_cache import CachedSession
from typeguard import TypeCheckError

from singstat.exceptions import APIError
from singstat.singstat import SingStat

from tests.mocks.api_response_zero_data import APIResponseZeroData
from tests.mocks.types_args import MockArgsDict

# constants for testing date as date object
GOOD_DATE = date(2019, 7, 13)

# constants for testing date as string object
BAD_DATE = '2019-07-13'

SANITISE_DATA_DICT = {
    'between': '13,57,99',
    'limit': '123',
    'offset': '456',
    'total': '789.3',
    'value_str': 'foo bar',
    'value_int': '42',
    'value_bool': 'True',
    'value_date': '1/7/2019',
    'value_list': [1, '2', {
        'between': 'foo,77',
        'dataLastUpdated': '12/3/2021',
    }],
    'value_dict': {
        'key1': '316',
        'between': '45, 89',
        'dateGenerated': '2024-12-01',
    },
}

@pytest.fixture
def mock_requests_zero_data_response(monkeypatch):
    """Requests.get() mocked to return sample API response with value without data."""

    def mock_requests_get(*args, **kwargs):
        return APIResponseZeroData()

    monkeypatch.setattr(CachedSession, 'get', mock_requests_get)

@pytest.fixture(scope='module')
def client():
    return SingStat(is_test_api=True)

@pytest.fixture(scope='module')
def client_not_test():
    return SingStat()

def test_repr(client_not_test):
    assert repr(client_not_test) == str(client_not_test.__class__)

@pytest.mark.parametrize(
    ('original_params', 'default_params', 'expected_params'),
    [
        (
            {'foobar': 'foo bar'},
            {'meaning_of_universe': 42},
            {'foobar': 'foo bar', 'meaningOfUniverse': 42},
        ),
        (
            {'foobar': 'foo bar'},
            None,
            {'foobar': 'foo bar'},
        ),
    ],
)
def test_build_params(
    client,
    original_params,
    default_params,
    expected_params,
):
    params = client.build_params(MockArgsDict, original_params, default_params)
    assert params == expected_params

@pytest.mark.parametrize(
    ('original_params', 'default_params'),
    [
        (
            {'foobar': 'foo bar'},
            {'meaning_of_universe': '42'},
        ),
        (
            {'foo': 'foo'},
            None,
        ),
    ],
)
def test_build_params_with_bad_inputs(client, original_params, default_params):
    with pytest.raises(TypeCheckError):
        _ = client.build_params(MockArgsDict, original_params, default_params)

@pytest.mark.parametrize(
    ('kwargs', 'expected_result'),
    [
        (
            {},
            {
                'between': '13,57,99',
                'limit': 123,
                'offset': 456,
                'total': '789.3',
                'value_str': 'foo bar',
                'value_int': '42',
                'value_bool': 'True',
                'value_date': '1/7/2019',
                'value_list': [1, '2', {
                    'between': 'foo,77',
                    'dataLastUpdated': date(2021, 3, 12),
                }],
                'value_dict': {
                    'key1': '316',
                    'between': (45, 89),
                    'dateGenerated': date(2024, 12, 1),
                },
            },
        ),
        (
            {'iterate': False},
            SANITISE_DATA_DICT,
        ),
    ],
)
def test_sanitise_data(
    client,
    kwargs,
    expected_result,
):
    result = client.sanitise_data(value=SANITISE_DATA_DICT, **kwargs)
    assert result == expected_result

@pytest.mark.parametrize(
    ('url', 'params'),
    [
        (
            'https://tablebuilder.singstat.gov.sg/api/table/resourceId',
            {'keyword': 'house', 'searchOption': 'title'},
        ),
        (
            'https://tablebuilder.singstat.gov.sg/api/table/metadata/M212151',
            {},
        ),
        (
            'https://tablebuilder.singstat.gov.sg/api/table/tabledata/M212151',
            {},
        ),
        (
            'https://tablebuilder.singstat.gov.sg/api/table/tabledata/D10022',
            {},
        ),
    ],
)
def test_send_request(client, url, params):
    data = client.send_request(url, params)
    assert isinstance(data, dict)

def test_send_request_with_invalid_endpoint(client):
    with pytest.raises(HTTPError):
        _ = client.send_request(
            'https://tablebuilder.singstat.gov.sg/api/table/',
        )

def test_send_request_with_zero_data_value(
    client_not_test,
    mock_requests_zero_data_response,
):
    with pytest.raises(APIError) as excinfo:
        _ = client_not_test.send_request(
            'https://tablebuilder.singstat.gov.sg/api/table/tabledata/M212151'
        )

    assert excinfo.value.message == 'No data records returned'
