# Copyright 2021 Onestein (<https://www.onestein.nl>)
# License OPL-1 (https://www.odoo.com/documentation/14.0/legal/licenses.html#odoo-apps).

from odoo import fields, models


class ResPartner(models.Model):
    _inherit = "res.partner"

    sencloud_sender_address_id = fields.Many2one("sendcloud.sender.address")
