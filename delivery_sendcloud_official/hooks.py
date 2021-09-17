# Copyright 2021 Onestein (<https://www.onestein.nl>)
# License OPL-1 (https://www.odoo.com/documentation/14.0/legal/licenses.html#odoo-apps).

from odoo import api, SUPERUSER_ID


def uninstall_hook(cr, registry):
    env = api.Environment(cr, SUPERUSER_ID, {})
    carriers = env["delivery.carrier"].search([("delivery_type", "=", "sendcloud")])
    carriers.write({"delivery_type": "fixed", "active": False})
