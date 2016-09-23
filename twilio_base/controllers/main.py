# -*- coding: utf-8 -*-
# © 2016 Danimar Ribeiro, Trustcode
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import http
from odoo.http import request
from twilio import twiml
from twilio.util import TwilioCapability

TWILIO_ACCOUNT_SID = 'AC28b3af7006b1c34c483fd3660736a614'
TWILIO_AUTH_TOKEN = 'e2813de3989ecfdc64b37194a2ac1dca'
TWILIO_NUMBER = '+554840420303'
TWIML_APPLICATION_SID = 'AP319ae6c0e61a11b8dd9199ca56790dbb'


class TokenTwilio(http.Controller):

    @http.route('/twilio/agent', type='http', auth="public",
                cors="*", csrf=False)
    def dial_agent(self, **post):
        print post
        response = twiml.Response()
        with response.dial(callerId=TWILIO_NUMBER) as dial:
            dial.client('support_agent')
        return str(response)

    @http.route('/twilio/response', type='http', auth="public",
                cors="*", csrf=False)
    def dial_customer(self, **post):
        print post
        musica = 'http://demo.twilio.com/hellomonkey/monkey.mp3'

        response = twiml.Response()

        if post["Direction"] == 'inbound' and post["CallStatus"] == 'ringing':
            response.enqueue('Fila', waitUrl='http://0e0fe08c.ngrok.io/twilio/response')
            return str(response)
        if post["Direction"] == 'inbound' and post["CallStatus"] == 'in-progress':
            if int(post['QueueTime']) > 10:

                response.redirect(url='http://0e0fe08c.ngrok.io/twilio/agent')
                return str(response)

            response.play(url=musica)
            return str(response)

        with response.dial(callerId=TWILIO_NUMBER) as dial:
            dial.number(post['To'])
        return str(response)

    @http.route('/twilio/token', type='json', auth="public", cors="*")
    def generate_token(self):
        capability = TwilioCapability(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

        # Allow our users to make outgoing calls with Twilio Client
        capability.allow_client_outgoing(TWIML_APPLICATION_SID)
        capability.allow_client_incoming('support_agent')

        # Generate the capability token
        token = capability.generate()
        return token
