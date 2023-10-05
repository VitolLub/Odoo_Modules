from odoo import models,fields,api
import logging


class ProductTemplate(models.Model):
    _logger = logging.getLogger(__name__)
    _inherit = 'product.pricelist.item'

    actual_price = fields.Monetary(
        string='Actual Price',
        compute='_compute_actual_price',
        readonly=True)


    '''
    computing actual price
    '''
    def _compute_actual_price(self):
        for product in self:
            try:
                if product.compute_price == 'fixed':

                    # assign actual price to current product
                    product.actual_price = product.fixed_price

                else:
                    # get pricelist for current product
                    pricelist = self.env['product.pricelist'].browse(product.pricelist_id.id)

                    # get product data for current product
                    product_res = self.env['product.product'].browse(product.product_id.id)

                    # get partner id for current product
                    uom = product_res.uom_id.id

                    # get actual price for current product
                    actula_price = pricelist.with_context(uom=uom).get_product_price(product_res, False, False)

                    # assign actual price to current product
                    product.actual_price = actula_price
            except Exception as e:
                self._logger.error('Error: %s', e)
                self._logger.error('Product ID is: %s and PriceList ID is: %', product.id, product.pricelist_id.id)



