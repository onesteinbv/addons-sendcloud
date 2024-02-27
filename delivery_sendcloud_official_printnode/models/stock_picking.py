# Copyright 2024 Onestein (<https://www.onestein.nl>)
# License OPL-1 (https://www.odoo.com/documentation/16.0/legal/licenses.html#odoo-apps).

from odoo import models


class StockPicking(models.Model):
    _inherit = "stock.picking"

    def action_multi_create_sendcloud_labels_print(self):
        self.action_multi_create_sendcloud_labels()
        self.mapped('shipping_label_ids').print_via_printnode()
