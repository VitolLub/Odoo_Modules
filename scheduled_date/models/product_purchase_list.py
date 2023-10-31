from odoo import http,models,fields,api
import logging
from odoo.http import request
import json

'''
Display List of Purchase Orders in Product Form View 
Products -> Any Product -> Purchase -> Purchase List
'''
class ProductPurchaseList(models.Model):
    _logger = logging.getLogger(__name__)
    _inherit = 'product.template'


    # set color for purchase_order_ids
    purchase_list = fields.Many2many(
        'purchase.order.line',
        compute='_compute_purchase_order_ids',
        string='Purchase List',
        )

    def _compute_purchase_order_ids(self):

        for product in self:
            '''
            in current product data we can get only product ID bot variant ID
            We need to get variant ID if user selected product into Products -> Product Variants
            if user selected product in Products -> Products when we just get product ID 
            All depents from view:
                Products -> Products = Display all purchase orders for selected product
                Products -> Product Variants = Display purchase orders related to selected variant
            '''
            current_url_data = json.loads(request.httprequest.data)
            if current_url_data['params']['model'] == 'product.template':
                product_id = product.product_variant_ids.ids
            else:
                product_id = current_url_data['params']['args'][0]

            # selected orders from purchase.order.line based on current product ID or variant ID
            purchase_orders = self.env['purchase.order.line'].search([
                ('product_id', 'in', product_id),
                ('state', 'in', ['purchase', 'to approve']), #, 'sent', 'draft'
            ])

            # assign purchase orders to purchase_list field
            product.purchase_list = purchase_orders


