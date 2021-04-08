# Copyright 2020 Onestein (<https://www.onestein.eu>)
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).

import base64

from odoo import api, models, fields, _
from odoo.exceptions import UserError
from odoo.tools.safe_eval import safe_eval


class SendCloudParcel(models.Model):
    _inherit = "sendcloud.parcel"

    def _generate_parcel_labels(self):
        res = super()._generate_parcel_labels()
        existing_attachments = self.mapped("picking_id.shipping_label_ids.label_ids.document_id")
        for parcel in self.filtered(lambda p: p.attachment_id):
            if parcel.attachment_id not in existing_attachments:
                label_attachments = [
                    (0, 0, {'document_id': parcel.attachment_id.id})
                ]
                shipping_label_vals = {
                    'carrier_id': parcel.picking_id.carrier_id.id,
                    'picking_id': parcel.picking_id.id,
                    'tracking_numbers': parcel.picking_id.carrier_tracking_ref,
                    'label_ids': label_attachments,
                    'label_status': 'active',
                }
                self.env['shipping.label'].create(shipping_label_vals)

        return res
