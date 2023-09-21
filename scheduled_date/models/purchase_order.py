from odoo import models,api
import logging

class PurchaseOrder(models.Model):
    _logger = logging.getLogger(__name__)
    _inherit = 'purchase.order'

    '''
    Update expected_delivery field when date_planned is changed
    Purchase -> Any Orders from List
    purchase.order -> date_planned
    '''
    @api.onchange('date_planned')
    def _onchange_scheduled_date(self):

        for order in self:
            if order.date_planned:

                # get products from order line
                products = order.order_line.product_id

                # run _compute_expected_delivery and update expected_delivery field
                # update expected_delivery field for product.template
                products.product_tmpl_id._compute_expected_delivery(order.date_planned)

                # update expected_delivery field for product.product
                products._compute_expected_delivery_for_product(order.date_planned)