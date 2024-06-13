from odoo import models, fields


class Product(models.Model):
    _name = "food_sales.product"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _description = "Model kue"
    _order = 'write_date desc'

    name = fields.Char(string="Name", required=True)
    desc = fields.Char(string='Description')
    category = fields.Selection(string="Category", selection=[('appetizer', 'Appetizer'),
                                                              ('main', 'Main'),
                                                              ('desert', 'Desert'),
                                                              ('drink', 'Drink')])
    image = fields.Binary(string="Image")
    price = fields.Float(string='Price', required=True)
    stock = fields.Integer(string='Stock', required=True)
    cost = fields.Float(string='Cost', required=True)
    recipe_ids = fields.Many2one(comodel_name='food_sales.recipe', string='Recipe')
    active = fields.Boolean(string="Active", default=True)
