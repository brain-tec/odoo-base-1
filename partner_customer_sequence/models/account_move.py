from odoo import models, fields, api, _
import logging
_logger = logging.getLogger(__name__)

class AccountMove(models.Model):
    _inherit = 'account.move'

    customer_sequence = fields.Char(related='partner_id.customer_sequence',string='Customer Number', readonly=True)
    company_code_partner = fields.Char(related='partner_id.company_code_partner', string='Customer Code')
    invoice_adress = fields.Char(related='partner_id.name',string='Invoice address')
    vendor = fields.Char(related='partner_id.parent_name',string='Vendor')
