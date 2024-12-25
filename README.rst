singstat
========

|pyversions| |pypi| |status| |codecov| |downloads| |license| |readthedocs|

.. |pyversions| image:: https://img.shields.io/pypi/pyversions/singstat
   :alt: Python 3
.. |pypi| image:: https://img.shields.io/pypi/v/singstat
   :alt: PyPi
   :target: https://pypi.org/project/singstat
.. |status| image:: https://img.shields.io/pypi/status/singstat
   :alt: PyPi status
.. |codecov| image:: https://codecov.io/gh/yuhui/singstat/graph/badge.svg?token=ahhqotTFVt
   :target: https://codecov.io/gh/yuhui/singstat
   :alt: CodeCov coverage
.. |downloads| image:: https://img.shields.io/pypi/dm/singstat
.. |license| image:: https://img.shields.io/github/license/yuhui/singstat
   :alt: GNU General Public License v3.0
   :target: https://www.gnu.org/licenses/gpl-3.0.html
.. |readthedocs| image:: https://readthedocs.org/projects/singstat/badge/?version=latest
   :alt: Documentation Status
   :target: https://singstat.readthedocs.io/en/latest/?badge=latest

This is an unofficial Python package for interacting with APIs available at
`SingStat.gov.sg`_.

.. _SingStat.gov.sg: https://www.singstat.gov.sg

Installing the package
----------------------

Install the package using ``pip``::

    pip install singstat

Using the package
-----------------

The main steps are:

1. Import the Client class.
2. Instantiate an object from the Client class.
3. Call a function on that object.

For more information, `refer to the documentation`_.

.. _refer to the documentation: http://singstat.readthedocs.io/

Usage overview
^^^^^^^^^^^^^^

Interacting with `SingStat.gov.sg`_'s API is done through a client.

This client contains several public functions, one function per endpoint. A
function's name is the same as its corresponding endpoint's ending path.

Most functions accept named arguments, where an argument corresponds with a
parameter that the endpoint accepts.

Reference
---------

`SingStat.gov.sg's Developer Guide`_

.. _SingStat.gov.sg's Developer Guide: https://tablebuilder.singstat.gov.sg/view-api/for-developers

Other Packages Built by Me
--------------------------

If you like this package, you may be interested in these packages that I have
built to work with other Government of Singapore APIs:

- `datagovsg`_: for interacting with APIs available at Data.gov.sg.
- `landtransportsg`_: for interacting with APIs available at LTA DataMall.

.. _datagovsg: https://pypi.org/project/datagovsg/
.. _landtransportsg: https://pypi.org/project/landtransportsg/
