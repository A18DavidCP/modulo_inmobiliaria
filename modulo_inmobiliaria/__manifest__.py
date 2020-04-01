# -*- coding: utf-8 -*-
{
    'name': "Inmobiliaria",  # Module title
    'summary': "Control casas y contratos inmobiliaria",  # Module subtitle phrase
    'description': """Long description""",  # You can also rst format
    'author': "David Conde",
    'website': "http://www.example.com",
    'category': 'Uncategorized',
    'version': '12.0.1',
    'depends': ['base'],
    # This data files will be loaded at the installation (commented becaues file is not added in this example)
    'data': [
        'security/groups.xml',
        'security/ir.model.access.csv',
        'views/inmobiliaria_casa.xml',
        'views/inmobiliaria_persona.xml',
        'views/inmobiliaria_contrato.xml'
    ],
    # This demo data files will be loaded if db initialize with demo data (commented becaues file is not added in this example)
    # 'demo': [
    #     'demo.xml'
    # ],
}
