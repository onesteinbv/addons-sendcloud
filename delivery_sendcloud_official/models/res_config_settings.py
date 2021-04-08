# Copyright 2020 Onestein (<https://www.onestein.eu>)
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).

from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    is_sendcloud_test_mode = fields.Boolean(
        related="company_id.is_sendcloud_test_mode",
        readonly=False,
    )
