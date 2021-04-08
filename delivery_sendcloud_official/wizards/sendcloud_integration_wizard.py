# Copyright 2020 Onestein (<https://www.onestein.eu>)
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).

import requests
from urllib.parse import urlencode

from odoo import api, fields, models, _


class SendCloudIntegrationWizard(models.TransientModel):
    _name = "sendcloud.integration.wizard"
    _description = "SendCloud Integration Wizard"

    configuration = fields.Selection(
        [("odoo", "Odoo Integration"), ("api", "API Integration")],
        default="odoo",
        required=True,
    )

    public_key = fields.Char(
        compute="_compute_sendcloud_keys", compute_sudo=True, store=True, readonly=False
    )
    secret_key = fields.Char(
        compute="_compute_sendcloud_keys", compute_sudo=True, store=True, readonly=False
    )
    base_url = fields.Char(compute="_compute_base_url", store=True)
    integration_request_url = fields.Char(compute="_compute_integration_request_url")
    error_message = fields.Text(readonly=True)
    info_message = fields.Text(readonly=True)
    company_id = fields.Many2one('res.company', required=True, default=lambda self: self.env.company)
    is_sendcloud_test_mode = fields.Boolean(compute="_compute_is_sendcloud_test_mode")

    @api.depends("company_id.is_sendcloud_test_mode")
    def _compute_is_sendcloud_test_mode(self):
        for record in self:
            record.is_sendcloud_test_mode = record.company_id.is_sendcloud_test_mode

    @api.depends("configuration")
    def _compute_sendcloud_keys(self):
        for wizard in self:
            if wizard.configuration == "api":
                integrations = self.env.company.sendcloud_integration_ids
                integrations = integrations.filtered(lambda i: i.system == "api")
                integration = fields.first(integrations)
                wizard.public_key = (
                    integration.public_key
                    if integration.public_key
                    else wizard.public_key
                )
                wizard.secret_key = (
                    integration.secret_key
                    if integration.secret_key
                    else wizard.secret_key
                )
            else:
                wizard.public_key = wizard.public_key
                wizard.secret_key = wizard.secret_key

    @api.depends("configuration")
    def _compute_base_url(self):
        for wizard in self:
            wizard.base_url = self.env["ir.config_parameter"].get_param("web.base.url")

    def _get_odoo_connect_url(self):
        return "https://panel.sendcloud.sc/shops/odoo/connect/"

    @api.depends("configuration", "integration_request_url")
    def _compute_integration_request_url(self):
        for wizard in self:
            wizard.integration_request_url = False
            if wizard.configuration == "odoo":
                request_url = self._get_odoo_connect_url()
                Request = self.env["sendcloud.request"]
                webhook = Request._default_integration_webhook(self.env.company.id)
                querystring = urlencode(
                    {
                        "url_webshop": wizard.base_url,
                        "webhook_url": wizard.base_url + webhook,
                        "shop_name": self.env.cr.dbname
                        + " "
                        + str(self.env.company.id),
                    }
                )
                wizard.integration_request_url = "%s?%s" % (request_url, querystring)

    @api.onchange("configuration")
    def _onchange_configuration(self):
        self.error_message = False
        self.info_message = False
        if self.configuration == "api":
            self.info_message = _("When using the API integration you will only be "
                                  "able to create labels and will not sync orders")

    def check_webhook_url(self):
        self.ensure_one()
        default_webhook = self.env["sendcloud.request"]._default_integration_webhook(
            self.env.company.id
        )
        url = self.base_url + default_webhook
        try:
            resp = requests.post(url=url, json={}, timeout=10)
        except Exception as err:
            self.error_message = _("Error while checking the webhook connection.\n")
            self.error_message += "%s\n" % str(err)
            self.error_message += _("Webhook URL: %s\n" % url)
            return False
        if resp.status_code != 200:
            err_msg = _("Webhook URL: %s (error code %s)") % (
                resp.reason,
                resp.status_code,
            )
            self.error_message = _("Error while checking the webhook connection.\n")
            self.error_message += "%s\n" % err_msg
            self.error_message += "URL: %s\n" % url
            return False
        return True

    def button_update(self):
        self = self.sudo()
        integrations = self.env.company.sendcloud_integration_ids
        integrations = integrations.filtered(lambda i: i.system == self.configuration)
        if self.configuration == "api":
            integrations = integrations.filtered(
                lambda i: i.public_key == self.public_key
                and i.secret_key == self.secret_key
            )
            if not integrations:
                vals = {
                    "shop_name": "API Integration " + self.env.company.name,
                    "system": "api",
                    "public_key": self.public_key,
                    "secret_key": self.secret_key,
                    "company_id": self.env.company.id,
                }
                integrations = self.env["sendcloud.integration"].create(vals)

            integration = fields.first(integrations)
            req_integrations = integration.get_integrations()
            self.env["sendcloud.integration"].sendcloud_create_update_integrations(
                req_integrations, self.env.company
            )
        else:
            integrations = integrations.filtered(
                lambda i: not i.sendcloud_code and not i.public_key and not i.secret_key
            )
            if not integrations:
                vals = {
                    "shop_name": "API Integration " + self.env.company.name,
                    "system": "odoo",
                    "company_id": self.env.company.id,
                }
                self.env["sendcloud.integration"].create(vals)
            if not self.check_webhook_url():
                action_name = (
                    "delivery_sendcloud_official.action_sendcloud_onboarding_integration_wizard"
                )
                action = self.env.ref(action_name).read()[0]
                action["res_id"] = self.id
                return action
            return {
                "type": "ir.actions.act_url",
                "target": "self",
                "url": self.integration_request_url,
            }
