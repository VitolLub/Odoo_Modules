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
            current_data = json.loads(request.httprequest.data)

            if current_data['params']['model'] == 'product.template':
                # product_id = product.id
                selector = 'product_id', '=', product.id
                product_id = product.product_variant_ids.ids
            else:
                # variation_id = current_data['params']['args'][0][0]
                selector = 'variation_id', '=', current_data['params']['args'][0][0]
                product_id = current_data['params']['args'][0]

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

                    # get all data from purchase.order model by id
                    purchase_res = self.env['purchase.order'].search([('id', '=', purchase_orders_lin.order_id.id)])

                    try:

                        product_template_purchase_list = self.env['product.template.purchase.list'].search(
                            [(selector), ('purchase_id', '=', purchase_res.id)])

                        # if test_test exist then update data
                        if product_template_purchase_list:
                            # update data
                            product_template_purchase_list.write({
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
                            self.env['product.template.purchase.list'].sudo().create({
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
                        self._logger.error('Error %s', e)

                product.purchase_list = self.env['product.template.purchase.list'].search(
                    [(selector)])