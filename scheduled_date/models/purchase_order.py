from odoo import models,api
import logging

class PurchaseOrder(models.Model):
    _logger = logging.getLogger(__name__)
    _inherit = 'purchase.order'

    '''
    Update expected_delivery field when scheduled_date is changed
    '''
    @api.onchange('date_planned')
    def _onchange_scheduled_date(self):

        for order in self:
            self._logger.info(f'purchase order1 {order}')
            if order.date_planned:
                self._logger.info(f'purchase order1 {order.date_planned}')
                product = order.product_id.product_tmpl_id
                product._compute_expected_delivery(order.date_planned)