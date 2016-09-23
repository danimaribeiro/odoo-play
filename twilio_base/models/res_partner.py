# -*- coding: utf-8 -*-
# © 2016 Danimar Ribeiro, Trustcode
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).


from twilio.rest import TwilioRestClient
from odoo import api, models


class ResPartner(models.Model):
    _inherit = 'res.partner'

    @api.multi
    def notify_by_sms(self, message=None, raise_error=False):
        twilio_client = TwilioRestClient(
            self.env.user.company_id.twilio_account_sid,
            self.env.user.company_id.twilio_auth_token)

        for partner in self:
            twilio_client.messages.create(
                body=message,
                to=(partner.mobile or partner.phone),
                from_=self.env.user.company_id.twilio_number)

    @api.multi
    def write(self, vals):
        self.env.user.notify_twilio_call(
            'Recebendo chamada de Danimar Ribeiro (+55 (48) 9801-6226)',
            sticky=True)
        return super(ResPartner, self).write(vals)
