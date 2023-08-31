from odoo import http,models,fields,api
import logging,sys
from datetime import datetime, timedelta
import datetime
from functools import reduce


class StockPickingInherited(models.Model):
    _logger = logging.getLogger(__name__)
    _inherit = 'stock.picking'

    @api.onchange('scheduled_date')
    def _onchange_scheduled_date(self):
        self._logger.info(f"_onchange_scheduled_date123")
        for picking in self:
            self._logger.info(f"_onchange_scheduled_date {picking}")
            if picking.scheduled_date:
                self._logger.info(f"_onchange_scheduled_date {picking.scheduled_date}")
                for move_line in picking.move_line_ids:
                    self._logger.info(f"_onchange_scheduled_date {move_line}")
                    product = move_line.product_id.product_tmpl_id
                    self._logger.info(f"_onchange_scheduled_date {product}")
                    product._compute_expected_delivery(picking.scheduled_date)

class ScheduledDateProductGrid(models.Model):
    _logger = logging.getLogger(__name__)
    _inherit = 'product.template'
    scheduled_date = fields.Many2one('stock.picking', string="stock.picking", required=True)


    expected_delivery = fields.Char(
        string='Expected Delivery',
        compute='_compute_expected_delivery',
        readonly=True,
        store=True)


    @api.onchange('scheduled_date')
    def _onchange_scheduled_date(self):
        self._logger.info(f"_onchange_scheduled_date")
        self._logger.info(f"Value {self.scheduled_date}")


    '''
    update purchase_order 
    date_planned field
    '''

    @api.onchange('scheduled_date')
    @api.depends('scheduled_date')
    def _compute_expected_delivery(self,scheduled_date_on_change=None):
        # super(CustomModuleProductGrid, self).update({
        #     'expected_delivery': 'test',
        # })
        for product in self:
            if product.default_code != False:
                # super().update({
                #     'expected_delivery': self._search_expected_delivery(),
                # })
                matching_orders = self._search_expected_delivery('default_code', product.default_code)


                expected_delivery_dates = matching_orders.mapped('package_level_id')
                # self._logger.info(f'+++++++++++++++++++++++++++++')
                # self._logger.info(f"matching_orders {matching_orders.mapped('reference')}")
                # self._logger.info(f"matching_orders {matching_orders.mapped('package_level_id')}")
                # self._logger.info(f"matching_orders {matching_orders.mapped('consume_line_ids')}")
                # self._logger.info(f"matching_orders {matching_orders.mapped('create_date')}")
                # self._logger.info(f"matching_orders {matching_orders.mapped('create_uid')}")
                # self._logger.info(f"matching_orders {matching_orders.mapped('display_name')}")
                # self._logger.info(f"matching_orders {matching_orders.mapped('id')}")
                # self._logger.info(f"matching_orders {matching_orders.mapped('package_level_id')}")
                # self._logger.info(f"matching_orders {matching_orders.mapped('picking_code')}")
                # self._logger.info(f"picking_id.scheduled_date {matching_orders.mapped('picking_id.scheduled_date')}")
                # self._logger.info(f"matching_orders {matching_orders.mapped('produce_line_ids')}")
                # self._logger.info(f"matching_orders {matching_orders.mapped('state')}")
                # self._logger.info(f"matching_orders {matching_orders.mapped('qty_done')}")
                # self._logger.info(f"matching_orders {matching_orders.mapped('result_package_id')}")
                try:
                    self._logger.info(f"scheduled_date_origin {product.scheduled_date}")
                    self._logger.info(f"scheduled_date_origin {product.expected_delivery}")
                except:
                    pass
                self._logger.info(f'+++++++++++++++++++++++++++++')

                scheduled_date = matching_orders.mapped('picking_id.scheduled_date')
                # get newest date from scheduled_date
                # scheduled_date = max(scheduled_date)
                self._logger.info(f"(99999999999999999999999")
                self._logger.info(f"matching_orders {scheduled_date}")
                # get biggest date from array [datetime.datetime(2023, 8, 29, 12, 45, 33), datetime.datetime(2023, 8, 29, 12, 45, 34)]
                if len(scheduled_date)!= 0:
                    self._logger.info(f"scheduled_date {scheduled_date}")
                    scheduled_date = reduce(lambda x, y: x if x > y else y, scheduled_date, datetime.datetime.min)
                    self._logger.info(f"scheduled_date {scheduled_date}")
                    # convert from [datetime.datetime(2023, 9, 2, 14, 22, 16)] to 2023-09-02 14:22:16
                    formatted_dates = scheduled_date.strftime("%Y-%m-%d %H:%M:%S")
                    self._logger.info(f"scheduled_date {formatted_dates}")
                    if product.expected_delivery == False:
                        product.expected_delivery = str(formatted_dates)
                    elif scheduled_date != None:
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
        self._logger.info(f'matching_orders {matching_orders}')
        self._logger.info(f'+==============================+')
        return matching_orders





