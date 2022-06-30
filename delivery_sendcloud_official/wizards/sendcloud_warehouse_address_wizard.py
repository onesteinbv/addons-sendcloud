# Copyright 2021 Onestein (<https://www.onestein.nl>)
# License OPL-1 (https://www.odoo.com/documentation/14.0/legal/licenses.html#odoo-apps).

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class SendcloudWarehouseAddressWizard(models.TransientModel):
    _name = "sendcloud.warehouse.address.wizard"
    _description = "Sendcloud Warehouse Address Wizard"

    def _default_warehouse_ids(self):
        warehouses = self.env["stock.warehouse"].search(
            [("company_id", "=", self.env.company.id)]
        )
        lines_dict = [{
            "warehouse_id": warehouse.id,
            "sencloud_sender_address_id": warehouse.partner_id.sencloud_sender_address_id.id,
        } for warehouse in warehouses]
        return self.env["sendcloud.change.warehouse.address.wizard"].create(lines_dict)

    warehouse_ids = fields.One2many(
        "sendcloud.change.warehouse.address.wizard",
        "wizard_id",
        string="Warehouses",
        default=_default_warehouse_ids,
    )

    def button_update(self):
        self.ensure_one()
        self._check_line_countries_consistence()
        for line in self.warehouse_ids:
            warehouse = line.warehouse_id
            warehouse_adress = warehouse.partner_id
            warehouse_adress.sencloud_sender_address_id = (
                line.sencloud_sender_address_id
            )

        company = self.env.company
        company.set_onboarding_step_done("sendcloud_onboarding_warehouse_address_state")

    def _check_line_countries_consistence(self):
        self.ensure_one()
        err_msg = ""
        for line in self.warehouse_ids.filtered(
                lambda warehouse: warehouse.sencloud_sender_address_id
        ):
            if line.warehouse_country_code != line.sencloud_sender_address_country_code:
                err_msg += "\n%s: %s - %s: %s" % (
                    line.warehouse_id.name,
                    line.warehouse_country_code,
                    line.sencloud_sender_address_id.company_name,
                    line.sencloud_sender_address_country_code,
                )
        if err_msg:
            raise ValidationError(_("Inconsistent countries:") + err_msg)


class SendcloudChangeWarehouseAddressWizard(models.TransientModel):
    _name = "sendcloud.change.warehouse.address.wizard"
    _description = "Warehouse, Change Address Wizard"

    wizard_id = fields.Many2one(
        "sendcloud.warehouse.address.wizard", ondelete="cascade"
    )
    warehouse_id = fields.Many2one(
        "stock.warehouse", required=True, readonly=True, ondelete="cascade"
    )
    warehouse_country_code = fields.Char(
        related="warehouse_id.partner_id.country_id.code"
    )
    sencloud_sender_address_id = fields.Many2one(
        "sendcloud.sender.address",
        compute="_compute_sencloud_sender_address_id",
        readonly=False,
        store=True,
    )
    sencloud_sender_address_country_code = fields.Char(
        related="sencloud_sender_address_id.country"
    )

    @api.depends("warehouse_id.partner_id.sencloud_sender_address_id")
    def _compute_sencloud_sender_address_id(self):
        for record in self:
            record.sencloud_sender_address_id = (
                record.warehouse_id.partner_id.sencloud_sender_address_id
            )
