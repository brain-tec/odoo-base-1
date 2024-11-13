from odoo import models, fields, api, _

class ResPartner(models.Model):
    _inherit = "res.partner"

    allow_email_marketing = fields.Boolean(string="Tillåt e-postmarknadsföring")
