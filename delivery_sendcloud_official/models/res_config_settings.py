# Copyright 2021 Onestein (<https://www.onestein.nl>)
# License OPL-1 (https://www.odoo.com/documentation/14.0/legal/licenses.html#odoo-apps).

from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    is_sendcloud_test_mode = fields.Boolean(
        related="company_id.is_sendcloud_test_mode",
        readonly=False,
    )
    sendcloud_delivery_product_id = fields.Many2one(
        "product.product",
        related="company_id.sendcloud_delivery_product_id",
        readonly=False,
    )
