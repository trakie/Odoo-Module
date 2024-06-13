from email.policy import default
from typing import Sequence
from odoo import api, fields, models


class Recipe(models.Model):
    _name = 'food_sales.recipe'
    _description = 'Recipe'
    name = fields.Char('Name', required=True)
    ingredients = fields.Text('Ingredients', required=True)
    steps = fields.Text('Steps')


