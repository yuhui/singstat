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

"""Client for interacting with the SingStat API endpoints."""

import re
from typing import Any
from warnings import warn

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

    References: \
        https://tablebuilder.singstat.gov.sg/view-api/for-developers
    """

    @typechecked
    def metadata(self, resource_id: str) -> MetadataDict:
        """Return the metadata of a resource.

        :param resource_id: ID of the resource.
        :type resource_id: str

        :warns RuntimeWarning: "Empty data set returned" when ``data_count`` \
            is 1 but ``data.records`` is empty.

        :return: Metadata of the requested resource.
        :rtype: MetadataDict
        """
        metadata: MetadataDict

        metadata_endpoint = f'{METADATA_ENDPOINT}/{resource_id}'
        metadata = self.send_request(metadata_endpoint)

        data_count = metadata['DataCount']
        records = metadata['Data']['records']

        if data_count == 1 and len(records) == 0:
            warn('Empty data set returned', RuntimeWarning)

        return metadata

    @typechecked
    def resource_id(self, **kwargs: Any) -> ResourceIdDict:
        """Search for a list of resources.

        :param kwargs: Key-value arguments to be passed as parameters \
            to the endpoint URL. Refer to ``ResourceIdArgsDict`` for the \
            specification of the argument names and types.
        :type kwargs: ResourceIdArgsDict

        :raises APIError: ``search_option`` is not "all", "title" or "variable".

        :warns RuntimeWarning: "Empty data set returned" when ``data_count`` \
            is 1 but ``data.total`` is 0.

        :return: List of resources.
        :rtype: ResourceIdDict
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

        data_count = resources['DataCount']
        total = resources['Data']['total']

        if data_count == 1 and total == 0:
            warn('Empty data set returned', RuntimeWarning)

        return resources

    @typechecked
    def tabledata(self, resource_id: str, **kwargs: Any) -> TabledataDict:
        """Retrieve data in a resource.

        :param resource_id: ID of the resource.
        :type resource_id: str

        :param kwargs: Key-value arguments to be passed as parameters \
            to the endpoint URL. Refer to ``TabledataArgsDict`` for the \
            specification of the argument names and types.
        :type kwargs: TabledataArgsDict

        :raises APIError: ``between`` tuple has at least one value that is \
            less than 0.
        :raises APIError: ``between`` tuple's first value is greater than its \
            second value.
        :raises APIError: ``limit`` is not between 0 and 3000.
        :raises APIError: ``offset`` is less than 0.
        :raises APIError: ``sort_by`` does not match the regular expression \
            ``r'^(key|value|seriesNo|rowNo|rowText) (asc|desc)$'``.

        :warns RuntimeWarning: "Empty data set returned" when ``data_count`` \
            is 1 but ``data.row`` is empty.

        :return: Records of data that match the search criteria.
        :rtype: TabledataDict
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

        data_count = tabledata['DataCount']
        rows = tabledata['Data']['row']

        if data_count == 1 and len(rows) == 0:
            warn('Empty data set returned', RuntimeWarning)

        return tabledata

__all__ = [
    'Client',
]
