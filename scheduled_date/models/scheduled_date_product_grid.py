from odoo import http,models,fields,api
import logging,sys
from datetime import datetime, timedelta
import datetime
from functools import reduce

class PurchaseOrderInherited(models.Model):
    _logger = logging.getLogger(__name__)
    _inherit = 'purchase.order'

    '''
    Update expected_delivery field when scheduled_date is changed
    '''
    @api.onchange('date_planned')
    def _onchange_scheduled_date(self):

        for order in self:
            self._logger.info(f'purchase order {order}')
            if order.date_planned:
                self._logger.info(f'purchase order {order.date_planned}')
                product = order.product_id.product_tmpl_id
                product._compute_expected_delivery(order.date_planned)

class StockPickingInherited(models.Model):
    _logger = logging.getLogger(__name__)
    _inherit = 'stock.picking'


    '''
    Update expected_delivery field when scheduled_date is changed
    '''
    @api.onchange('scheduled_date')
    def _onchange_scheduled_date(self):

        for picking in self:
            self._logger.info(f'scheduled_date {picking}')
            if picking.scheduled_date:
                self._logger.info(f'scheduled_date {picking.scheduled_date}')
                for move_line in picking.move_line_ids:
                    product = move_line.product_id.product_tmpl_id
                    self._logger.info(f'scheduled_date {product}')
                    product._compute_expected_delivery(picking.scheduled_date)

class ScheduledDateProductGrid(models.Model):
    _logger = logging.getLogger(__name__)
    _inherit = 'product.template'
    scheduled_date = fields.Many2one('stock.picking', string="stock.picking", required=True)

    expected_delivery = fields.Datetime(
        string='Expected Delivery',
        compute='_compute_expected_delivery',
        readonly=True,
        store=True)

    '''
    update purchase_order 
    date_planned field
    '''

    @api.onchange('scheduled_date')
    @api.depends('scheduled_date')
    def _compute_expected_delivery(self,scheduled_date_on_change=None):
        for product in self:
            if product.default_code != False:
                matching_orders = self._search_expected_delivery('default_code', product.default_code)

                scheduled_date = matching_orders.mapped('picking_id.scheduled_date')

                # get biggest date from array [datetime.datetime(2023, 8, 29, 12, 45, 33), datetime.datetime(2023, 8, 29, 12, 45, 34)]
                if len(scheduled_date)!= 0:
                    scheduled_date = reduce(lambda x, y: x if x > y else y, scheduled_date, datetime.datetime.min)

                    # get current date
                    now_date = datetime.datetime.now()

                    # check if expected_delivery NOT False and scheduled_date is bigger than now_date
                    if product.expected_delivery == False and scheduled_date != None and scheduled_date > now_date:

                        # set expected_delivery to scheduled_date
                        product.expected_delivery = scheduled_date

                    elif scheduled_date != None:
                        # rewrite expected_delivery to scheduled_date
                        product.expected_delivery = scheduled_date_on_change

    '''
    Seacrh purchase order by default code and name
    '''
    def _search_expected_delivery(self, key = None, value= None):
        self._logger.info(f'matching_orders {key} and {value}')
        matching_orders = self.env['stock.move.line'].search([
                ('product_id.'+str(key), '=', value),
            ('state', 'in', ['incoming','assigned']),  # 'purchase', 'done', Filter only completed or ongoing orders
        ])
        return matching_orders





