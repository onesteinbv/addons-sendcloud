# Copyright 2020 Onestein (<https://www.onestein.eu>)
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).

from odoo import models, fields


class SendCloudReturn(models.Model):
    _name = "sendcloud.return.location"
    _description = "SendCloud Return Location"

    name = fields.Char()
    sendcloud_code = fields.Integer(required=True)
    country_name = fields.Char()
    company_name = fields.Char()
    address_1 = fields.Char()
    address_2 = fields.Char()
    house_number = fields.Char()
    city = fields.Char()
    postal_code = fields.Char()
    senderaddress_labels = fields.Text(default="[]")
    brand_id = fields.Many2one("sendcloud.brand")
