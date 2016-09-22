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

    @http.route('/twilio/response', type='http', auth="public",
                cors="*", csrf=False)
    def dial_customer(self, **post):
        response = twiml.Response()
        with response.dial(callerId=TWILIO_NUMBER) as dial:
            dial.number(post['To'])
        response = str(response)
        print response
        return response

    @http.route('/twilio/token', type='json', auth="public", cors="*")
    def generate_token(self):
        capability = TwilioCapability(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

        # Allow our users to make outgoing calls with Twilio Client
        capability.allow_client_outgoing(TWIML_APPLICATION_SID)

        # Generate the capability token
        token = capability.generate()
        return token
