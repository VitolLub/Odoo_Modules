from odoo import http,models,fields,api
import logging,sys
from datetime import datetime, timedelta
import datetime

class ProductPurchaseList(models.Model):
    _logger = logging.getLogger(__name__)

    _inherit = 'purchase.order'
    _name = 'product_purchase_list'

    product_purchase_list = 'dfsd'
    '''
    get a list of purchase orders when product default_code is equal to default_code from purchase order line
    '''

    @api.model
    def _get_purchase_orders(self, default_code=None):
        purchase_orders = self.env['purchase.order'].search([
            ('order_line.product_id.default_code', '=', default_code),
            ('state', 'in', ['purchase', 'done']),  # Filter only completed orders
        ])

        return purchase_orders