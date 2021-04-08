In the Odoo configuration file add ``delivery_sendcloud_official`` in the list
``server_wide_modules``:

.. code-block:: ini

  [options]
  (...)
  server_wide_modules = web,delivery_sendcloud_official
  (...)

A restart of the Odoo server is required afterwards.