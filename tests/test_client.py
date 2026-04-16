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

"""Test that the Client class is working properly."""

from unittest.mock import Mock
from warnings import catch_warnings, simplefilter

import pytest
from requests import HTTPError
from requests_cache import CachedSession
from typeguard import check_type

from singstat.client import Client
from singstat.client.constants import (
    METADATA_ENDPOINT,
    RESOURCE_ID_ENDPOINT,
    TABLEDATA_ENDPOINT,
)
from singstat.client.types import (
    MetadataDict,
    ResourceIdDict,
    TabledataDict,
)

from .mocks.api_response_empty_data import (
    APIResponseEmptyMetadata,
    APIResponseEmptyTabledata,
)

# constants for testing resource_id()
BAD_KEYWORD = 'sdfger934rzh'
BAD_SEARCH_OPTION = 'foo'
GOOD_KEYWORD = 'house'
GOOD_SEARCH_OPTION = 'title'

# constants for testing metadata() and tabledata()
BAD_RESOURCE_ID = '12345'
GOOD_RESOURCE_ID = 'M212151'
GOOD_CUBE_RESOURCE_ID = '8865'

@pytest.fixture(scope='module')
def client():
    client = Client(is_test_api=True)

    original_send_request = client.send_request
    client.send_request = Mock(side_effect=original_send_request)

    return client

@pytest.mark.parametrize(
    ('kwargs', 'params'),
    [
        ({}, {}),
        # one parameter at a time
        (
            {'keyword': GOOD_KEYWORD},
            {'keyword': GOOD_KEYWORD},
        ),
        (
            {'search_option': GOOD_SEARCH_OPTION},
            {'searchOption': GOOD_SEARCH_OPTION},
        ),
        # all parameters together
        (
            {'keyword': GOOD_KEYWORD, 'search_option': GOOD_SEARCH_OPTION},
            {'keyword': GOOD_KEYWORD, 'searchOption': GOOD_SEARCH_OPTION},
        ),
    ],
)
def test_resource_id(client, kwargs, params):
    resources = client.resource_id(**kwargs)

    called_args, called_kwargs = client.send_request.call_args
    assert called_args[0] == RESOURCE_ID_ENDPOINT
    for k, v in params.items():
        assert called_kwargs['params'][k] == v

    assert check_type(resources, ResourceIdDict) == resources

@pytest.mark.parametrize(
    ('kwargs'),
    [
        {'search_option': BAD_SEARCH_OPTION},
    ],
)
def test_resource_id_with_bad_inputs(client, kwargs):
    with pytest.raises(ValueError):
        _ = client.resource_id(**kwargs)

@pytest.mark.parametrize(
    ('kwargs'),
    [
        {'keyword': BAD_KEYWORD, 'search_option': GOOD_SEARCH_OPTION},
    ],
)
def test_resource_id_with_empty_data(client, kwargs):
    with catch_warnings(record=True) as w:
        # Cause all warnings to always be triggered.
        simplefilter('always')

        _ = client.resource_id(**kwargs)

        assert len(w) == 1
        assert issubclass(w[-1].category, RuntimeWarning)
        assert 'Empty data set returned' in str(w[-1].message)

@pytest.mark.parametrize(
    ('resource_id'),
    [GOOD_RESOURCE_ID, GOOD_CUBE_RESOURCE_ID]
)
def test_metadata(client, resource_id):
    metadata = client.metadata(resource_id=resource_id)

    called_args, _ = client.send_request.call_args
    assert called_args[0] == f'{METADATA_ENDPOINT}/{resource_id}'

    assert check_type(metadata, MetadataDict) == metadata

def test_metadata_with_bad_resource_id(client):
    with pytest.raises(HTTPError):
        _ = client.metadata(resource_id=BAD_RESOURCE_ID)

def test_metadata_with_empty_data(client, monkeypatch):
    def mock_requests_get(*args, **kwargs):
        return APIResponseEmptyMetadata()

    monkeypatch.setattr(CachedSession, 'get', mock_requests_get)

    with catch_warnings(record=True) as w:
        # Cause all warnings to always be triggered.
        simplefilter('always')

        _ = client.metadata(BAD_RESOURCE_ID)

        assert len(w) == 1
        assert issubclass(w[-1].category, RuntimeWarning)
        assert 'Empty data set returned' in str(w[-1].message)

@pytest.mark.parametrize(
    ('resource_id', 'kwargs', 'params'),
    [
        (GOOD_RESOURCE_ID, {}, {}),
        # one parameter at a time
        (
            GOOD_RESOURCE_ID,
            {'series_no_or_row_no': ['1.1.1', '1.99']},
            {'seriesNoOrRowNo': '1.1.1,1.99'},
        ),
        (
            GOOD_RESOURCE_ID,
            {'offset': 1},
            {'offset': 1},
        ),
        (
            GOOD_RESOURCE_ID,
            {'limit': 10},
            {'limit': 10},
        ),
        (
            GOOD_RESOURCE_ID,
            {'sort_by': 'seriesNo asc'},
            {'sortBy': 'seriesNo asc'},
        ),
        (
            GOOD_RESOURCE_ID,
            {'time_filter': ('2018', '2023')},
            {'timeFilter': '2018,2023'},
        ),
        (
            GOOD_RESOURCE_ID,
            {'between': (0, 100)},
            {'between': '0,100'},
        ),
        (
            GOOD_RESOURCE_ID,
            {'search': 'and'},
            {'search': 'and'},
        ),
        # all parameters together
        (
            GOOD_RESOURCE_ID,
            {
                'series_no_or_row_no': ['1.1.1', '1.99'],
                'offset': 1,
                'limit': 10,
                'sort_by': 'seriesNo asc',
                'time_filter': ('2018', '2023'),
                'between': (0, 100),
                'search': 'and',
            },
            {
                'seriesNoOrRowNo': '1.1.1,1.99',
                'offset': 1,
                'limit': 10,
                'sortBy': 'seriesNo asc',
                'timeFilter': '2018,2023',
                'between': '0,100',
                'search': 'and',
            },
        ),
        # all parameters together as strings
        (
            GOOD_RESOURCE_ID,
            {
                'series_no_or_row_no': '1.1.1,1.99',
                'offset': 1,
                'limit': 10,
                'sort_by': 'seriesNo asc',
                'time_filter': '2018,2023',
                'between': '0,100',
                'search': 'and',
            },
            {
                'seriesNoOrRowNo': '1.1.1,1.99',
                'offset': 1,
                'limit': 10,
                'sortBy': 'seriesNo asc',
                'timeFilter': '2018,2023',
                'between': '0,100',
                'search': 'and',
            },
        ),
        (GOOD_CUBE_RESOURCE_ID, {}, {}),
        # all parameters together
        (
            GOOD_CUBE_RESOURCE_ID,
            {
                'series_no_or_row_no': '1.6,1.8,3',
                'offset': 1,
                'limit': 10,
                'sort_by': 'rowNo asc',
                'time_filter': ('2018'),
                'between': (0, 100),
                'search': 'polytechnic',
            },
            {
                'seriesNoOrRowNo': '1.6,1.8,3',
                'offset': 1,
                'limit': 10,
                'sortBy': 'rowNo asc',
                'timeFilter': '2018',
                'between': '0,100',
                'search': 'polytechnic',
            },
        ),
    ],
)
def test_tabledata(client, resource_id, kwargs, params):
    tabledata = client.tabledata(resource_id=resource_id, **kwargs)

    called_args, called_kwargs = client.send_request.call_args
    assert called_args[0] == f'{TABLEDATA_ENDPOINT}/{resource_id}'
    for k, v in params.items():
        assert called_kwargs['params'][k] == v

    assert check_type(tabledata, TabledataDict) == tabledata

def test_tabledata_with_bad_resource_id(client):
    with pytest.raises(HTTPError):
        _ = client.tabledata(resource_id=BAD_RESOURCE_ID)

@pytest.mark.parametrize(
    ('kwargs'),
    [
        {
            # 'between' has negative value
            'between': (0, -100),
        },
        {
            # 'between'  first value bigger than second value
            'between': (100, 0),
        },
        {
            # 'limit' has negative value
            'limit': -10,
        },
        {
            # 'limit' value is greater than 3000
            'limit': 5000,
        },
        {
            # 'offset' has negative value
            'offset': -10,
        },
        {
            'sort_by': 'foo',
        },
    ],
)
def test_tabledata_with_bad_inputs(client, kwargs):
    with pytest.raises(ValueError):
        _ = client.tabledata(resource_id=GOOD_RESOURCE_ID, **kwargs)

def test_tabledata_with_empty_data(client, monkeypatch):
    def mock_requests_get(*args, **kwargs):
        return APIResponseEmptyTabledata()

    monkeypatch.setattr(CachedSession, 'get', mock_requests_get)

    with catch_warnings(record=True) as w:
        # Cause all warnings to always be triggered.
        simplefilter('always')

        _ = client.tabledata(BAD_RESOURCE_ID)

        assert len(w) == 1
        assert issubclass(w[-1].category, RuntimeWarning)
        assert 'Empty data set returned' in str(w[-1].message)
