# Copyright 2020 Onestein (<https://www.onestein.eu>)
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).

from odoo import models, fields


class Website(models.Model):
    _name = "website"
    _inherit = ["website", "sendcloud.mixin"]

    sendcloud_brand_id = fields.Many2one("sendcloud.brand")
