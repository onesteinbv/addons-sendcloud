# Copyright 2021 Onestein (<https://www.onestein.nl>)
# License OPL-1 (https://www.odoo.com/documentation/15.0/legal/licenses.html#odoo-apps).

from odoo import api, fields, models


class ResPartner(models.Model):
    _inherit = "res.partner"

    sencloud_sender_address_id = fields.Many2one(
        comodel_name="sendcloud.sender.address",
        string="Sendcloud Sender Address"
    )
    sendcloud_is_in_eu = fields.Boolean(
        compute="_compute_sendcloud_is_in_eu",
        string="Is in EU",
    )

    @api.depends("country_id.code")
    def _compute_sendcloud_is_in_eu(self):
        europe_codes = self.env.ref("base.europe").country_ids.mapped("code")
        for partner in self:
            partner.sendcloud_is_in_eu = partner.country_id.code in europe_codes
