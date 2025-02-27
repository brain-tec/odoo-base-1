from odoo import models, fields, api, _
from odoo.exceptions import UserError, AccessError, ValidationError
import logging

_logger = logging.getLogger(__name__)

class ConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    active_paying_users = fields.Integer(compute="_compute_active_paying_users")

    @api.depends('company_id')
    def _compute_active_paying_users(self):
        res_users_count = self.env["res.users"].search_count([("login", "!=", "admin")])
        for record in self:
            record.active_paying_users = res_users_count
