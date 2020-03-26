# -*- coding: utf-8 -*-
##############################################################################
#
#    Odoo, Open Source Management Solution, third party addon
#    Copyright (C) 2004-2019 Vertel AB (<http://vertel.se>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

from odoo import models, fields, api, _
import logging
_logger = logging.getLogger(__name__)


class ResPartner(models.Model):
    _inherit = "res.partner" 
    
    job_ids = fields.One2many(comodel_name="res.partner.jobs", inverse_name="partner_id")


    
class Jobs(models.Model):
    _name = 'res.partner.jobs'

    partner_id = fields.Many2one(comodel_name="res.partner")
    
    name = fields.Many2one('res.ssyk', string="Job title") 
    ssyk_code = fields.Char(string="SSYK", related="name.code")
    education = fields.Boolean(string="Education") #kan expanderas till modul i framtiden så att den visar utbildningen
    experience = fields.Boolean(string="Experience")
    
    #skills = fields.Many2many('hr.skill', string="Experience") #potentiell expansion istället för endast checkbox som då bör vara separerat från kompetenser på nått sätt, kanske göra utökning på hr_skill? Visa nivå och beskrivning

