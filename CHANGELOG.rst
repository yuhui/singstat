Changelog
=========

[2.0.2] - 2024-12-29
--------------------

Changed
^^^^^^^

- Don't convert response keys from camelCase to snake_case, i.e. leave the keys untouched.
    - ``Client``'s methods' argument names are still required to be in snake_case.

[2.0.1] - 2024-12-26
--------------------

Changed
^^^^^^^

- Updated minimum Python version to v3.11.

[2.0.0] - 2024-12-26
--------------------

**Alert!** This version was yanked because it requires an incorrect version of Python.

Added
^^^^^

- Add type hints for input arguments and output responses.
    -  Type check performed by typeguard_.
- Add packages: ``requests-cache``, ``typeguard``, ``types-requests``.

.. _typeguard: https://typeguard.readthedocs.io/en/latest/

Changed
^^^^^^^

- **Breaking:** Require argument names and response keys to use snake_case. This is enforced with ``typeguard``.
- **Breaking:** ``tabledata()``: Remove the argument ``variables``, because SingStat removed it from the endpoint.
- Require minimum Python version to v3.10.

Removed
^^^^^^^

- Remove packages: ``backoff``, ``cachetools``, ``pytz``.

[1.1.0] - 2024-02-02
--------------------

Changed
^^^^^^^

- Commit contributions from @qiujunda92 to interact with SingStat.gov.sg's documented API endpoints as of January 2024.
    - Add user-agent in header.
    - Update endpoint base path.
    - Update ``pytz`` version.
- Update package build to use ``build``.

[1.0.2] - 2020-01-19
--------------------

Changed
^^^^^^^

- Update ``pytest`` requirement.

[1.0.1] - 2019-09-03
--------------------

Changed
^^^^^^^

- Use relative imports.

[1.0.0] - 2019-08-21
--------------------

Initial version to interact with SingStat.gov.sg's documented API endpoints as of August 2019.
