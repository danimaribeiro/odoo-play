# -*- coding: utf-8 -*-
# © 2016 Danimar Ribeiro, Trustcode
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).


from odoo import api, fields, models


class PhoneCall(models.Model):
    _name = 'phone.call'

    name = fields.Char(string="Descrição")
    partner_id = fields.Many2one('res.partner', string="Parceiro")

    start_date = fields.Datetime(string="Data de Inicio")
    end_date = fields.Datetime(string="Data de Inicio")

    type = fields.Selection([('incoming', 'Entrada'),
                             ('outgoing', 'Saída')], string="Tipo")

    state = fields.Selection([('incoming', 'Recebendo'),
                              ('incall', 'Em chamada'),
                              ('finished', 'Finalizada'),
                              ('not_answered', 'Não atendida'),
                              ('error_on_call', 'Erro na ligação')],
                             string="Situação")
