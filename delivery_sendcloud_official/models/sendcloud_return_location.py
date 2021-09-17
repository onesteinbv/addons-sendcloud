# Copyright 2021 Onestein (<https://www.onestein.nl>)
# License OPL-1 (https://www.odoo.com/documentation/14.0/legal/licenses.html#odoo-apps).

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
