# Copyright 2021 Onestein (<https://www.onestein.nl>)
# License OPL-1 (https://www.odoo.com/documentation/16.0/legal/licenses.html#odoo-apps).

{
    "name": "Sendcloud eCommerce",
    "summary": "Integrate your web shop with Sendcloud",
    "images": ["static/description/sendcloud_cover.jpeg"],
    "category": "Website/Website",
    "version": "16.0.1.0.0",
    "author": "Onestein",
    "license": "OPL-1",
    "depends": ["website_sale_delivery", "delivery_sendcloud_official"],
    "data": [
        "security/ir.model.access.csv",
        "templates/website_sale_delivery.xml",
        "views/website_view.xml",
        "views/res_config_settings_view.xml",
        "wizards/sendcloud_sync_wizard_view.xml",
        "wizards/sendcloud_website_brand_wizard_view.xml",
        "views/sendcloud_onboarding_views.xml",
        "views/menu.xml",
    ],
    "assets": {
        "web.assets_frontend": [
            "website_sendcloud_official/static/src/js/*",
            "website_sendcloud_official/static/src/xml/*",
        ]
    },
    "application": True,
}
