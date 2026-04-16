# Copyright 2019-2026 Yuhui. All rights reserved.
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

"""Test that the SingStat class is working properly."""

from datetime import date, datetime
from unittest.mock import Mock
from zoneinfo import ZoneInfo

import pytest
from requests import HTTPError
from requests_cache import CachedSession

from singstat.constants import USER_AGENT
from singstat.exceptions import APIError
from singstat.singstat import SingStat

from tests.mocks.api_response_bad_request import APIResponseBadRequest
from tests.mocks.api_response_singstat import APIResponseSendRequest
from tests.mocks.api_response_zero_data import APIResponseZeroData
from tests.mocks.types_args import MockArgsDict

SANITISE_DATA_DICT = {
    'value_str': 'foo bar',
    'value_ignore': '37',
    'value_int': 42,
    'value_bool': True,
    'value_date': '1/7/2019',
    'value_blank': '',
    'value_list': [1, '2', {
        'key1': '205',
        'date_time': '2024-12-01T09:57:45+08:00',
    }],
    'value_dict': {
        'key1': '316',
        'date_time': '2024-12-01 09:57:45.789',
    },
    'value_tuple_int': '1,2,3',
    'value_tuple_float': '1.1,2.2,3.3,4.4',
    'value_tuple_int_float': '1,2.2,3',
}

# constants for testing date as date object
GOOD_DATE = date(2019, 7, 13)
GOOD_DATE_STR = '2019-07-13'
GOOD_DATETIME = datetime(2019, 7, 13, 4, 56, 8)
GOOD_DATETIME_STR = '2019-07-13T04:56:08'

DATA_ERROR_MESSAGE = 'Inspect the "data" attribute for the response data.'

@pytest.fixture(scope='module')
def client():
    client = SingStat(is_test_api=True)
    assert client.is_test_api is True
    return client

@pytest.fixture(scope='module')
def client_not_test():
    client = SingStat()
    assert client.is_test_api is False
    return client

def test_repr(client_not_test):
    assert repr(client_not_test).startswith(str(client_not_test.__class__))
    assert USER_AGENT in repr(client_not_test)

@pytest.mark.parametrize(
    (
        'original_params',
        'default_params',
        'key_map',
        'remove_none_values',
        'expected_params',
    ),
    [
        (
            {
                'foobar': 'foo bar',
                'date': GOOD_DATE,
                'datetime': GOOD_DATETIME,
                'none_value': None,
            },
            {
                'foobar': 'foo and bar',
                'meaning_of_universe': 42,
            },
            {
                'datetime': 'DATE_TIME',
                'meaning_of_universe': 'meaningOfUniverse',
            },
            True,
            {
                'foobar': 'foo bar',
                'date': GOOD_DATE_STR,
                'DATE_TIME': GOOD_DATETIME_STR,
                'meaningOfUniverse': 42,
            },
        ),
        (
            {
                'foobar': 'foo bar',
                'date': GOOD_DATE,
                'datetime': GOOD_DATETIME,
                'none_value': None,
            },
            None,
            None,
            False,
            {
                'foobar': 'foo bar',
                'date': GOOD_DATE_STR,
                'datetime': GOOD_DATETIME_STR,
                'none_value': None,
            },
        ),
    ],
)
def test_build_params(
    client,
    original_params,
    default_params,
    key_map,
    remove_none_values,
    expected_params,
):
    params = client.build_params(
        MockArgsDict,
        original_params,
        default_params,
        key_map,
        remove_none_values,
    )
    assert params == expected_params

@pytest.mark.parametrize(
    ('kwargs', 'expected_result'),
    [
        (
            {},
            {
                'value_str': 'foo bar',
                'value_ignore': 37,
                'value_int': 42,
                'value_bool': True,
                'value_date': date(2019, 7, 1),
                'value_blank': '',
                'value_list': [1, 2, {
                    'key1': 205,
                    'date_time': datetime(2024, 12, 1, 9, 57, 45, tzinfo=ZoneInfo(key='Asia/Singapore')),
                }],
                'value_dict': {
                    'key1': 316,
                    'date_time': datetime(2024, 12, 1, 9, 57, 45, 789000, tzinfo=ZoneInfo(key='Asia/Singapore')),
                },
                'value_tuple_int': (1, 2, 3),
                'value_tuple_float': (1.1, 2.2, 3.3, 4.4),
                'value_tuple_int_float': '1,2.2,3',
            },
        ),
        (
            {'iterate': False},
            SANITISE_DATA_DICT,
        ),
        (
            {
                'ignore_keys': [
                    'value_ignore',
                    'value_dict.date_time',
                    'value_list[].key1',
                ]
            },
            {
                'value_str': 'foo bar',
                'value_ignore': '37',
                'value_int': 42,
                'value_bool': True,
                'value_date': date(2019, 7, 1),
                'value_blank': '',
                'value_list': [1, 2, {
                    'key1': '205',
                    'date_time': datetime(2024, 12, 1, 9, 57, 45, tzinfo=ZoneInfo(key='Asia/Singapore')),
                }],
                'value_dict': {
                    'key1': 316,
                    'date_time': '2024-12-01 09:57:45.789',
                },
                'value_tuple_int': (1, 2, 3),
                'value_tuple_float': (1.1, 2.2, 3.3, 4.4),
                'value_tuple_int_float': '1,2.2,3',
            },
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
    ('kwargs', 'expected_data'),
    [
        (
            # default parameter values
            {
                'url': 'https://tablebuilder.singstat.gov.sg/api/gndn',
                'params': {'param1': 'value1', 'param2': 'value2'},
            },
            {
                'Data': {
                    'generatedBy': 'SingStat Table Builder',
                    'records': {
                        'foo': 'bar',
                        'number': 42,
                        'may_ignore': (37, 81),
                        'may_ignore_too': 123.456,
                    },
                },
                'DataCount': 1,
                'StatusCode': 200,
                'Message': '',
            },
        ),
        (
            # with cache duration
            {
                'url': 'https://tablebuilder.singstat.gov.sg/api/gndn',
                'params': {'param1': 'value1', 'param2': 'value2'},
                'cache_duration': 3600,
            },
            {
                'Data': {
                    'generatedBy': 'SingStat Table Builder',
                    'records': {
                        'foo': 'bar',
                        'number': 42,
                        'may_ignore': (37, 81),
                        'may_ignore_too': 123.456,
                    },
                },
                'DataCount': 1,
                'StatusCode': 200,
                'Message': '',
            },
        ),
        (
            # without sanitisation
            {
                'url': 'https://tablebuilder.singstat.gov.sg/api/gndn',
                'params': {'param1': 'value1', 'param2': 'value2'},
                'sanitise': False,
            },
            {
                'Data': {
                    'generatedBy': 'SingStat Table Builder',
                    'records': {
                        'foo': 'bar',
                        'number': '42',
                        'may_ignore': '37,81',
                        'may_ignore_too': '123.456',
                    },
                },
                'DataCount': 1,
                'StatusCode': 200,
                'Message': '',
            },
        ),
        (
            # with sanitisation and ignore keys
            {
                'url': 'https://tablebuilder.singstat.gov.sg/api/gndn',
                'params': {'param1': 'value1', 'param2': 'value2'},
                'sanitise_ignore_keys': [
                    'Data.records.may_ignore',
                    'Data.records.may_ignore_too',
                ],
            },
            {
                'Data': {
                    'generatedBy': 'SingStat Table Builder',
                    'records': {
                        'foo': 'bar',
                        'number': 42,
                        'may_ignore': '37,81',
                        'may_ignore_too': '123.456',
                    },
                },
                'DataCount': 1,
                'StatusCode': 200,
                'Message': '',
            },
        ),
    ],
)
def test_send_request(kwargs, expected_data, monkeypatch):
    """IMPORTANT!

    Use a new ``client_patched`` here so that the CachedSession get() method \
        can be monkeypatched to return the mock response for this specific \
        test.

    If the fixture ``client`` were used, then other tests that also use \
        ``client`` would fail due to the monkeypatch.
    """
    def mock_requests_get(*args, **kwargs):
        return APIResponseSendRequest()

    monkeypatch.setattr(CachedSession, 'get', mock_requests_get)

    client_patched = SingStat(is_test_api=True)

    original_session_get = client_patched.session.get
    client_patched.session.get = Mock(side_effect=original_session_get)

    data = client_patched.send_request(**kwargs)

    client_patched.session.get.assert_called_once()

    called_args, called_kwargs = client_patched.session.get.call_args
    assert called_args[0] == kwargs['url']
    for k, v in kwargs['params'].items():
        assert called_kwargs['params'][k] == v
    if 'cache_duration' in kwargs:
        assert called_kwargs['expire_after'] == kwargs['cache_duration']

    assert data == expected_data

def test_send_request_with_invalid_endpoint(client):
    with pytest.raises(HTTPError):
        _ = client.send_request(
            'https://tablebuilder.singstat.gov.sg/api/table/',
        )

def test_send_request_with_zero_data_value(client, monkeypatch):
    def mock_requests_get(*args, **kwargs):
        return APIResponseZeroData()

    monkeypatch.setattr(CachedSession, 'get', mock_requests_get)

    with pytest.raises(APIError) as excinfo:
        _ = client.send_request(
            'https://tablebuilder.singstat.gov.sg/api/table/tabledata/M212151'
        )

    assert excinfo.value.message == \
        f'No data records returned. {DATA_ERROR_MESSAGE}'
    assert excinfo.value.data == APIResponseZeroData().json()

def test_send_request_with_bad_request(client, monkeypatch):
    def mock_requests_get(*args, **kwargs):
        return APIResponseBadRequest()

    monkeypatch.setattr(CachedSession, 'get', mock_requests_get)

    with pytest.raises(APIError) as excinfo:
        _ = client.send_request(
            'https://tablebuilder.singstat.gov.sg/api/table/resourceid',
            {'keyword': 'house'},
        )

    assert excinfo.value.message == \
        f'One or more validation errors occurred. {DATA_ERROR_MESSAGE}'
    assert excinfo.value.data == APIResponseBadRequest().json()
