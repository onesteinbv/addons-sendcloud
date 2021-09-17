# Copyright 2021 Onestein (<https://www.onestein.eu>)
# License OPL-1 (https://www.odoo.com/documentation/14.0/legal/licenses.html#odoo-apps).

from odoo import models, fields


class SendCloudShippingMethodCountryCustom(models.Model):
    _name = "sendcloud.shipping.method.country.custom"
    _description = "SendCloud Shipping Method Country Custom"

    iso_2 = fields.Char(required=True)
    price = fields.Float()
    method_code = fields.Integer(required=True)
    company_id = fields.Many2one("res.company", required=True)
