from odoo import http,models,fields,api
import logging,sys
from datetime import datetime, timedelta
import datetime
from functools import reduce


class ProductTemplate(models.Model):
    _logger = logging.getLogger(__name__)
    _inherit = 'product.template'

    expected_delivery = fields.Datetime(
        string='Expected Delivery',
        compute='_compute_expected_delivery',
        readonly=True,
        store=True)

    '''
    computing and updating expected_delivery field
    '''

    def _compute_expected_delivery(self,scheduled_date_on_change=None):
        for product in self:
            if product.default_code != False:

                # check if scheduled_date_on_change NOT None and rewrite expected_delivery
                if scheduled_date_on_change != None:

                    # rewrite expected_delivery
                    product.expected_delivery = scheduled_date_on_change

                # check if expected_delivery NOT False
                elif product.expected_delivery == False:

                    # set expected_delivery when if date_expected exists into stock.move
                    product.expected_delivery = self._search_expected_delivery('default_code', product.default_code)


    '''
    Seacrh purchase order by default code and name and get expected_date field
    stock.move -> expected_date
    '''
    def _search_expected_delivery(self, key = None, value= None):
        stock_move_data = self.env['stock.move'].search([
                ('product_id.'+str(key), '=', value),
            ('date_expected', '>', datetime.datetime.now()),
            # ('state', 'in', ['incoming','assigned']),  # 'purchase', 'done', Filter only completed or ongoing orders
        ])

        if stock_move_data:
            return stock_move_data.mapped('date_expected')[0]





