# Copyright 2021 Onestein (<https://www.onestein.nl>)
# License OPL-1 (https://www.odoo.com/documentation/14.0/legal/licenses.html#odoo-apps).

from odoo import api, models


class SendcloudParcel(models.Model):
    _inherit = "sendcloud.parcel"

    @api.depends("company_id")
    def _compute_brand_id(self):
        res = super()._compute_brand_id()
        for parcel in self:
            brand = parcel.picking_id.sale_id.website_id.sendcloud_brand_id
            if brand:
                parcel.brand_id = brand
        return res
