# Copyright 2024 Yuhui
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

# pylint: disable=missing-class-docstring,missing-function-docstring

"""Mock response to return response with empty data records."""

from datetime import date

class APIResponseEmptyMetadata:
    status_code = 200

    @staticmethod
    def json():
        return {
            'data': {
                'generatedBy': 'SingStat Table Builder',
                'dateGenerated': date(2024, 12, 1),
                'records': {},
            },
            'DataCount': 1,
            'StatusCode': 200,
            'Message': '',
        }

class APIResponseEmptyTabledata:
    status_code = 200

    @staticmethod
    def json():
        return {
            'data': {
                'generatedBy': 'SingStat Table Builder',
                'dateGenerated': date(2024, 12, 1),
                'row': [],
            },
            'DataCount': 1,
            'StatusCode': 200,
            'Message': '',
        }

__all__ = [
    'APIResponseEmptyMetadata',
    'APIResponseEmptyTabledata',
]