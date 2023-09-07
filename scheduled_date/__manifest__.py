{
    'name': 'Scheduled Date',
    'summary': 'Add custom label to product form view after barcode input',
    'description': 'Add custom label to product form view after barcode input',
    'author': 'Lubomir',
    'depends': ['base','mail','product','stock','sale'],
    'data': [
        'views/expected_delivery_product_grid_view.xml',
    ],
    'installable': True,
    'auto_install': False,
    'application': True,
    'module': 'scheduled_date',
}
