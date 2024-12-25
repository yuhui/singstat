# Copyright 2024 Yuhui. All rights reserved.
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

"""SingStat custom types for client methods' arguments."""

from typing import NotRequired
try:
    from typing import TypedDict
except ImportError:
    TypedDict = dict

# metadata() does not have any input parameters

class ResourceIdArgsDict(TypedDict):
    """Type definition for resource_id() input parameters"""
    keyword: NotRequired[str]
    """Keyword to search resources by.

    :default: "%", i.e. don't search by any specific keyword.
    """
    search_option: NotRequired[str]
    """Where to search the keyword in:

    - "all": search in all resources.
    - "title": search in resource titles only.
    - "variable": search in resource variables only.

    :default: "all"
    """


class TabledataArgsDict(TypedDict):
    """Type definition for tabledata() input parameters"""
    series_no_or_row_no: NotRequired[list[str] | str]
    """Specify the seriesNo for Time Series Table and rowNo for Cross \
        Sectional Table and Multi-Dimensional Data Cubes.

    :example: ["13.1", "2.3"]
    :example: "13.1,2.3"
    """
    offset: NotRequired[int]
    """Specify the first n number of records to be excluded in the returned \
        result.
    """
    limit: NotRequired[int]
    """Specify the number (maximum = 3000) of records to be included in the \
        returned results for Time Series Table or number of rows to be \
        included in the returned results for Cross Sectional Table and \
        Multi-Dimensional Data Cubes.
    """
    sort_by: NotRequired[str]
    """Sort the returned records in descending ("desc") or ascending ("asc") \
        order by the fields:

    - "key"
    - "value"
    - "seriesNo"
    - "rowText"
    - "rowNo"

    Not applicable for Cross Sectional tables and Multi-Dimensional Data Cubes.

    :example: "key asc"
    """
    time_filter: NotRequired[tuple[str] | tuple[str, str] | str]
    """Return records of specific time points based on the type of selected \
        table (monthly, half-yearly, quarterly, annual). Not applicable for \
        Cross Sectional tables and Multi-Dimensional Data Cubes.

    :example: For the quarterly table: ("2017 4Q", "2018 1Q") or \
        "2017 4Q,2018 1Q".
    :example: For the annual table: ("2017", "2018") or "2017,2018".
    :example: For the monthly table: ("2018 Mar") or "2018 Mar".
    :example: For the half yearly table: ("2018 1H") or "2018 1H".
    """
    between: NotRequired[tuple[int, int] | str]
    """Range within which the data values are to be filtered to give the \
        returned result. The start and end points of the range are to be \
        included.

    :example: (1560, 1677)
    :example: "1560,1677"
    """
    search: NotRequired[str]
    """Return records that contain the search string.
    """

__all__ = [
    'ResourceIdArgsDict',
    'TabledataArgsDict',
]
