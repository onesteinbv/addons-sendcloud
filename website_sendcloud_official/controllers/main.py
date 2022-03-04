# Copyright 2021 Onestein (<https://www.onestein.nl>)
# License OPL-1 (https://www.odoo.com/documentation/14.0/legal/licenses.html#odoo-apps).

import logging

from odoo import http, _
from odoo.http import request
from odoo.addons.website_sale_delivery.controllers.main import WebsiteSaleDelivery

_logger = logging.getLogger(__name__)


class WebsiteSaleSendcloudDelivery(WebsiteSaleDelivery):

    def _update_website_sale_delivery_return(self, order, **post):
        res = super()._update_website_sale_delivery_return(order, **post)
        if order and post.get('carrier_id'):
            carrier_id = int(post['carrier_id'])
            carrier = request.env['delivery.carrier'].sudo().browse(carrier_id)
            if carrier and carrier.delivery_type == 'sendcloud':
                res.update(order.sendcloud_sale_delivery_data(carrier))
        return res

    @http.route(
        ["/shop/sendcloud_update_service_point_address"],
        type="json",
        auth="public",
        methods=["POST"],
        website=True,
        csrf=False,
    )
    def sendcloud_update_service_point_address(self, **post):
        if post.get("order_id"):
            order = request.env["sale.order"].sudo().browse(post.get("order_id"))
            order.write(
                {
                    "sendcloud_service_point_address": post.get(
                        "sendcloud_service_point_address"
                    )
                }
            )
        return True

    # TODO do we need this?
    # @http.route('/shop/payment/validate', type='http', auth="public", website=True, sitemap=False)
    # def payment_validate(self, transaction_id=None, sale_order_id=None, **post):
    #     """ Method that should be called by the server when receiving an update
    #     for a transaction.
    #     """
    #     if sale_order_id is None:
    #         order = request.website.sale_get_order()
    #     else:
    #         order = request.env['sale.order'].sudo().browse(sale_order_id)
    #         assert order.id == request.session.get('sale_last_order_id')
    #
    #     # raise in case service point is required but not set
    #     carrier = order.carrier_id
    #     if carrier.sendcloud_service_point_input == "required":
    #         if not order.sendcloud_service_point_address:
    #             raise ValidationError(_("Sendcloud Service Point is required."))
    #
    #     return super().payment_validate(transaction_id, sale_order_id, **post)
