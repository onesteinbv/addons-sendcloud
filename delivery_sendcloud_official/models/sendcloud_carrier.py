# Copyright 2021 Onestein (<https://www.onestein.nl>)
# License OPL-1 (https://www.odoo.com/documentation/14.0/legal/licenses.html#odoo-apps).

from odoo import api, models, fields


class SendcloudCarrier(models.Model):
    _name = "sendcloud.carrier"
    _description = "Sendcloud Carrier"

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
