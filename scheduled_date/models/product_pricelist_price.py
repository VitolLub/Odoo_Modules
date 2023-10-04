from odoo import models,fields,api
import logging

class SaleOrderLine(models.Model):
    _loggertwo = logging.getLogger(__name__)
    _inherit = 'sale.order.line'

    @api.depends('product_id', 'product_uom_qty', 'price_unit', 'discount', 'tax_id')
    def get_price_rule(self,product_id, quantity):
        # get price rule
        self._loggertwo.info('get_price_rule %s', product_id)
        self._loggertwo.info('get_price_rule %s', quantity)
        # self._logger.info('get_price_rule %s', partner_id)

        # get real product price

class ProductTemplate(models.Model):
    _logger = logging.getLogger(__name__)
    _inherit = 'product.pricelist.item'

    actual_price = fields.Float(
        string='Actual Price',
        compute='_compute_real_price',
        readonly=True,
        store=True)


    '''
    computing real price
    '''
    def _compute_real_price(self):
        for product in self:
            # check if scheduled_date_on_change NOT None and rewrite expected_delivery
            pricelist = self.env['product.pricelist'].browse(1)
            product_res = self.env['product.product'].browse(product.id)
            uom = product_res.uom_id.id
            self._logger.info('fixed_price %s', uom)
            result = pricelist.with_context(uom=uom).get_product_price(product_res, 1, False)
            self._logger.info('fixed_price %s', result)

            self._logger.info('fixed_price %s', product.product_tmpl_id)
            self._logger.info('fixed_price %s', product.product_tmpl_id.id)
            self._logger.info('fixed_price %s', product.product_tmpl_id.name)
            self._logger.info('fixed_price %s', product.product_tmpl_id.default_code)

            self._logger.info('fixed_price %s', product.name)
            self._logger.info('fixed_price %s', product.id)
            self._logger.info('fixed_price %s', product.min_quantity)
            self._logger.info('fixed_price %s', product.pricelist_id.id)
            self._logger.info('fixed_price %s', product.base_pricelist_id)

            partner2 = self.env['res.partner'].browse(product.product_tmpl_id.id)

            self._logger.info('fixed_price %s', partner2)
            self._logger.info('fixed_price %s', partner2.id)
            self._logger.info('fixed_price %s', partner2.parent_id.id)

            self._logger.info('---------------------------------------')
            # SaleOrderLine.get_price_rule(product.id, product.min_quantity, product.pricelist_id)
            # product = self.env['product.pricelist'].search([('id', '=', product.id)])
            # self._logger.info('get_price_rule %s', product)
            # self._logger.info('get_price_rule %s', product.id)
            # self._logger.info('get_price_rule %s', product.name)
            # self._logger.info('get_price_rule %s', product.partner_id)
            # self._logger.info('get_price_rule %s', product.partner_id.id)
            # self._logger.info('---------------------------------------')
            # standard_price = self.env['product.template'].search([('id', '=', product.product_tmpl_id.id)])
            # # float data 3 digits after comma
            # if standard_price:
            #     actual_price_value = float(standard_price.standard_price)
            #     self._logger.info('actual_price_value %s', actual_price_value)
            # else:
            #     actual_price_value = 0
            #
            #
            #
            #
            # product.actual_price = actual_price_value
            # self._logger.info('fixed_price %s', standard_price.standard_price)
            # self._logger.info('fixed_price %s', standard_price.list_price)
            self._logger.info('====================================')






