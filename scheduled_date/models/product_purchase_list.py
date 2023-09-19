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
        # if
        for product in self:
            # search data from purchase.order model
            product_product = self.env['product.product'].search([('product_tmpl_id', '=', product.id)])

            purchase_orders = self.env['purchase.order'].search([
                ('order_line.product_id', 'in', product_product.ids),
                ('state', 'in', ['purchase', 'to approve','sent','draft']),  # Filter only completed or ongoing orders
            ])

            # assign purchase_orders to product.purchase_order_ids
            product.purchase_order_ids = purchase_orders











