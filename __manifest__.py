{
    'name': 'Food Sales',
    'version': '1.0',
    'description': 'Module to make point of sales of foods',
    'summary': 'Module to make point of sales of foods',
    'author': 'IhsanSFD',
    'website': 'ihsansfd.github.io',
    'category': 'Sales',
    'depends': [
        'base','mail'
    ],
    'data': [
        'views/actions/product_view.xml',
        'views/actions/recipe_view.xml',
        'views/actions/customer_view.xml',
        'views/actions/order_view.xml',
        'views/menus/main_menu.xml',
        'report/template.xml',
        'report/order_report.xml',
        'security/ir.model.access.csv',
        'data/sequence.xml'
    ],
    'application': True
}