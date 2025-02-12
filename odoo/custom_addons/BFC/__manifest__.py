{
    'name': 'BFC',
    'version': '1.0',
    'category': 'Services',
    'summary': 'Manage Reception Operations for Martial Arts Centers',
    'description': 'A module to manage reception operations including member registration, subscription tracking, and payments.',
    'depends': ['base', 'mail'],
    'data': [
        'security/ir.model.access.csv',
        'views/martial_arts_center_views.xml',
        'views/martial_arts_game_views.xml',
        'views/renewal_views.xml',
        'reports/reports.xml',
        'reports/qr_card.xml',

    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}
