# Copyright 2021 Onestein (<https://www.onestein.nl>)
# License OPL-1 (https://www.odoo.com/documentation/14.0/legal/licenses.html#odoo-apps).

{
    "name": "SendCloud Shipping",
    "summary": "Compute shipping costs and ship with SendCloud",
    "images": ["static/description/sendcloud_cover.jpeg"],
    "category": "Operations/Inventory/Delivery",
    "version": "15.0.1.0.5",
    "author": "Onestein",
    "license": "OPL-1",
    "depends": ["delivery", "base_address_extended"],
    "data": [
        "security/ir.model.access.csv",
        "security/sendcloud_security_rule.xml",
        "data/delivery_sendcloud_data.xml",
        "data/delivery_sendcloud_cron.xml",
        "wizards/sendcloud_create_return_parcel_wizard_view.xml",
        "views/sale_order_view.xml",
        "views/stock_picking_view.xml",
        "views/stock_warehouse_view.xml",
        "views/res_partner_view.xml",
        "views/delivery_carrier_view.xml",
        "views/sendcloud_parcel_view.xml",
        "views/sendcloud_brand_view.xml",
        "views/sendcloud_carrier_view.xml",
        "views/sendcloud_return_view.xml",
        "views/sendcloud_invoice_view.xml",
        "views/sendcloud_parcel_status_view.xml",
        "views/sendcloud_sender_address_view.xml",
        "views/sendcloud_action.xml",
        "views/sendcloud_integration_view.xml",
        "views/res_config_settings_view.xml",
        "wizards/sendcloud_warehouse_address_wizard_view.xml",
        "wizards/sendcloud_cancel_shipment_confirm_wizard_view.xml",
        "wizards/sendcloud_integration_wizard_view.xml",
        "wizards/sendcloud_sync_wizard_view.xml",
        "wizards/sendcloud_sync_order_wizard_view.xml",
        "wizards/sendcloud_custom_price_details_wizard.xml",
        "views/sendcloud_onboarding_views.xml",
        "views/sendcloud_shipping_method_country_view.xml",
        "views/menu.xml",
    ],
    "assets": {
        "web.assets_common": [
            "delivery_sendcloud_official/static/src/lib/sendcloud/api.min.js",
            "delivery_sendcloud_official/static/src/js/common.js"
        ],
        "web.assets_backend": [
            "delivery_sendcloud_official/static/src/js/backend.js",
            "delivery_sendcloud_official/static/src/js/widget.js",
            "delivery_sendcloud_official/static/src/scss/backend.scss",
            "delivery_sendcloud_official/static/src/scss/widget.scss"
        ],
        "web.assets_qweb": [
            "delivery_sendcloud_official/static/src/xml/backend_service_point.xml",
        ]
    },
    "application": True,
}
