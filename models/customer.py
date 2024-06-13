from odoo import api, fields, models


class Customer(models.Model):
    _name = 'food_sales.customer'

    name = fields.Char(string="Name", required=True)
    contact = fields.Char(string="Contact")
    address = fields.Char(string="Address")
    company_id = fields.Many2one(comodel_name="res.company", string="Company")
    order_count = fields.Integer(string="Order Count", compute='_compute_order_count')

    @api.depends('order_count')
    def _compute_order_count(self):
        for rec in self:
            order_count = self.env['food_sales.order'].search_count([('customer_id', '=', rec.id)])
            rec.order_count = order_count

    def customer_orders(self):
        return {'type': 'ir.actions.act_window',
                'name': f"{self.name}'s Orders",
                'res_model': 'food_sales.order',
                'domain': [('customer_id', '=', self.id)],
                'target': 'main',
                'view_mode': 'tree,form'}
