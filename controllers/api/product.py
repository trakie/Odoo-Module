from odoo import http
from odoo.http import request
import json


class ProductController(http.Controller):

    # Digunakan tipe http krn lebih mudah dalam get data, apabila pake json maka parameter di-passing
    # melalui json pula sementara pake http, parameter cukup di-passing dalam url.
    @http.route(['/api/product', '/api/product/<int:product_id>'], auth='public', method='GET', type='http')
    def product(self, product_id=None, name=None, category=None, active=None):
        res, filter_data = [], []

        if not product_id:
            if name: filter_data.append(("name", "ilike", name))
            if category: filter_data.append(("category", "=", category))
            if active: filter_data.append(("active", "=", active))
        else: filter_data.append(("id", "=", product_id))

        rec = request.env['food_sales.product'].sudo().search(filter_data)

        for data in rec:
            res.append({'id': data.id, 'name': data.name, 'price': data.price, 'desc': data.desc,
                        'category': data.category})

        return request.make_response(json.dumps({'code': 200, 'found': True if res else False, 'data': res}),
                                     [('Content-Type', 'application/json')])
