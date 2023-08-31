from odoo import models, fields, api


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    def _compute_map_price(self):
        for product in self:
            # map price = Sale Price + 1
            print('Dbug')
            product.map_price = product.list_price + 1

    map_price = fields.Monetary(
        string='Map Price',
        compute='_compute_map_price',
        readonly=True,
        currency_field='company_currency_id',
        store=True)

    company_currency_id = fields.Many2one('res.currency', related='company_id.currency_id', string="Company Currency",
                                              readonly=True)






