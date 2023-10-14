from odoo import http,models,fields,api
import logging,sys
from datetime import datetime, timedelta
import datetime
from odoo.http import request
import json

class ScheduledDate(models.Model):
    _name= 'product.template.purchase.list'

    id = fields.Integer(string='ID')
    name = fields.Char(string='Full name')
    purchase_id = fields.Integer(string='Purchase ID', required=True)
    product_id = fields.Integer(string='Product ID', required=True)
    quantity = fields.Float(string='Quantity')
    price_subtotal = fields.Float(string='Amount', required=True)
    vendor = fields.Char(string='Vendor', store=True)
    buyer = fields.Many2one('res.users', string='Buyer')
    source_document = fields.Char(string='Source Document')
    po = fields.Char(string='PO')
    date_planned = fields.Char(string='Planed Date')
    variation_id = fields.Integer(string='Variation ID')



'''
Display List of Purchase Orders in Product Form View 
Products -> Any Product -> Purchase -> Purchase List
'''
class ProductPurchaseList(models.Model):
    _logger = logging.getLogger(__name__)
    _inherit = 'product.template'

    # purchase_order_ids = fields.Many2many(
    #     'purchase.order.line',
    #     compute='_compute_purchase_order_ids',
    #     string='Purchase Name'
    #     )
    # set color for purchase_order_ids
    purchase_list = fields.Many2many(
        'product.template.purchase.list',
        compute='_compute_purchase_order_ids',
        string='Purchase List',
        )


    # @api.depends('purchase_name')
    def _compute_purchase_order_ids(self,scheduled_date_on_change=None,po_name=None):

        for product in self:
            # self._logger.info('scheduled_date_on_change: %s', scheduled_date_on_change)
            # self._logger.info('RELA ID: %s', product.product_variant_ids)
            current_url = request.httprequest.url
            self._logger.info('RELA ID2: %s', current_url)
            current_data = request.httprequest.data
            self._logger.info('RELA ID2: %s', current_data)
            self._logger.info('RELA ID2: %s', type(current_data))
            # current_data to json
            current_data = json.loads(current_data)
            self._logger.info('RELA ID3: %s', current_data)
            self._logger.info('RELA ID4: %s', current_data['params']['args'][0][0])
            self._logger.info('RELA ID4: %s', current_data['params']['model'])
            if current_data['params']['model'] == 'product.template':
                # product_id = product.id
                selector = 'product_id', '=', product.id
                product_id = product.product_variant_ids.ids
            else:
                # variation_id = current_data['params']['args'][0][0]
                selector = 'variation_id', '=', current_data['params']['args'][0][0]
                product_id = current_data['params']['args'][0]


            self._logger.info('product.product_variant_ids %s', product.product_variant_ids.ids)

            # # # display all data from product.template
            # for field_name, field_value in product.read()[0].items():
            #     self._logger.info(f"{field_name}: {field_value}")
            #     self._logger.info('==---====---=====---====---=====---====---=====---====---=====---====---=====---====---===')

            # get variant id by attribute line
            # cur_prodcut = self.env['product.product'].search([('product_tmpl_id', '=', product.id)])
            # for purchase_orders_lin_res in cur_prodcut:
            #     for field_name, field_value in purchase_orders_lin_res.read()[0].items():
            #         self._logger.info(f"{field_name}: {field_value}")
            #         self._logger.info('==---====---=====---====---=====---====---=====---====---=====---====---=====---====---===')

            # try:
            #     self._logger.info('RELA ID1: %s', product.valid_product_template_attribute_line_ids)
            #
            #     self._logger.info('RELA ID2: %s',product.product_variant_ids)
            #     self._logger.info('RELA ID3: %s',product.product_variant_id)
            #     self._logger.info('RELA ID3: %s', product.product_variant_id.id)
            # except Exception as e:
            #     self._logger.error('Error product: %s', e)


            if scheduled_date_on_change != None:
                # update date_planned field for product.template.purchase.list
                try:
                    self._logger.info('order_id: %s', po_name)
                    resp = self.env['product.template.purchase.list'].search([('po', '=', str(po_name))]).write({'date_planned': scheduled_date_on_change})
                    self._logger.info('resp: %s', resp)
                except Exception as e:
                    self._logger.error('Error: %s', e)
            if scheduled_date_on_change == None:
                self._logger.info('RELA ID3: %s', product.id)
                self._logger.info('RELA ID4: %s', product.name)
                # self._logger.info('product id: %s', product.default_code)
                # self._logger.info('product id: %s', product.description_picking)
                self._logger.info('RELA ID: %s', product.pricelist_id.id)
                # try:
                #     self._logger.info('product id: %s', product.product_id)
                # except Exception as e:
                #     self._logger.error('Error: %s', e)

                # get variant id
                # search data variations from product.product.order model by current product id
                # product_product = self.env['product.product'].search([('product_tmpl_id', '=', product.id)])
                # self._logger.info('product_product id: %s', product_product.ids)

                # for purchase_orders_lin in product_product:
                #     self._logger.info('Product variant ID: %s', purchase_orders_lin.id)
                #     self._logger.info('START///////////////////////////////////////////////')
                #     for field_name, field_value in purchase_orders_lin.read()[0].items():
                #         self._logger.info(f"{field_name}: {field_value}")
                #         self._logger.info('==---====---=====---====---=====---====---=====---====---=====---====---=====---====---===')
                #     self._logger.info('END///////////////////////////////////////////////')
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
                # for valueer in purchase_orders:
                #     self._logger.info('//////////////////////')
                #     # self._logger.info('purchase_orders: %s', value)
                #     # self._logger.info('PO: %s', value.name)
                #     # self._logger.info('Source Document: %s', value.origin)
                #     # self._logger.info('date_planned: %s', value.date_planned)
                #     # self._logger.info('partner_id: %s', value.partner_id.name)
                #     # self._logger.info('partner_id: %s', value.company_id.name)
                #     # self._logger.info('partner_id: %s', value.user_id.name)
                #     for field_name, field_value in valueer.read()[0].items():
                #         self._logger.info(f"{field_name}: {field_value}")
                #         self._logger.info(
                #             '==---====---=====---====---=====---====---=====---====---=====---====---=====---====---===')
                #
                #     self._logger.info('//////////////////////')

                self._logger.info('product_product.ids: %s', product.product_variant_ids.ids)
                purchase_orders_line = self.env['purchase.order.line'].search([
                    ('product_id', 'in', product_id),
                ])
                # try:
                #     for order_line in purchase_orders_line:
                #         self._logger.info("Purchase Order Line ID:", order_line.id)
                #         for field_name, field_value in order_line.read()[0].items():
                #             self._logger.info(f"{field_name}: {field_value}")
                #             self._logger.info('-------------------------------------------')
                # except Exception as e:
                #     self._logger.info("Error:", e)
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
                        # self._logger.info('Product variant ID: %s', purchase_orders_lin.id)

                        # for field_name, field_value in purchase_orders_lin.read()[0].items():
                        #     self._logger.info(f"{field_name}: {field_value}")
                        #     self._logger.info('==---====---=====---====---=====---====---=====---====---=====---====---=====---====---===')

                        # purchase_orders = self.env['purchase.order'].search([
                        #     ('order_line.product_id', 'in', purchase_orders_lin.id),
                        #     # Filter only completed or ongoing orders
                        # ])

                        self._logger.info('purchase_orders_lin.order_id.id: %s', purchase_orders_lin.order_id.id)

                        # get all data from purchase.order model by id
                        purchase_res = self.env['purchase.order'].search([('id', '=', purchase_orders_lin.order_id.id)])
                        # for purchase_re in purchase_res:
                        #     for field_name, field_value in purchase_re.read()[0].items():
                        #         self._logger.info(f"{field_name}: {field_value}")
                        #         self._logger.info('==---====---=====---====---=====---====---=====---====---=====---====---=====---====---===')
                        # self._logger.info('purchase_res: %s', purchase_res)
                        try:
                            self._logger.info('purchase_id: %s', purchase_res.id)
                            self._logger.info('purchase_res: %s', product.id)
                            self._logger.info('purchase_orders_lin.order_id.name: %s', purchase_orders_lin.order_id.name)

                            # select all records where product_id=product.id and purchase_id=purchase_res.id
                            # ('variation_id', '=', current_data['params']['args'][0][0]),
                            test_test = self.env['product.template.purchase.list'].search(
                                [(selector), ('purchase_id', '=', purchase_res.id)])
                            self._logger.info('selector: %s', selector)
                            self._logger.info('purchase_id_origin: %s', purchase_res.id)
                            self._logger.info('test_test: %s', test_test)
                            # if test_test exist then update data
                            if test_test:
                                # update data
                                test_test.write({
                                    'name': purchase_orders_lin.name,
                                    'quantity': purchase_orders_lin.product_qty,
                                    'purchase_id': purchase_res.id,
                                    'product_id': product.id,
                                    'price_subtotal': purchase_orders_lin.price_subtotal,
                                    'vendor': purchase_orders_lin.partner_id.name,
                                    'buyer': purchase_res.user_id.id,
                                    'source_document': purchase_res.origin,
                                    'po': purchase_orders_lin.order_id.name,
                                    'date_planned': purchase_res.date_planned
                                })
                            else:
                                # create data
                                save_res = self.env['product.template.purchase.list'].sudo().create({
                                    # 'id': product.id,
                                    'name': purchase_orders_lin.name,
                                    'quantity': purchase_orders_lin.product_qty,
                                    'purchase_id': purchase_res.id,
                                    'product_id': product.id,
                                    'price_subtotal': purchase_orders_lin.price_subtotal,
                                    'vendor': purchase_orders_lin.partner_id.name,
                                    'buyer': purchase_res.user_id.id,
                                    'source_document': purchase_res.origin,
                                    'po': purchase_orders_lin.order_id.name,
                                    'date_planned': purchase_res.date_planned,
                                    'variation_id':purchase_orders_lin.product_id.id
                                })


                        except Exception as e:
                            self._logger.error('Error product.template.purchase.list: %s', e)

                            # save data into purchase.order.line.test model
                            #
                            # purchase_test = self.env['product.template.purchase.list'].search(
                            #     [('product_id', '=', product.id)])
                            #
                            # product.purchase_list = purchase_test
                            # self._logger.info('save_res: %s', save_res)
                            # self._logger.info('Product variant: %s', purchase_orders_lin.id)
                            # self._logger.info('Product variant: %s', purchase_orders_lin.name)
                            # self._logger.info('Product Quantity: %s', purchase_orders_lin.product_qty)
                            # self._logger.info('Amount: %s', purchase_orders_lin.partner_id.name)

                except Exception as e:
                    self._logger.error('Error: %s', e)

                # self._logger.error('purchase_orders_line: %s', purchase_orders_line)
                # # assign purchase_orders to product.purchase_order_ids
                # # product.purchase_order_ids = purchase_orders_line #purchase_orders
                # # purchase_test = self.env['scheduled.date'].sudo().search([('product_id', '=', product.id)])
                # # select all data from scheduled.date model product_id=product.id
                # purchase_test = self.env['product.template.purchase.list'].search([('product_id', '=', product.id)])
                # # get all data from scheduled.date model
                # # try:
                # #     for purchase_tes in purchase_test:
                # #         self._logger.info("Purchase Order Line ID:", purchase_tes.id)
                # #         for field_name, field_value in purchase_tes.read()[0].items():
                # #             self._logger.info(f"{field_name}: {field_value}")
                # #             self._logger.info('***********************************')
                # # except Exception as e:
                # #     self._logger.info("Error:", e)
                #
                # self._logger.info('purchase_test: %s', purchase_test)
                purchase_test = self.env['product.template.purchase.list'].search(
                    [(selector)])

                product.purchase_list = purchase_test
                self._logger.info('====================================')