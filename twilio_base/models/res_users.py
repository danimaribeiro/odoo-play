# -*- coding: utf-8 -*-
# © 2016 Danimar Ribeiro, Trustcode
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import api, fields, models, _


class ResUsers(models.Model):
    _inherit = 'res.users'

    @api.multi
    @api.depends('create_date')
    def _compute_channel_names(self):
        for record in self:
            res_id = record.id
            record.twilio_call_channel = 'notify_twilio_call_%s' % res_id

    twilio_call_channel = fields.Char(
        compute='_compute_channel_names')

    @api.multi
    def notify_twilio_call(self, message, title=None, sticky=False):
        title = title or _('Nova chamada')
        self._notify_channel(
            'notify_twilio_call_channel_name', message, title, sticky)

    @api.multi
    def _notify_channel(self, channel_name_field, message, title, sticky):
        bus_message = {
            'message': message,
            'title': title,
            'sticky': sticky,
            'call_id': 5,
        }
        notifications = [(record.twilio_call_channel, bus_message)
                         for record in self]
        self.env['bus.bus'].sendmany(notifications)
