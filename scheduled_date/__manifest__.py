{
    'name': 'Scheduled Date',
    'summary': 'Add custom label to product form view after barcode input',
    'description': 'Add custom label to product form view after barcode input',
    'author': 'Lubomir',
    'depends': ['base','mail','product','stock','sale','purchase','account'],
    'data': [
        'views/expected_delivery_product_grid_view.xml',
        'views/expected_delivery_product_variation_view.xml',
        'views/product_purchase_list_view.xml',
        'views/account_move_ref_view.xml',
        'views/product_pricelist_item_view.xml',
    ],
    'installable': True,
    'auto_install': False,
    'application': True,
    'module': 'scheduled_date',
}
