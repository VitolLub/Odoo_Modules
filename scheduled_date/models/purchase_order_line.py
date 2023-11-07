from odoo import http,models,fields,api
import logging
from odoo.http import request
import json

class PurchaseOrderLine(models.Model):
    _inherit= 'purchase.order.line'

    '''
    Created new field necessary to task VIPODOO-1
    '''

    purchase_order_id = fields.Many2one('purchase.order', string='Purchase Order', related='order_id')
    date_planned = fields.Datetime(related='purchase_order_id.date_planned', string='Receipt Date',store=True)
    source_document = fields.Char(related='purchase_order_id.origin', string='Source Document', store=True)

    res_users = fields.Many2one('res.users', related='purchase_order_id.user_id', string='Buyer')
    buyer = fields.Char(related='res_users.name', string='Buyer', store=True)
    qty_dem_rec = fields.Char(string='Qty dem / rec', compute='_compute_amount_order')


    def _compute_amount_order(self):
        for line in self:
            if str(line.qty_received).endswith('.0') or str(line.qty_received).endswith('.0'):
                product_qty = int(line.product_qty)
                qty_received = int(line.qty_received)
            else:
                product_qty = float(line.product_qty)
                qty_received = float(line.qty_received)

            # set values for  amount_order
            line.qty_dem_rec = str(product_qty) +" / "+ str(qty_received)