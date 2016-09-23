# -*- coding: utf-8 -*-
# © 2016 Danimar Ribeiro, Trustcode
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).


from odoo import api, fields, models


class ResCompany(models.Model):
    _inherit = 'res.company'

    twilio_account_sid = fields.Char(string="SID Twilio")
    twilio_auth_token = fields.Char(string="Token Twilio")
    twilio_number = fields.Char(string="Twilio Número")
    twiml_application = fields.Char(string="Id Aplicação Twiml")
