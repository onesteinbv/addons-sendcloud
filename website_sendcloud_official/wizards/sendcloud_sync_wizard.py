# Copyright 2020 Onestein (<https://www.onestein.eu>)
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).

from odoo import fields, models


class SendCloudSyncWizard(models.TransientModel):
    _inherit = "sendcloud.sync.wizard"

    publish_all_shipping_methods = fields.Boolean()

    def button_sync(self):
        ctx = self.env.context.copy()
        if self.publish_all_shipping_methods:
            ctx["sendcloud_publish_all_shipping_methods"] = True
        return super(SendCloudSyncWizard, self.with_context(ctx)).button_sync()
