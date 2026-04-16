Changelog
=========

[2.1.0] - 2026-04-16
--------------------

Changed
^^^^^^^

- Use `Unpack` from `typing` to define argument types.
- Update typehints according to API specifications.
- Specify allowed date and datetime string formats.
- Set datetime correctly in Singapore timezone.
- Require expected parameter type when building query parameters.
- Improve data sanitisation. Allow specifying of keys to ignore when sanitising.
- Set default error message and also mention if `data` and/or `errors` attributes are set in the error.
- Refactored code to separate ``Client``-specific code into its own module.

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

**Alert!** This version was yanked because it required an incorrect version of Python.

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

Added
^^^^^

- Initial version to interact with SingStat.gov.sg's documented API endpoints as of August 2019.
