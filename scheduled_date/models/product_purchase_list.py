from odoo import http,models,fields,api
import logging
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


    # set color for purchase_order_ids
    purchase_list = fields.Many2many(
        'product.template.purchase.list',
        compute='_compute_purchase_order_ids',
        string='Purchase List',
        )

    def _compute_purchase_order_ids(self,scheduled_date_on_change=None,po_name=None):

        for product in self:
            current_url_data = json.loads(request.httprequest.data)

            # get selector and product_id depend on model
            selector,product_id = self.get_selector(current_url_data,product)

            # update date_planned field for product.template.purchase.list
            if scheduled_date_on_change != None:
                # update date_planned field for product.template.purchase.list
                try:
                    self.env['product.template.purchase.list'].search([('po', '=', str(po_name))]).write({'date_planned': scheduled_date_on_change})

                except Exception as e:
                    self._logger.error('Error: %s', e)

            if scheduled_date_on_change == None:

                purchase_orders_line = self.env['purchase.order.line'].search([
                    ('product_id', 'in', product_id),
                ])

                for purchase_orders_lin in purchase_orders_line:

                    self.check_every_order_line(product,purchase_orders_lin,selector)

                product.purchase_list = self.env['product.template.purchase.list'].search(
                    [(selector)])

    def check_every_order_line(self,product,purchase_orders_lin,selector):

        # get all data from purchase.order model by id
        purchase_res = self.env['purchase.order'].search([('id', '=', purchase_orders_lin.order_id.id)])

        try:

            product_template_purchase_list = self.env['product.template.purchase.list'].search(
                [(selector), ('purchase_id', '=', purchase_res.id)])

            # if product_template_purchase_list exist then update data
            if product_template_purchase_list:
                # update data
                self.update_values(product_template_purchase_list, purchase_orders_lin, purchase_res, product,
                                   use_case=True)
            else:
                # create data
                self.update_values(product_template_purchase_list, purchase_orders_lin, purchase_res, product,
                                   use_case=False)

        except Exception as e:
            self._logger.error('Error %s', e)

    def get_selector(self,current_url_data,product):
        '''
        selector used for Products -> Product Variants
        Product Variants used product.product model and we gen't get curent variend ID
        So if model is product.product then we get curent variant ID for work
        if model is product.template then we get curent product ID for work
        '''

        if current_url_data['params']['model'] == 'product.template':
            selector = 'product_id', '=', product.id
            product_id = product.product_variant_ids.ids
        else:
            selector = 'variation_id', '=', current_url_data['params']['args'][0][0]
            product_id = current_url_data['params']['args'][0]

        return selector,product_id

    # update/create record into product.template.purchase.list
    def update_values(self,product_template_purchase_list,purchase_orders_lin,purchase_res,product,use_case):


        data = {
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
            'variation_id': purchase_orders_lin.product_id.id
        }

        if use_case == True:
            product_template_purchase_list.write(data)
        elif use_case == False:
            product_template_purchase_list.create(data)
