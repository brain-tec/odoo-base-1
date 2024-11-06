# File: your_module/controllers/signup.py
from odoo import http
from odoo.addons.auth_signup.controllers.main import AuthSignupHome
from odoo.http import request

import logging
_logger = logging.getLogger(__name__)

class SignupExtended(AuthSignupHome):

    def do_signup(self, qcontext):
        # Capture allow_email_marketing field value
        allow_email_marketing = qcontext.get('allow_email_marketing') == 'true'

        # Call the original do_signup method to handle standard fields
        super(SignupExtended, self).do_signup(qcontext)

        # Get the user record and update the partner's allow_email_marketing field
        if request.params.get("allow_email_marketing"):
            _logger.info("allow_email_marketing is True")
            user = request.env['res.users'].sudo().search([('login', '=', qcontext.get('login'))], limit=1)
            if user:
                user.partner_id.sudo().write({'allow_email_marketing': True})
