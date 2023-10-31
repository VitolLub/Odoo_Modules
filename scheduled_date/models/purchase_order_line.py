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
    date_planned = fields.Datetime(related='purchase_order_id.date_planned', string='Scheduled Date')
    source_document = fields.Char(related='purchase_order_id.origin', string='Source Document')
    res_users = fields.Many2one('res.users', related='purchase_order_id.user_id', string='Buyer')
    buyer = fields.Char(related='res_users.name', string='Buyer')