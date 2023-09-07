from odoo import models,api
import logging

class StockPicking(models.Model):
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
                self._logger.info(f'scheduled_date2 {picking.scheduled_date}')
                for move_line in picking.move_line_ids:
                    product = move_line.product_id.product_tmpl_id
                    self._logger.info(f'scheduled_date2 {product}')
                    product._compute_expected_delivery(picking.scheduled_date)