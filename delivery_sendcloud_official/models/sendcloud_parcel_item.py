# Copyright 2021 Onestein (<https://www.onestein.nl>)
# License OPL-1 (https://www.odoo.com/documentation/14.0/legal/licenses.html#odoo-apps).

from odoo import api, models, fields


class SendCloudParcelItem(models.Model):
    _name = "sendcloud.parcel.item"
    _description = "SendCloud Parcel Items"
    _rec_name = "description"

    description = fields.Char(required=True)
    quantity = fields.Integer()
    weight = fields.Float()
    value = fields.Float()
    hs_code = fields.Char()
    origin_country = fields.Char()
    product_id = fields.Char()
    properties = fields.Char()
    sku = fields.Char()
    return_reason = fields.Char()
    return_message = fields.Char()
    parcel_id = fields.Many2one("sendcloud.parcel", ondelete="cascade")
