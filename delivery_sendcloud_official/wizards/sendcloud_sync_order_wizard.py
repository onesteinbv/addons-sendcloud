# Copyright 2021 Onestein (<https://www.onestein.nl>)
# License OPL-1 (https://www.odoo.com/documentation/14.0/legal/licenses.html#odoo-apps).

from dateutil.relativedelta import relativedelta

from odoo import fields, models, _
from odoo.exceptions import UserError


class SendCloudSyncOrderWizard(models.TransientModel):
    _name = "sendcloud.sync.order.wizard"
    _description = "SendCloud Sync Order Wizard"

    sync_from_date = fields.Date(
        default=lambda self: fields.Date.context_today(self) + relativedelta(days=-30),
        required=True,
    )

    def button_sync(self):
        company = self.env.company
        integration = company.sendcloud_default_integration_id
        if not integration:
            raise UserError(
                _("No SendCloud integrations found. Setup an integration first.")
            )

        pickings = self.env["stock.picking"].search([
            ("delivery_type", "=", "sendcloud"),
            ("picking_type_code", "=", "outgoing"),
            ("sale_id", "!=", False),
            ("date", ">=", self.sync_from_date),
        ])
        if not pickings:
            raise UserError(
                _("There are no outgoing shipments set with SendCloud shipping method.")
            )
        pickings._sync_picking_to_sendcloud()
