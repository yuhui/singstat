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

"""Test that the net functions are working properly."""

import pytest

from singstat import net

@pytest.mark.parametrize(
    ('url', 'kwargs'),
    [
        (
            'https://tablebuilder.singstat.gov.sg/api/table/resourceId?keyword=%25&searchOption=All',
            {},
        ),
        (
            'https://tablebuilder.singstat.gov.sg/api/table/metadata/14556',
            {},
        ),
        (
            'https://tablebuilder.singstat.gov.sg/api/table/tabledata/14556',
            {},
        ),
    ],
)
def test_send_request(url, kwargs):
    response_content = net.send_request(url, **kwargs)
    assert isinstance(response_content, dict)
