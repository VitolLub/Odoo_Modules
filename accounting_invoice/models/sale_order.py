from odoo import models,fields,api
import logging

class SaleOrder(models.Model):
    _logger = logging.getLogger(__name__)
    _inherit = 'sale.order'

    amount_outstanding = fields.Float(string='Outstanding Amount', store=False)
    amount_to_refund = fields.Float(string='Amount to Refund', store=False)
    amount_display = fields.Char(compute='_compute_amount_display', string='Amount to Display', store=True)

    def _compute_amount_display(self):
        '''
        Statuses:
        partial  - partially paid
        in_payment - still not paid
        reversed  - refunded
        :return:
        '''
        statuses = ['partial', 'in_payment', 'reversed']
        for order in self:

            # get all invoices from account.move
            invoices = order.invoice_ids

            # if invoices exists with current order
            if invoices:

                # check payment_state from currecnt order invoices
                payment_state = invoices.mapped('payment_state')

                invoices = invoices.filtered(lambda current_order: current_order.payment_state in statuses) #['partial', 'in_payment']
                amount_total_signed = sum(invoices.mapped('amount_total_signed'))

                if 'reversed' in payment_state:
                    order.amount_to_refund = amount_total_signed
                else:
                    order.amount_outstanding = amount_total_signed

                # amount_outstanding and  amount_to_refund by default is 0.0 if current order doesn't have any reversed,partial or in_payment statuses
                if order.amount_outstanding == 0.0 and order.amount_to_refund == 0.0:
                    order.amount_display = "OK"
                else:
                    order.amount_display = str(order.amount_outstanding)+" / "+str(order.amount_to_refund)

            else:
                # set Not invoiced for amount_display if current order doesn't have invoices
                order.amount_display = "Not invoiced"


