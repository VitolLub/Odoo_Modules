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
            purchase_orders = self.env['purchase.order'].search([
                ('order_line.product_id.default_code', '=', product.default_code),
                ('state', 'in', ['purchase', 'to approve','sent','draft']),  # Filter only completed or ongoing orders
            ])

            # filtered partner_id from purchase_orders if purchase_orders.partner_id not in product.seller_ids
            purchase_orders = purchase_orders.filtered(lambda r: r.partner_id in product.seller_ids.name)

            # assign purchase_orders to product.purchase_order_ids
            product.purchase_order_ids = purchase_orders











