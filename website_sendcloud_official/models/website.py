# Copyright 2021 Onestein (<https://www.onestein.nl>)
# License OPL-1 (https://www.odoo.com/documentation/14.0/legal/licenses.html#odoo-apps).

from odoo import models, fields


class Website(models.Model):
    _name = "website"
    _inherit = ["website", "sendcloud.mixin"]

    sendcloud_brand_id = fields.Many2one("sendcloud.brand")
