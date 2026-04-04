{
    'name': 'Library Manager',
    'version': '17.0.1.0.0',
    'summary': 'Gestione libri e prestiti - Portfolio Junior Dev',
    'category': 'Tools',
    'author': 'Zigna Dev',
    'depends': ['base', 'mail'],
    'data': [
        'security/ir.model.access.csv',
        'views/loan_views.xml',
        'views/book_views.xml',
        'views/menu.xml',
        'data/demo_data.xml',
    ],
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
}
