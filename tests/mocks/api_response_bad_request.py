# Copyright 2026 Yuhui. All rights reserved.
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

"""Mock response to return response with bad request."""

class APIResponseBadRequest:
    status_code = 400

    @staticmethod
    def json():
        return {
            "Data": {
                "type": "https://tools.ietf.org/html/rfc9110#section-15.5.1",
                "title": "One or more validation errors occurred.",
                "status": 400,
                "errors": {
                    "SearchOption": [
                        "The SearchOption field is required."
                    ]
                },
                "traceId": "00-3b816b577dac6264a170f3cf2b21a8f6-646a60ea1f649933-00"
            },
            "DataCount": 1,
            "StatusCode": 400,
            "Message": ""
        }

__all__ = [
    'APIResponseBadRequest',
]