# Copyright 2020 Onestein (<https://www.onestein.eu>)
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).

from odoo import api, models, fields


class SendCloudShippingMethodCountry(models.Model):
    _name = "sendcloud.shipping.method.country"
    _description = "SendCloud Shipping Method Country"

    name = fields.Char(compute="_compute_country_id")
    country_id = fields.Many2one(
        "res.country", compute="_compute_country_id", string="To Country"
    )
    sendcloud_code = fields.Integer(required=True)
    iso_2 = fields.Char(required=True)
    iso_3 = fields.Char()
    from_name = fields.Char(compute="_compute_country_id")
    from_country_id = fields.Many2one("res.country", compute="_compute_country_id")
    from_iso_2 = fields.Char()
    from_iso_3 = fields.Char()
    price = fields.Float()
    method_code = fields.Integer(required=True)
    sendcloud_is_return = fields.Boolean()
    company_id = fields.Many2one("res.company", required=True)

    @api.depends("iso_2", "from_iso_2")
    def _compute_country_id(self):
        iso_2_list = self.mapped("iso_2")
        from_iso_2_list = self.mapped("from_iso_2")
        all_countries = self.env["res.country"].search(
            [("code", "in", iso_2_list + from_iso_2_list)]
        )
        for record in self:
            to_countries = all_countries.filtered(lambda c: c.code == record.iso_2)
            record.country_id = fields.first(to_countries)
            record.name = record.country_id.name
            from_countries = all_countries.filtered(
                lambda c: c.code == record.from_iso_2
            )
            record.from_country_id = fields.first(from_countries)
            record.from_name = record.from_country_id.name
