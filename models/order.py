from email.policy import default
from odoo import api, fields, models
from odoo.exceptions import ValidationError
from datetime import datetime
import copy


class Order(models.Model):
    _name = 'food_sales.order'
    _description = 'Order'
    _order = 'write_date desc'
    _inherit = ["mail.thread", "mail.activity.mixin"]

    order_details_ids = fields.One2many(comodel_name='food_sales.order_details', inverse_name='order_id',
                                        string='Order Details')
    name = fields.Char(string='Order ID', readonly=True, default='New', required=True, copy=False)
    customer_id = fields.Many2one(comodel_name='food_sales.customer', string='Customer', ondelete='restrict')
    order_date = fields.Date(string='Date', default=datetime.today())
    status = fields.Selection(string='Status', selection=[('pending', 'Pending'), ('in_transit', 'In Transit'),
                                                          ('completed', 'Completed'), ('canceled', 'Canceled')],
                              default='pending')
    total = fields.Float(compute='_compute_total', string='Total', store=True)
    profit = fields.Float(compute='_compute_total', string='Net Profit', store=True)

    @api.constrains('order_details_ids')
    def _check_exist_the_same_product(self):
        list_of_products = []
        for rec in self:
            for order_detail in rec.order_details_ids:
                if order_detail.product_id in list_of_products:
                    raise ValidationError(f"You cannot have a duplicate product "
                                          f"({order_detail.product_id.product_name}) in one order")
                list_of_products.append(order_detail.product_id)

    @api.depends('order_details_ids')
    def _compute_total(self):
        total_price, total_profit = 0, 0

        for rec in self:
            for order_detail in rec.order_details_ids:
                cost = self.env['food_sales.product'].browse(order_detail.product_id.id)['cost']
                price = order_detail['product_price']
                qty = order_detail['product_quantity']

                total_price += price * qty
                total_profit += (price - cost) * qty

        rec.total = total_price
        rec.profit = total_profit

    @api.model
    def create(self, vals):
        if vals.get('name', 'New') == 'New':
            vals['name'] = self.env['ir.sequence'].next_by_code('food_sales.order')
        return super(Order, self).create(vals)

    def cancel_order(self):
        self.status = 'canceled'


class OrderDetails(models.Model):
    _name = 'food_sales.order_details'
    _description = 'This model keeps track what products a customer buys'

    order_id = fields.Many2one(comodel_name='food_sales.order', string='Order ID')
    name = fields.Char(string='ID', readonly=True, default='New', required=True, copy=False, invisible=True)
    product_id = fields.Many2one(comodel_name='food_sales.product', string='Product', required=True, store=True)
    product_name = fields.Char(compute='_compute_product_info', string='Name', store=True)
    product_price = fields.Float(compute='_compute_product_info', string='Price', store=True)
    product_quantity = fields.Integer(string='Quantity', required=True)

    @api.constrains('product_quantity')
    def _check_product_quantity(self):
        for rec in self:
            if rec.product_quantity <= 0:
                raise ValidationError("Quantity must be greater than 0")

            stock = self.env['food_sales.product'].search([('stock', '<', rec.product_quantity),
                                                           ('id', '=', rec.product_id.id)])
            if stock:
                raise ValidationError(f"Quantity for {stock.name} exceeds product's stock "
                                      f"({rec.product_quantity} > {stock.stock})")

    @api.depends('product_id')
    def _compute_product_info(self):
        for rec in self:
            rec.product_name = copy.deepcopy(rec.product_id.name)
            rec.product_price = copy.deepcopy(rec.product_id.price)

    @api.model
    def create(self, vals):
        rec = super(OrderDetails, self).create(vals)
        if rec.product_quantity:
            self.env['food_sales.product'].search([('id', '=', rec.product_id.id)]) \
                .write({'stock': rec.product_id.stock - rec.product_quantity})

        if vals.get('name', 'New') == 'New':
            vals['name'] = self.env['ir.sequence'].next_by_code('food_sales.order_details')
        return rec
