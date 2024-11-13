from odoo import models, fields, api, _

class ResUsers(models.Model):
    _inherit = "res.users"

    allow_email_marketing = fields.Boolean(related="partner_id.allow_email_marketing", string="Tillåt e-postmarknadsföring", readonly=False)
