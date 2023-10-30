{
    'name': 'PO Settings',
    'summary': 'Add custom label to product form view after barcode input',
    'description': 'Add custom label to product form view after barcode input',
    'author': 'Lubomir',
    'depends': ['base','product','stock','purchase','sale'],
    'data': [
        'views/settings_views.xml',
    ],
    'installable': True,
    'auto_install': False,
    'application': True,
    'module': 'po_settings',
}
