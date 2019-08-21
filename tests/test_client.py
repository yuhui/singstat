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

"""Test that the Client class is working properly."""

import pytest

from singstat import Client
from singstat.exceptions import APIError

# constants for testing metadata() and tabledata()
BAD_RESOURCE_ID = 1234567890
GOOD_RESOURCE_ID = 14556

@pytest.fixture(scope='module')
def client():
    return Client()

def test_metadata(client):
    metadata = client.metadata(resource_id=GOOD_RESOURCE_ID)

    assert isinstance(metadata, dict)

    assert 'records' in metadata
    assert isinstance(metadata['records'], list)
    assert len(metadata['records']) == 1
    record = metadata['records'][0]

    assert 'resourceId' in record
    assert record['resourceId'] == GOOD_RESOURCE_ID

    assert 'variables' in record
    assert isinstance(record['variables'], list)

def test_metadata_with_bad_resource_id(client):
    with pytest.raises(APIError):
        _ = client.metadata(resource_id=BAD_RESOURCE_ID)

def test_resource_id(client):
    resources = client.resource_id()

    assert isinstance(resources, dict)

    assert 'records' in resources
    assert isinstance(resources['records'], list)

def test_tabledata(client):
    tabledata = client.tabledata(
        resource_id=GOOD_RESOURCE_ID,
    )

    assert isinstance(tabledata, dict)

    assert 'resourceId' in tabledata
    assert tabledata['resourceId'] == GOOD_RESOURCE_ID

    assert 'variables' in tabledata
    assert isinstance(tabledata['variables'], list)

    assert 'records' in tabledata
    assert isinstance(tabledata['records'], list)

def test_tabledata_with_bad_resource_id(client):
    with pytest.raises(APIError):
        _ = client.tabledata(resource_id=BAD_RESOURCE_ID)
