from odoo import http
from odoo.http import request


class Hospital(http.Controller):
    @http.route(['/hospital/index/'], type="http", website ='True', auth='public')
    def hospital_index(self, **kw):
        return "Hello, world"

    @http.route(['/salesdata/'], type ='http', auth ='public', website ='True')
    def sale_data(self, **post):
        sales_data = request.env['sale.order'].sudo().search([])
        values = {
        'records': sales_data
        }
        print(values)