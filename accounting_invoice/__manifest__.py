{
    'name': 'Acounting Invoice',
    'summary': '',
    'description': '',
    'author': 'Goodahead',
    'depends': ['base','product','stock','purchase','sale'],
    'data': [
        'views/sale_order_outstanding_to_refund.xml',
    ],
    'installable': True,
    'auto_install': False,
    'application': True,
    'module': 'accounting_invoice',
}
