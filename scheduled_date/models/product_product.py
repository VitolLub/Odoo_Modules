from odoo import http,models,fields,api
import logging,sys
from datetime import datetime, timedelta
import datetime


class ProductTemplate(models.Model):
    _logger = logging.getLogger(__name__)
    _inherit = 'product.product'

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

            # set expected_delivery when if date_expected exists into stock.move
            # datetine empty
            self._logger.info("product_data: %s", product.id)
            self._logger.info("product_data: %s", product.default_code)
            self._logger.info("product_data: %s", product.name)
            self._logger.info("product_data: %s", product.lst_price)
            self._logger.info("product_data: %s", product.standard_price)
            self._logger.info("++++++++++++++++++++++++++++")
            product.expected_delivery = self._search_date_expected(product.id)


    '''
    Seacrh purchase order by default code and name and get expected_date field
    stock.move -> expected_date
    '''
    def _search_date_expected(self, product_id):
        # search data from stock.move model by current product id
        stock_move_data = self.env['stock.move'].search([('product_id.id', '=', product_id)])
        self._logger.info(stock_move_data)
        if stock_move_data:
            self._logger.info("stock_move_data.mapped('date_expected') %s", stock_move_data.mapped('date_expected')[0])
        self._logger.info("=====================================")

    # stock_move_data = self.env['stock.move'].search([
    #         ('product_id.'+str(key), '=', value),
    #     ('date_expected', '>', datetime.datetime.now()),
    #     ('state', 'in', ['incoming','assigned']),  # 'purchase', 'done', Filter only completed or ongoing orders
    # ])
    #
    # if stock_move_data:
    #     return stock_move_data.mapped('date_expected')[0]





