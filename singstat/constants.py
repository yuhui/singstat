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

BASE_API_DOMAIN = 'https://tablebuilder.singstat.gov.sg'
BASE_API_ENDPOINT = f'{BASE_API_DOMAIN}/api/table'

METADATA_ENDPOINT = f'{BASE_API_ENDPOINT}/metadata'
RESOURCE_ID_ENDPOINT = f'{BASE_API_ENDPOINT}/resourceid'
TABLEDATA_ENDPOINT = f'{BASE_API_ENDPOINT}/tabledata'

RESOURCE_ID_DEFAULT_ARGS = {
    'keyword': '%',
    'search_option': 'all',
}
RESOURCE_ID_SEARCH_OPTIONS = ('all', 'title', 'variable')

TABLEDATA_SORT_BY_REGEXP = r'^(key|value|seriesNo|rowNo|rowText) (asc|desc)$'

DATA_KEYS_TO_SANITISE = (
    'between',
    'dataLastUpdated',
    'dateGenerated',
    'limit',
    'offset',
    'rowNo',
    'total',
)

CACHE_NAME = 'singstat_cache'
CACHE_TWELVE_HOURS = 60 * 60 * 12
USER_AGENT = f'SingStat Python package/2.0.1 https://pypi.org/project/singstat'

__all__ = [
    'METADATA_ENDPOINT',
    'RESOURCE_ID_ENDPOINT',
    'TABLEDATA_ENDPOINT',

    'RESOURCE_ID_DEFAULT_ARGS',
    'RESOURCE_ID_SEARCH_OPTIONS',

    'TABLEDATA_SORT_BY_REGEXP',

    'DATA_KEYS_TO_SANITISE',

    'CACHE_NAME',
    'CACHE_TWELVE_HOURS',

    'USER_AGENT',
]
