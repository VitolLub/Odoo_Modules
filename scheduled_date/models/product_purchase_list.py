from odoo import http,models,fields,api
import logging
from odoo.http import request
import json

class ScheduledDate(models.Model):
    _inherit= 'purchase.order.line'

    '''
    Created new field necessary to task VIPODOO-1
    '''

    order_id_test = fields.Many2one('purchase.order', string='Purchase Order', related='order_id')
    date_planned = fields.Datetime(related='order_id_test.date_planned', string='Scheduled Date')
    source_document = fields.Char(related='order_id_test.origin', string='Source Document')
    res_users = fields.Many2one('res.users', related='order_id_test.user_id', string='Buyer')
    buyer = fields.Char(related='res_users.name', string='Buyer')




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
                ('state', 'in', ['purchase', 'to approve', 'sent', 'draft']),
            ])

            # assign purchase orders to purchase_list field
            product.purchase_list = purchase_orders


