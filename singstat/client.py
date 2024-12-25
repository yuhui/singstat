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

import re
from typing import Any

from typeguard import typechecked

from .constants import (
    METADATA_ENDPOINT,
    RESOURCE_ID_DEFAULT_ARGS,
    RESOURCE_ID_ENDPOINT,
    RESOURCE_ID_SEARCH_OPTIONS,
    TABLEDATA_ENDPOINT,
    TABLEDATA_SORT_BY_REGEXP,
)
from .singstat import SingStat
from .types_args import ResourceIdArgsDict, TabledataArgsDict
from .types import MetadataDict, ResourceIdDict, TabledataDict

class Client(SingStat):
    """Interact with SingStat's API to access its catalogue of datasets.

    References:
        https://tablebuilder.singstat.gov.sg/view-api/for-developers
    """

    @typechecked
    def metadata(self, resource_id: str) -> MetadataDict:
        """Return the metadata of a resource.

        Arguments:
            resource_id (str):
                ID of the resource.

        Returns:
            (dict) Metadata of the requested resource.
        """
        metadata: MetadataDict

        metadata_endpoint = f'{METADATA_ENDPOINT}/{resource_id}'
        metadata = self.send_request(metadata_endpoint)

        return metadata

    @typechecked
    def resource_id(self, **kwargs: Any) -> ResourceIdDict:
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
        resources: ResourceIdDict

        # Validate inputs
        if (
            'search_option' in kwargs
            and kwargs['search_option'] not in RESOURCE_ID_SEARCH_OPTIONS
        ):
            search_options = ('", "').join(RESOURCE_ID_SEARCH_OPTIONS)
            raise ValueError(
                f'Argument "search_option" must be one of "{search_options}".'
            )

        params = self.build_params(
            params_expected_type=ResourceIdArgsDict,
            original_params=kwargs,
            default_params=RESOURCE_ID_DEFAULT_ARGS,
        )

        resources = self.send_request(RESOURCE_ID_ENDPOINT, params)

        return resources

    @typechecked
    def tabledata(self, resource_id: str, **kwargs: Any) -> TabledataDict:
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
        tabledata: TabledataDict

        # Validate inputs
        if 'between' in kwargs and isinstance(kwargs['between'], tuple):
            if any(val < 0 for val in kwargs['between']):
                raise ValueError(
                    'values in argument "between" must be 0 or greater.'
                )
            if kwargs['between'][0] > kwargs['between'][1]:
                raise ValueError(
                    'first value in argument "between" must be smaller than second value.'
                )

        if (
            'limit' in kwargs
            and (kwargs['limit'] < 0 or kwargs['limit'] > 3000)
        ):
            raise ValueError('argument "limit" must be between 0 and 3000.')

        if 'offset' in kwargs and kwargs['offset'] < 0:
            raise ValueError('argument "offset" must be 0 or greater.')

        if (
            'sort_by' in kwargs
            and re.fullmatch(
                TABLEDATA_SORT_BY_REGEXP,
                kwargs['sort_by']
            ) is None
        ):
            raise ValueError('argument "sort_by" has invalid sort criteria.')

        params = self.build_params(
            params_expected_type=TabledataArgsDict,
            original_params=kwargs,
        )

        # Convert parameters to have the values that the endpoint expects
        if 'between' in params and isinstance(params['between'], tuple):
            params['between'] = ','.join(str(b) for b in params['between'])

        if (
            'seriesNoOrRowNo' in params
            and isinstance(params['seriesNoOrRowNo'], list)
        ):
            params['seriesNoOrRowNo'] = ','.join(params['seriesNoOrRowNo'])

        if 'timeFilter' in params and isinstance(params['timeFilter'], tuple):
            params['timeFilter'] = ','.join(params['timeFilter'])

        tabledata_endpoint = f'{TABLEDATA_ENDPOINT}/{resource_id}'
        tabledata = self.send_request(tabledata_endpoint, params)

        return tabledata

__all__ = [
    'Client',
]

