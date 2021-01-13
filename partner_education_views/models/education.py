from odoo import models, fields


class ResPartnerEducation(models.Model):
    _name = "res.partner.education"

    partner_ids = fields.Many2many(comodel_name="res.partner")
    sun_id = fields.Many2one(comodel_name='res.sun',
                               string='SUN Code')
    education_level_id = fields.Many2one(
        comodel_name="res.partner.education.education_level",
        string="Education level")
    foreign_education = fields.Boolean(string="Foreign education")
    foreign_education_approved = fields.Boolean(
        string="Foreign education approved")