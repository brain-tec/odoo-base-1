from odoo import models, fields, api, _


class ResPartner(models.Model):
    _inherit = "res.partner"

    allow_email_marketing = fields.Selection([
        ('ja', 'Ja'), ('nej', 'Nej')], string="Tillåt e-postmarknadsföring",
        readonly=False
    )


