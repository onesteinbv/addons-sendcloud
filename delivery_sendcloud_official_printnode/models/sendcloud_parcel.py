# Copyright 2021 Onestein (<https://www.onestein.nl>)
# License OPL-1 (https://www.odoo.com/documentation/16.0/legal/licenses.html#odoo-apps).

import base64

from odoo import api, models, fields, _


class SendcloudParcel(models.Model):
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
