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

"""Test that the Client class is working properly."""

from warnings import catch_warnings, simplefilter

import pytest
from requests import HTTPError
from requests_cache import CachedSession
from typeguard import check_type

from singstat import Client
from singstat.types import MetadataDict, ResourceIdDict, TabledataDict

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
GOOD_CUBE_RESOURCE_ID = 'D10022'

@pytest.fixture
def mock_requests_empty_metadata(monkeypatch):
    """Requests.get() mocked to return metadata response with empty data."""

    def mock_requests_get(*args, **kwargs):
        return APIResponseEmptyMetadata()

    monkeypatch.setattr(CachedSession, 'get', mock_requests_get)

@pytest.fixture
def mock_requests_empty_tabledata(monkeypatch):
    """Requests.get() mocked to return tabledata response with empty data."""

    def mock_requests_get(*args, **kwargs):
        return APIResponseEmptyTabledata()

    monkeypatch.setattr(CachedSession, 'get', mock_requests_get)

@pytest.fixture(scope='module')
def client():
    return Client(is_test_api=True)

@pytest.mark.parametrize(
    ('kwargs'),
    [
        {},
        {'keyword': GOOD_KEYWORD},
        {'search_option': GOOD_SEARCH_OPTION},
        {'keyword': GOOD_KEYWORD, 'search_option': GOOD_SEARCH_OPTION},
    ],
)
def test_resource_id(client, kwargs):
    """This calls the live API endpoint."""
    resources = client.resource_id(**kwargs)

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
    """This calls the live API endpoint."""
    with catch_warnings(record=True) as w:
        # Cause all warnings to always be triggered.
        simplefilter('always')

        _ = client.resource_id(**kwargs)

        assert len(w) == 1
        assert issubclass(w[-1].category, RuntimeWarning)
        assert 'Empty data set returned' in str(w[-1].message)

def test_metadata(client):
    """This calls the live API endpoint."""
    metadata = client.metadata(resource_id=GOOD_RESOURCE_ID)

    assert check_type(metadata, MetadataDict) == metadata

def test_metadata_with_bad_resource_id(client):
    """This calls the live API endpoint."""
    with pytest.raises(HTTPError):
        _ = client.metadata(resource_id=BAD_RESOURCE_ID)

def test_metadata_with_empty_data(
    client,
    mock_requests_empty_metadata,
):
    with catch_warnings(record=True) as w:
        # Cause all warnings to always be triggered.
        simplefilter('always')

        _ = client.metadata(BAD_RESOURCE_ID)

        assert len(w) == 1
        assert issubclass(w[-1].category, RuntimeWarning)
        assert 'Empty data set returned' in str(w[-1].message)

@pytest.mark.parametrize(
    ('resource_id', 'kwargs'),
    [
        (GOOD_RESOURCE_ID, {}),
        (GOOD_RESOURCE_ID, {
            'series_no_or_row_no': ['1.1.1', '1.99'],
            'offset': 1,
            'limit': 10,
            'sort_by': 'seriesNo asc',
            'time_filter': ('2018', '2023'),
            'between': (0, 100),
            'search': 'and',
        }),
        (GOOD_RESOURCE_ID, {
            'series_no_or_row_no': '1.1.1,1.99',
            'offset': 1,
            'limit': 10,
            'sort_by': 'seriesNo asc',
            'time_filter': '2018,2023',
            'between': '0,100',
            'search': 'and',
        }),
        (GOOD_CUBE_RESOURCE_ID, {}),
        (GOOD_CUBE_RESOURCE_ID, {
            'series_no_or_row_no': '2,3',
            'offset': 1,
            'limit': 10,
            'sort_by': 'rowNo asc',
            'time_filter': ('2018'),
            'between': (0, 100),
            'search': 'and',
        }),
    ],
)
def test_tabledata(client, resource_id, kwargs):
    """This calls the live API endpoint."""
    tabledata = client.tabledata(resource_id=resource_id, **kwargs)

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
    """This calls the live API endpoint."""
    with pytest.raises(ValueError):
        _ = client.tabledata(resource_id=GOOD_RESOURCE_ID, **kwargs)

def test_tabledata_with_empty_data(
    client,
    mock_requests_empty_tabledata,
):
    with catch_warnings(record=True) as w:
        # Cause all warnings to always be triggered.
        simplefilter('always')

        _ = client.tabledata(BAD_RESOURCE_ID)

        assert len(w) == 1
        assert issubclass(w[-1].category, RuntimeWarning)
        assert 'Empty data set returned' in str(w[-1].message)
