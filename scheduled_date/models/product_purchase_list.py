from odoo import http,models,fields,api
import logging,sys
from datetime import datetime, timedelta
import datetime


class ProductPurchaseList(models.Model):
    _logger = logging.getLogger(__name__)

    _inherit = 'product.template'

    purchase_order_ids = fields.Many2many(
        'purchase.order',
        string='Purchase Orders',
        compute='_compute_purchase_order_ids',
        store=True,
    )

    def _compute_purchase_order_ids(self):
        for product in self:
            purchase_orders = self.env['purchase.order'].search([
                ('order_line.product_id.default_code', '=', product.default_code),
            ])

            # select purchase order data
            product.purchase_order_ids = purchase_orders











