from odoo import http,models,fields,api
import logging,sys
from datetime import datetime, timedelta
import datetime


class PurchaseOrderLineTest(models.Model):
    _name= 'purchase.order.line.test'

    id = fields.Integer(string='ID', required=True, store=True)
    custom_field1 = fields.Char(string='Custom Field 1', store=True)
    custom_field2 = fields.Float(string='Custom Field 2', store=True)
    purchase_id = fields.Integer(string='Purchase ID', store=True)
    product_id = fields.Integer(string='Product ID', store=True)
    company_id = fields.Many2one('res.company', string='Company', store=True)


'''
Display List of Purchase Orders in Product Form View 
Products -> Any Product -> Purchase -> Purchase List
'''
class ProductPurchaseList(models.Model):
    _logger = logging.getLogger(__name__)
    _inherit = 'product.template'
    # _name = 'product.purchase.list.test'
    # purchase_order_ids = fields.Many2many(
    #     'purchase.order.line',
    #     string='Purchase Orders',
    #     compute='_compute_purchase_order_ids',
    #     store=True,
    # )
    purchase_name = fields.Many2many(
        'purchase.order.line.test',
        compute='_compute_purchase_order_ids',
        string='Purchase Name',
        store=True,
        )

    @api.depends('purchase_name')
    def _compute_purchase_order_ids(self):
        for product in self:

            self._logger.info('product id: %s', product.id)
            self._logger.info('product id: %s', product.name)
            # self._logger.info('product id: %s', product.default_code)
            # self._logger.info('product id: %s', product.description_picking)
            self._logger.info('product id: %s', product.pricelist_id.id)
            # try:
            #     self._logger.info('product id: %s', product.product_id)
            # except Exception as e:
            #     self._logger.error('Error: %s', e)

            # get variant id
            # search data variations from product.product.order model by current product id
            product_product = self.env['product.product'].search([('product_tmpl_id', '=', product.id)])
            # self._logger.info('product id: %s', product_product.ids)
            # # try:
            # #     self._logger.info('product id: %s', product_product.default_code)
            # #     self._logger.info('product id: %s', product_product.active)
            # #     # get default code by product_product.ids
            # # except Exception as e:
            # #     self._logger.error('Error: %s', e)
            #
            #
            # purchase_orders = self.env['purchase.order'].search([
            #     ('order_line.product_id', 'in', product_product.ids),
            #     ('state', 'in', ['purchase', 'to approve','sent','draft']),  # Filter only completed or ongoing orders
            # ])
            #
            # self._logger.info('purchase_orders: %s', type(purchase_orders))
            # self._logger.info('purchase_orders: %s', purchase_orders)
            # self._logger.info('purchase_orders: %s', purchase_orders.ids)
            # # display key and value
            # for value in purchase_orders:
            #     self._logger.info('//////////////////////')
            #     self._logger.info('purchase_orders: %s', value)
            #     self._logger.info('PO: %s', value.name)
            #     self._logger.info('Source Document: %s', value.origin)
            #     self._logger.info('date_planned: %s', value.date_planned)
            #     self._logger.info('partner_id: %s', value.partner_id.name)
            #     self._logger.info('partner_id: %s', value.company_id.name)
            #     self._logger.info('partner_id: %s', value.user_id.name)
            #     self._logger.info('//////////////////////')



            purchase_orders_line = self.env['purchase.order.line'].search([
                ('product_id', 'in', product_product.ids),
            ])
            try:
                for order_line in purchase_orders_line:
                    self._logger.info("Purchase Order Line ID:", order_line.id)
                    for field_name, field_value in order_line.read()[0].items():
                        self._logger.info(f"{field_name}: {field_value}")
                        self._logger.info('-------------------------------------------')
            except Exception as e:
                self._logger.info("Error:", e)
            # #
            # # # add purchase_orders to purchase_orders_line
            # # purchase_orders_line.purchase_orders = purchase_orders
            # #
            # self._logger.info('purchase_orders_line: %s', purchase_orders_line)
            # self._logger.info('-------------------------------------------')
            try:
                # self._logger.info('purchase_orders: %s', purchase_orders.name)
                # self._logger.info('purchase_orders: %s', purchase_orders.origin)
                for purchase_orders_lin in purchase_orders_line:
                    self._logger.info('Product variant ID: %s', purchase_orders_lin.id)
                    # purchase_order_dev = self.env['purchase.order'].search([
                    #     ('order_line.product_id', 'in', purchase_orders_lin.id),
                    #     ('state', 'in', ['purchase', 'to approve', 'sent', 'draft']),
                    #     # Filter only completed or ongoing orders
                    # ])
                    # self._logger.info('user_id.name: %s', purchase_order_dev.user_id.name)
                    # save data into purchase.order.line.test model
                    save_res = self.env['purchase.order.line.test'].sudo().create({
                        'custom_field1': purchase_orders_lin.name,
                        'custom_field2': purchase_orders_lin.product_qty,
                        'purchase_id': purchase_orders_lin.id,
                        'product_id': product.id,
                        'company_id': product.company_id.id,
                    })
                    self._logger.info('save_res: %s', save_res)
                    self._logger.info('Product variant: %s', purchase_orders_lin.id)
                    self._logger.info('Product variant: %s', purchase_orders_lin.name)
                    self._logger.info('Product Quantity: %s', purchase_orders_lin.product_qty)
                    self._logger.info('Amount: %s', purchase_orders_lin.price_subtotal)

            except Exception as e:
                self._logger.error('Error: %s', e)

            self._logger.error('purchase_orders_line: %s', purchase_orders_line)
            # assign purchase_orders to product.purchase_order_ids
            # product.purchase_order_ids = purchase_orders_line #purchase_orders
            purchase_test = self.env['purchase.order.line.test'].sudo().search([('product_id', '=', product.id)])
            self._logger.info('purchase_test: %s', purchase_test)
            product.purchase_name = purchase_test
            # product.purchase_orders = purchase_orders
            self._logger.info('====================================')













