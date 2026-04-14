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

"""Constants that can be used anywhere."""

from .version import VERSION

NAME = 'singstat'

BASE_API_DOMAIN = 'https://tablebuilder.singstat.gov.sg'
BASE_API_ENDPOINT = f'{BASE_API_DOMAIN}/api/table'

METADATA_ENDPOINT = f'{BASE_API_ENDPOINT}/metadata'
RESOURCE_ID_ENDPOINT = f'{BASE_API_ENDPOINT}/resourceid'
TABLEDATA_ENDPOINT = f'{BASE_API_ENDPOINT}/tabledata'

RESOURCE_ID_ARGS_KEY_MAP = {
    'search_option': 'searchOption',
}
RESOURCE_ID_DEFAULT_ARGS = {
    'keyword': '%',
    'search_option': 'all',
}
RESOURCE_ID_SEARCH_OPTIONS = ('all', 'title', 'variable')

METADATA_SANITISE_IGNORE_KEYS = [
    'Data.records.id',
    'Data.records.startPeriod',
    'Data.records.endPeriod',
    'Data.records.column1[].columnNo',
    'Data.records.column2[].columnNo',
    'Data.records.column3[].columnNo',
    'Data.records.column4[].columnNo',
    'Data.records.column5[].columnNo',
    'Data.records.column6[].columnNo',
    'Data.records.column7[].columnNo',
    'Data.records.column8[].columnNo',
    'Data.records.column9[].columnNo',
    'Data.records.column10[].columnNo',
    'Data.records.row[].rowNo',
    'Data.records.row[].seriesNo',
]

TABLEDATA_ARGS_KEY_MAP = {
    'series_no_or_row_no': 'seriesNoOrRowNo',
    'sort_by': 'sortBy',
    'time_filter': 'timeFilter',
}
TABLEDATA_SANITISE_IGNORE_KEYS = [
    'Data.id',
    'Data.row[].columns[].key',
    'Data.row[].rowNo',
    'Data.row[].seriesNo',
]
TABLEDATA_SORT_BY_REGEXP = r'^(key|value|seriesNo|rowNo|rowText) (asc|desc)$'

CACHE_NAME = f'{NAME}_cache'

CACHE_TWELVE_HOURS = 60 * 60 * 12

USER_AGENT = f'SingStat Python package/{VERSION} https://pypi.org/project/{NAME}'

__all__ = [
    'NAME',

    'METADATA_ENDPOINT',
    'RESOURCE_ID_ENDPOINT',
    'TABLEDATA_ENDPOINT',

    'RESOURCE_ID_ARGS_KEY_MAP',
    'RESOURCE_ID_DEFAULT_ARGS',
    'RESOURCE_ID_SEARCH_OPTIONS',

    'METADATA_SANITISE_IGNORE_KEYS',

    'TABLEDATA_ARGS_KEY_MAP',
    'TABLEDATA_SORT_BY_REGEXP',
    'TABLEDATA_SANITISE_IGNORE_KEYS',

    'CACHE_NAME',

    'CACHE_TWELVE_HOURS',

    'USER_AGENT',
]
