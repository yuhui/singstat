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

"""Client for interacting with the SingStat APIs."""

from cachetools import cached, TTLCache

from singstat import net
from singstat.constants import *

class Client(object):
    """Interact with SingStat's API to access its catalogue of datasets.

    References:
        https://www.tablebuilder.singstat.gov.sg/publicfacing/api/api-intro.html
    """

    @cached(cache=TTLCache(maxsize=CACHE_MAXSIZE, ttl=CACHE_ONE_DAY))
    def metadata(self, resource_id):
        """Return the metadata of a resource.

        Arguments:
            resource_id (str):
                ID of the resource.

        Returns:
            (dict) Metadata of the requested resource.
        """
        metadata_endpoint = '{}/{}'.format(METADATA_ENDPOINT, resource_id)
        metadata = net.send_request(metadata_endpoint)

        return metadata

    @cached(cache=TTLCache(maxsize=CACHE_MAXSIZE, ttl=CACHE_ONE_DAY))
    def resource_id(self, keyword='%', search_option='All'):
        """Search for a list of resources.

        Arguments:
            keyword (str):
                (optional) Keyword to search resources by.
                Default: "%", i.e. don't search by any specific keyword.
            search_option (str):
                (optional) Where to search the keyword in.
                    - "All": search in all resources.
                    - "Title": search in resource titles only.
                    - "Variable": search in resource variables only.
                Default: "All".

        Returns:
            (dict) List of resources.
        """
        resources = net.send_request(
            RESOURCE_ID_ENDPOINT,
            keyword=keyword,
            searchOption=search_option,
        )

        return resources

    @cached(cache=TTLCache(maxsize=CACHE_MAXSIZE, ttl=CACHE_ONE_DAY))
    def tabledata(
        self,
        resource_id,
        variables=[],
        between=[],
        sort_by=None,
        offset=0,
        limit=2000,
        time_filter=[],
        search=None,
    ):
        """Retrieve data in a resource.

        Arguments:
            resource_id (str):
                ID of the resource.
            variables (list):
                (optional) variables to retrieve.
                Example: ["variableCode 1", "variableCode 2", ...].
            between (list):
                (optional) Data value range to be returned.
                Example: [1560, 1677].
            sort_by (str):
                (optional) Comma-separated field names with ordering.
                Example: "variableCode,level desc".
            offset (int):
                (optional) Offset this number of records.
                Default: 0.
            limit (int):
                (optional) Number of records to return.
                Maximum is 2,000.
                Default: 2000.
            time_filter (list):
                (optional) Time points for the selected table. Examples:
                    - Monthly table: ["2018 Mar"]
                    - Quarterly table: ["2017 4Q", "2018 1Q"]
                    - Half yearly table: ["2018 H1"]
                    - Annual table: ["2017", "2018"]
            search (str):
                (optional) Text to search for records.

        Returns:
            (dict) Records of data that match the search criteria.
        """
        tabledata_endpoint = '{}/{}'.format(TABLEDATA_ENDPOINT, resource_id)
        tabledata = net.send_request(
            tabledata_endpoint,
            variables=','.join(variables),
            between=','.join([str(r) for r in between]),
            sortBy=sort_by,
            offset=offset,
            limit=limit,
            timeFilter=','.join(time_filter),
            search=search,
        )

        return tabledata
