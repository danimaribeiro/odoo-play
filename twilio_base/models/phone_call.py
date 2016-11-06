# -*- coding: utf-8 -*-
# © 2016 Danimar Ribeiro, Trustcode
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).


from odoo import api, fields, models


class PhoneCall(models.Model):
    _name = 'phone.call'

    identifier = fields.Char(string="Identificador", size=60)
    name = fields.Char(string="Descrição")

    from_number = fields.Char(string="De")
    to_number = fields.Char(string="Para")
    caller_city = fields.Char(string="Cidade")
    caller_state = fields.Char(string="Estado")
    caller_country = fields.Char(string="País")
    duration = fields.Integer(string="Duração")

    partner_id = fields.Many2one('res.partner', string="Parceiro")
    start_date = fields.Datetime(string="Data de Inicio")
    end_date = fields.Datetime(string="Data de Inicio")

    type = fields.Selection([('in', 'Entrada'),
                             ('out', 'Saída')], string="Tipo")

    state = fields.Selection([('incoming', 'Recebendo'),
                              ('incall', 'Em chamada'),
                              ('finished', 'Finalizada'),
                              ('not_answered', 'Não atendida'),
                              ('error_on_call', 'Erro na ligação')],
                             string="Situação")

    def register_new_call(self, **data):
        call = self.search([('identifier', '=', data["CallSid"])])
        if not call:
            call = self.create({
                'identifier': data["CallSid"],
                'name': 'Chamada',
                'type': "out" if "client" in data["From"] else "in",
                'state': 'incoming',
                'from_number': data.get("From", False),
                'to_number': data.get("To", False),
                'caller_city': data.get("CallerCity", False),
                'caller_state': data.get("CallerState", False),
                'caller_country': data.get("CallerCountry", False),
            })
        if call.type == "in":
            users = self.env['res.users'].search([])
            for user in users:
                if user.im_status == 'online':
                    user.notify_twilio_call(
                        "Nova chamada de %s" % call.from_number)
        return call

    def update_call_status(self, **data):
        call = self.search([('identifier', '=', data["CallSid"])])
        if data["CallStatus"] == 'completed':
            call.write({
                'state': 'finished',
                'duration': int(data["CallDuration"])
            })
