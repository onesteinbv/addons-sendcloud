# Copyright 2021 Onestein (<https://www.onestein.nl>)
# License OPL-1 (https://www.odoo.com/documentation/14.0/legal/licenses.html#odoo-apps).

from odoo import models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    def _get_delivery_methods(self):
        ctx = dict(self.env.context, sale_order_id=self.id)
        return super(SaleOrder, self.with_context(ctx))._get_delivery_methods()

    def _cart_update(
        self, product_id=None, line_id=None, add_qty=0, set_qty=0, **kwargs
    ):
        """ Override to update carrier quotation if quantity changed """
        # TODO
        return super()._cart_update(product_id, line_id, add_qty, set_qty, **kwargs)

    def sendcloud_sale_delivery_data(self, carrier):
        self.ensure_one()
        self.write({"sendcloud_service_point_address": False})
        return {
            "sendcloud_details": {
                "order_id": self.id,
                "key": carrier.sendcloud_integration_id.public_key or "",
                "country_code": self.partner_shipping_id.country_id.code or "",
                "postcode": self.partner_id.zip or "",
                "carrier_name": [carrier.sendcloud_carrier or ""],
            }
        }
