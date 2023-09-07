from odoo import http,models,fields,api
import logging,sys
from datetime import datetime, timedelta
import datetime
from functools import reduce


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
                expected_delivery_dates = self._search_expected_delivery('default_code', product.default_code)

                # check if expected_delivery NOT False and scheduled_date is bigger than now_date
                if product.expected_delivery == False:

                    # set expected_delivery to scheduled_date
                    product.expected_delivery = expected_delivery_dates

                elif scheduled_date_on_change != None:

                    # rewrite expected_delivery to scheduled_date
                    product.expected_delivery = scheduled_date_on_change

    '''
    Seacrh purchase order by default code and name
    '''
    def _search_expected_delivery(self, key = None, value= None):
        self._logger.info(f'matching_orders {key} and {value}')
        date = datetime.datetime.now()
        matching_orders = self.env['purchase.order.line'].search([
                ('product_id.'+str(key), '=', value),
            ('order_id.date_planned', '>', date),
            ('state', 'in', ['incoming','assigned']),  # 'purchase', 'done', Filter only completed or ongoing orders
        ])
        expected_delivery_dates = matching_orders.mapped('order_id.date_planned')

        # get max date from expected_delivery_dates list
        if len(expected_delivery_dates) != 0:
            expected_delivery_dates = max(expected_delivery_dates)

            return expected_delivery_dates





