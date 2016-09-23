# -*- coding: utf-8 -*-
# © 2016 Danimar Ribeiro, Trustcode
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    'name': 'Integração Twilio',
    'summary': """Integração com o Twilio""",
    'description': """Efetua e recebe ligações telefônicas no Odoo
    através do Twilio - Mantido por Trustcode""",
    'version': '10.0.1.0.0',
    'category': 'CRM',
    'author': 'Trustcode',
    'license': 'AGPL-3',
    'website': 'http://www.trustcode.com.br',
    'contributors': [
        'Danimar Ribeiro <danimaribeiro@gmail.com>',
    ],
    'depends': [
        'crm',
    ],
    'data': [
        'views/twilio_base.xml',
        'views/res_company.xml',
        'views/res_partner.xml',
    ],
    'qweb': ['static/src/xml/twilio_base.xml'],
    'instalable': True,
    'application': True,
}
