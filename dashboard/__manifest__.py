# -*- coding: utf-8 -*-
# © 2016 Danimar Ribeiro, Trustcode
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    'name': 'Rich Dashboards for Odoo',
    'summary': """Rich Dashboards""",
    'description': """Rich dashboards for Odoo - Mantido por Trustcode""",
    'version': '10.0.1.0.0',
    'category': 'Charts',
    'author': 'Trustcode',
    'license': 'AGPL-3',
    'website': 'http://www.trustcode.com.br',
    'contributors': [
        'Danimar Ribeiro <danimaribeiro@gmail.com>',
    ],
    'depends': [
        'sale',
    ],
    'data': [
        'views/dashboards.xml',
    ],
    'instalable': True,
    'application': True,
}
