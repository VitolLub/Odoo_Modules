from odoo import models,fields
import logging
from datetime import datetime
import datetime

'''
Adding expected_delivery field into product.product model
Products -> Variant Product
'''
class ProductProduct(models.Model):
    _logger = logging.getLogger(__name__)
    _inherit = 'product.product'

    expected_delivery = fields.Datetime(
        string='Expected Delivery',
        compute='_compute_expected_delivery_for_product',
        readonly=True,
        store=True)

    '''
    computing and updating expected_delivery field into product.product model
    '''

    def _compute_expected_delivery_for_product(self,scheduled_date_on_change=None):
        for product_product in self:

            # set expected_delivery when if date_expected exists into stock.move

            # check if scheduled_date_on_change NOT None and rewrite expected_delivery
            if scheduled_date_on_change != None:

                # rewrite expected_delivery
                product_product.expected_delivery = scheduled_date_on_change

            # check if expected_delivery NOT False
            elif product_product.expected_delivery == False:

                # set expected_delivery when if date_expected exists into stock.move
                product_product.expected_delivery = self._search_date_expected(product_product.id)


    '''
    Seacrh purchase order by default code and name and get expected_date field
    stock.move -> expected_date
    '''
    def _search_date_expected(self, product_id):

        # search data from stock.move model by current product id
        stock_move_data = self.env['stock.move'].search([('product_id.id', '=', product_id),
                                                         ('date_expected', '>', datetime.datetime.now()),
                                                         ('state', 'in', ['purchase', 'to approve', 'sent', 'draft']), #,'purchase', 'done'
                                                         ])
        if stock_move_data:
            return stock_move_data.mapped('date_expected')[0]







