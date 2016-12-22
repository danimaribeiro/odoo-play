# -*- coding: utf-8 -*-
# © 2016 Danimar Ribeiro, Trustcode
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    'name': 'Odoo Pilot',
    'category': 'Tools',
    'summary': 'Odoo Pilot - Make Odoo instalation Easier',
    'version': '1.0',
    'description': """Odoo Pilot - Make Odoo instalation Easier""",
    'author': 'Trustcode',
    'depends': ['website', 'website_portal', 'portal_sale'],
    'data': [
        'views/pilot.xml',
        'views/pilot_templates.xml',
        'security/ir.model.access.csv',
    ],
    'application': True,
    'instalable': True,
}
