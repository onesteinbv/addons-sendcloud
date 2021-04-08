# Copyright 2020 Onestein (<https://www.onestein.eu>)
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).

from odoo import api, models


class ChooseDeliveryCarrier(models.TransientModel):
    _inherit = "choose.delivery.carrier"

    @api.onchange("carrier_id")
    def _onchange_carrier_id(self):
        res = super()._onchange_carrier_id()
        if self.delivery_type == "sendcloud":
            vals = self._get_shipment_rate()
            if vals.get("error_message"):
                return {"error": vals["error_message"]}
        return res
