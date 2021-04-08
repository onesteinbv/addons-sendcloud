# Copyright 2020 Onestein (<https://www.onestein.eu>)
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).

from odoo import api, models, fields


class SendCloudCarrier(models.Model):
    _name = "sendcloud.carrier"
    _description = "SendCloud Carrier"

    name = fields.Char(required=True)
    sendcloud_code = fields.Char(required=True)

    @api.model
    def _create_update_carriers(self, retrieved_carriers):
        all_carriers = self.search([])
        existing_carriers = all_carriers.mapped("sendcloud_code")
        to_add_carriers = set(retrieved_carriers) - set(existing_carriers)
        new_carrier_vals_list = []
        for new_carrier in list(to_add_carriers):
            vals = {"sendcloud_code": new_carrier, "name": new_carrier.upper()}
            new_carrier_vals_list.append(vals)
        self.create(new_carrier_vals_list)
