# License OPL-1 (https://www.odoo.com/documentation/14.0/legal/licenses.html#odoo-apps).

from odoo import SUPERUSER_ID, api


def migrate(cr, version):
    env = api.Environment(cr, SUPERUSER_ID, {})
    default_product = env.ref(
        "delivery_sendcloud_official.sendcloud_product_delivery")
    if not default_product:
        return
    if not default_product.company_id:
        default_product.active = False
    for company in env["res.company"].search([
        ("sendcloud_delivery_product_id", "=", False),
        ("sendcloud_integration_ids", "!=", False),
    ]):
        if default_product.company_id == company and default_product.active:
            company.sendcloud_delivery_product_id = default_product
        else:
            delivery_product = default_product.copy({
                'name': default_product.name,
                'default_code': default_product.default_code,
                'company_id': company.id,
                'active': True,
            })
            company.sendcloud_delivery_product_id = delivery_product
