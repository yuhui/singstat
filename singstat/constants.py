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

"""Constants that can be used anywhere."""

BASE_API_DOMAIN = 'https://tablebuilder.singstat.gov.sg'
BASE_API_ENDPOINT = f'{BASE_API_DOMAIN}/api/table'

METADATA_ENDPOINT = f'{BASE_API_ENDPOINT}/metadata'
RESOURCE_ID_ENDPOINT = f'{BASE_API_ENDPOINT}/resourceid'
TABLEDATA_ENDPOINT = f'{BASE_API_ENDPOINT}/tabledata'
__all__ = [
    'METADATA_ENDPOINT',
    'RESOURCE_ID_ENDPOINT',
    'TABLEDATA_ENDPOINT',
]
