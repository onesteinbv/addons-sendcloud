# Copyright 2020 Onestein (<https://www.onestein.eu>)
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).

{
    "name": "SendCloud eCommerce",
    "summary": "Integrate your web shop with SendCloud",
    "images": ["static/description/sendcloud_cover.jpeg"],
    "category": "Website/Website",
    "version": "14.0.1.0.0",
    "development_status": "Beta",
    "author": "Onestein",
    "license": "LGPL-3",
    "depends": ["website_sale_delivery", "delivery_sendcloud_official"],
    "data": [
        "security/ir.model.access.csv",
        "templates/assets.xml",
        "templates/website_sale_delivery.xml",
        "views/website_view.xml",
        "views/res_config_settings_view.xml",
        "wizards/sendcloud_sync_wizard_view.xml",
        "wizards/sendcloud_website_brand_wizard_view.xml",
        "views/sendcloud_onboarding_views.xml",
        "views/menu.xml",
    ],
    "application": True,
}
