from odoo import models,fields
import logging
from datetime import datetime
import datetime
import json
from odoo.http import request

'''
Display List of Purchase Orders in Product Form View 
Products -> Any Product -> Purchase -> Purchase List
 
Display List of Purchase Orders in Product Form View
Products -> Any Product -> Purchase -> Purchase List
'''
class ProductTemplate(models.Model):
    _logger = logging.getLogger(__name__)
    _inherit = 'product.template'

    expected_delivery = fields.Datetime(
        string='Expected Delivery',
        compute='_compute_expected_delivery',
        readonly=True,
        store=True)

    purchase_list = fields.Many2many(
        'purchase.order.line',
        compute='_compute_purchase_order_ids',
        string='Purchase List'
    )


    '''
    computing and updating expected_delivery field
    '''

    def _compute_expected_delivery(self,scheduled_date_on_change=None):
        for product in self:
            # check if scheduled_date_on_change NOT None and rewrite expected_delivery
            if scheduled_date_on_change != None:

                # rewrite expected_delivery
                product.expected_delivery = scheduled_date_on_change

            # check if expected_delivery NOT False
            elif product.expected_delivery == False:

                # set expected_delivery when if date_expected exists into stock.move
                if product.default_code != False:
                    product.expected_delivery = self._search_date_expected('product_id.default_code', product.default_code)
                elif product.default_code == False:
                    product.expected_delivery = self._search_date_expected('description_picking', product.name)

    '''
    Search purchase order by default code and name and get expected_date field
    stock.move -> date_expected
    '''
    def _search_date_expected(self, key = None, value= None):

        stock_move_data = self.env['stock.move'].search([
                (str(key), '=', value),
            ('date_expected', '>', datetime.datetime.now()),
            ('state', 'in', ['incoming','assigned']),  # 'purchase', 'done', Filter only completed or ongoing orders
        ])

        if stock_move_data:
             return stock_move_data.mapped('date_expected')[0]

        # set color for purchase_order_ids



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
                ('state', 'in', ['purchase', 'to approve', 'sent', 'draft'])  # Filter only completed or ongoing orders
            ])

            product.purchase_list = purchase_orders




