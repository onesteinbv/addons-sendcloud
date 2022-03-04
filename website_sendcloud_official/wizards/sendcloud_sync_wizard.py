# Copyright 2021 Onestein (<https://www.onestein.nl>)
# License OPL-1 (https://www.odoo.com/documentation/14.0/legal/licenses.html#odoo-apps).

from odoo import fields, models


class SendcloudSyncWizard(models.TransientModel):
    _inherit = "sendcloud.sync.wizard"

    publish_all_shipping_methods = fields.Boolean()

    def button_sync(self):
        ctx = self.env.context.copy()
        if self.publish_all_shipping_methods:
            ctx["sendcloud_publish_all_shipping_methods"] = True
        return super(SendcloudSyncWizard, self.with_context(ctx)).button_sync()
