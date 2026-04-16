singstat.client
===============

.. automodule:: singstat.client.client

Example usage:

.. code-block:: python

    # search for a resource ID
    from singstat import Client
    client = Client()
    resources = client.resource_id(keyword="population", search_option="all")

Methods
-------

.. autoclass:: Client
   :members:
   :member-order: bysource
   :show-inheritance:

Types
-----

.. toctree::
   :maxdepth: 1

   singstat.client.types_args
   singstat.client.types
