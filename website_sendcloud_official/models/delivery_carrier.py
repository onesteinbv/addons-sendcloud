# Copyright 2021 Onestein (<https://www.onestein.nl>)
# License OPL-1 (https://www.odoo.com/documentation/14.0/legal/licenses.html#odoo-apps).

from odoo import models, api


class DeliveryCarrier(models.Model):
    _inherit = "delivery.carrier"

    @api.model
    def _sendcloud_publish_all_shipping_methods(self, company_id):
        shipping_methods = self.search(
            [("delivery_type", "=", "sendcloud"), ("company_id", "=", company_id)]
        )
        shipping_methods.write({"website_published": True})

    @api.model
    def sendcloud_sync_shipping_method(self):
        res = super().sendcloud_sync_shipping_method()
        for company in self.env["res.company"].search([]):
            integration = company.sendcloud_default_integration_id
            if integration and self.env.context.get(
                "sendcloud_publish_all_shipping_methods"
            ):
                self._sendcloud_publish_all_shipping_methods(company.id)
        return res
