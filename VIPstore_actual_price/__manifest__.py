{
    'name': 'VIPstore_actual_price',
    'summary': 'Add Actual Price to product.pricelist.item',
    'description': 'Add Actual Price to product.pricelist.item',
    'author': 'Goodahead',
    'depends': ['base','mail','product','stock','sale','purchase','account'],
    'data': [
        'views/product_pricelist_item_view.xml',
    ],
    'installable': True,
    'auto_install': False,
    'application': True,
    'module': 'vip_store_actual_price',
}
