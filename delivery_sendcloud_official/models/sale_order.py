# Copyright 2021 Onestein (<https://www.onestein.nl>)
# License OPL-1 (https://www.odoo.com/documentation/15.0/legal/licenses.html#odoo-apps).

import logging

from odoo import api, fields, models

_logger = logging.getLogger(__name__)


class SaleOrder(models.Model):
    _name = "sale.order"
    _inherit = ["sale.order", "sendcloud.mixin"]

    is_sendcloud_delivery_type = fields.Boolean(
        compute="_compute_is_sendcloud_delivery_type", store=True
    )
    sendcloud_service_point_required = fields.Boolean(
        related="carrier_id.sendcloud_service_point_required"
    )
    sendcloud_service_point_address = fields.Text(copy=False)
    sendcloud_order_weight = fields.Float(compute="_compute_sendcloud_order_weight")
    sendcloud_customs_shipment_type = fields.Selection(
        selection="_get_sendcloud_customs_shipment_type",
        default=lambda self: self._default_get_sendcloud_customs_shipment_type(),
    )
    sendcloud_order_code = fields.Char(index=True)

    @api.depends("carrier_id.delivery_type")
    def _compute_is_sendcloud_delivery_type(self):
        for order in self:
            is_sendcloud = order.carrier_id.delivery_type == "sendcloud"
            order.is_sendcloud_delivery_type = is_sendcloud

    def _sendcloud_convert_price_in_euro(self, price):
        self.ensure_one()
        currency = self.currency_id
        if currency.name == "EUR":
            return price
        euro_curr = self.env["res.currency"].search([("name", "=", "EUR")], limit=1)
        if euro_curr:
            price = euro_curr._convert(
                price, currency, self.company_id, self.date_order
            )
        return price

    @api.depends(
        "order_line.product_id.weight",
        "order_line.product_qty",
        "order_line.display_type",
    )
    def _compute_sendcloud_order_weight(self):
        for order in self:
            lines = order.order_line.filtered(
                lambda l: not l.display_type and l.product_id.weight
            )
            weight = sum(
                [(line.product_id.weight * line.product_qty) for line in lines]
            )
            order.sendcloud_order_weight = self._sendcloud_convert_weight_to_kg(weight)

    def get_sendcloud_details(self):
        self.ensure_one()
        res = {}
        if (
            self.carrier_id.delivery_type == "sendcloud"
            and self.sendcloud_service_point_required
        ):
            if self.env.context.get("selected_partner_id"):
                selected_partner_id = self.env.context["selected_partner_id"]
                partner = self.env["res.partner"].browse(selected_partner_id)
            else:
                partner = self.partner_shipping_id or self.partner_id
            vals = {
                "key": self.sudo().carrier_id.sendcloud_integration_id.public_key,
                "country_code": partner.country_id.code or "",
                "postcode": partner.zip or "",
                "carrier_name": [self.carrier_id.sendcloud_carrier or ""],
            }
            res.update(vals)
        return res

    def action_cancel(self):
        to_delete_shipments = self.picking_ids.to_delete_sendcloud_pickings()
        res = super().action_cancel()
        self.env["stock.picking"].delete_sendcloud_pickings(to_delete_shipments)
        return res

    def unlink(self):
        to_delete_shipments = self.picking_ids.to_delete_sendcloud_pickings()
        res = super().unlink()
        self.env["stock.picking"].delete_sendcloud_pickings(to_delete_shipments)
        return res

    def _sync_sale_order_to_sendcloud(self):
        for order in self:
            order.picking_ids._sync_picking_to_sendcloud()

    def button_delete_sendcloud_order(self):
        self.ensure_one()
        to_delete_shipments = self.picking_ids.to_delete_sendcloud_pickings()
        self.env["stock.picking"].delete_sendcloud_pickings(to_delete_shipments)

    def button_to_sendcloud_sync(self):
        self.ensure_one()
        if self.carrier_id.delivery_type != "sendcloud":
            return
        if not self.carrier_id.sendcloud_integration_id:
            return
        if self.state != "cancel":
            self._sync_sale_order_to_sendcloud()

    def _action_confirm(self):
        res = super()._action_confirm()
        pickings = self.mapped("picking_ids")
        to_sync = pickings.filtered(lambda p: p.carrier_id.sendcloud_integration_id)
        to_sync._sync_picking_to_sendcloud()
        return res

    def _create_delivery_line(self, carrier, price_unit):
        line = super()._create_delivery_line(carrier, price_unit)
        sendcloud_specific_product = self.env.context.get("sendcloud_country_specific_product")
        if sendcloud_specific_product:
            line.product_id = sendcloud_specific_product
        return line

    def _sendcloud_order_invoice(self):
        """ When shipping outside of EU, an invoice number must be entered in Sendcloud.
        This method gets out invoices of the sale order.
        In case not any invoice is present and setting "Sendcloud_auto_create_invoice"
        is enabled, create a 100% down-payment invoice automatically.
        """
        self.ensure_one()
        out_invoices = self.invoice_ids.filtered(
            lambda i: i.move_type == "out_invoice" and i.state == "posted")

        # sendcloud_auto_create_invoice is set
        if self.company_id.sendcloud_auto_create_invoice:
            # If shipping to outside the EU and not any invoice was posted
            if not out_invoices and not self.partner_id.sendcloud_is_in_eu:
                downpayment_wizard = self.env['sale.advance.payment.inv']\
                    .with_context({
                        'active_model': 'sale.order',
                        'active_ids': [self.id],
                        'active_id': self.id,
                    }).create({
                        'advance_payment_method': 'percentage',
                        'amount': 100,
                    })
                downpayment_wizard.create_invoices()
                self.invoice_ids.action_post()
                out_invoices = self.invoice_ids

        return out_invoices
