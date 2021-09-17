# Copyright 2021 Onestein (<https://www.onestein.eu>)
# License OPL-1 (https://www.odoo.com/documentation/14.0/legal/licenses.html#odoo-apps).

from odoo import fields, models


class SendCloudCustomPriceDetailsWizard(models.TransientModel):
    _name = "sendcloud.custom.price.details.wizard"
    _description = "SendCloud Custom Price Details Wizard"

    shipping_method_country_id = fields.Many2one(
        "sendcloud.shipping.method.country",
        readonly=True,
        required=True,
        string="Shipping to Country",
    )
    price = fields.Float(related="shipping_method_country_id.price", string="Standard Price")
    price_custom = fields.Float(related="shipping_method_country_id.price_custom", readonly=False, string="Custom Price")
    price_check = fields.Selection(related="shipping_method_country_id.price_check")

    def set_custom_price(self):
        self.ensure_one()
        self.shipping_method_country_id.price_custom = self.price_custom

    def remove_custom_price(self):
        self.ensure_one()
        self.env[
            "sendcloud.shipping.method.country.custom"].search(
            [
                ("iso_2", "=", self.shipping_method_country_id.iso_2),
                ("company_id", "=", self.shipping_method_country_id.company_id.id),
                ("method_code", "=", self.shipping_method_country_id.method_code),
            ],
        ).unlink()
