# -*- coding: utf-8 -*-
{
    'name': 'Export Records to XML',
    'version': '14.0.0.1.1',
    'category': 'Extra Tools',
    'summary': 'Export Records to XML',
    'description': """
        Export Records to XML
        14.0.0.1.1 - Added Documentations
        """,
    'author': 'Vertelab',
    'website': "https://www.vertel.se",
    'depends': ['base', 'event', 'hr', 'sale', 'project'],
    'data': [
        "security/ir.model.access.csv",
        "views/export_view.xml",
        "data/data.xml",
    ],
    'installable': True,
    'auto_install': False,
}
