# Copyright 2020 Onestein (<https://www.onestein.eu>)
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).

from odoo import api, fields, models


class SendcloudOnboardingMixin(models.AbstractModel):
    _inherit = "sendcloud.onboarding.mixin"

    sendcloud_onboarding_website_brand_state = fields.Selection(
        [("not_done", "Not done"), ("just_done", "Just done"), ("done", "Done")],
        string="State of the configuration website brand step",
        default="not_done",
    )

    def _sendcloud_onboarding_state_steps(self):
        res = super()._sendcloud_onboarding_state_steps()
        res.append("sendcloud_onboarding_website_brand_state")
        return res

    @api.model
    def action_open_sendcloud_onboarding_website_brand(self):
        """ Called by onboarding panel."""
        action_name = "website_sendcloud_official.action_sendcloud_onboarding_website_wizard"
        return self.env.ref(action_name).read()[0]
