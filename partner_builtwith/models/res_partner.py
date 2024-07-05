from odoo import models, fields, api, _
from datetime import date
import logging
from odoo.exceptions import ValidationError
from odoo.addons.partner_builtwith.tools.builtwith import builtwith, data, name2url

_logger = logging.getLogger(__name__)


class ResPartner(models.Model):
    _inherit = "res.partner"
    
    # ~ data['categories']
    bw_analytics = fields.Char(string='Analytics')
    bw_blogs = fields.Char(string='Blogs')
    bw_cache_tools = fields.Char(string='Cache Tools')
    bw_cdn = fields.Char(string='CDN')
    bw_cms = fields.Char(string='CMS')
    bw_database_managers = fields.Char(string='Database Managers')
    bw_databases = fields.Char(string='Databases')
    bw_documentation_tools = fields.Char(string='Documentation Tools')
    bw_ecommerce = fields.Char(string='Ecommerce')
    bw_font_scripts = fields.Char(string='Font Scripts')
    bw_issue_trackers = fields.Char(string='Issue Trackers')
    bw_javascript_frameworks = fields.Char(string='Javascript Frameworks')
    bw_lms = fields.Char(string='LMS')
    bw_marketing_automation = fields.Char(string='Marketing Automation')
    bw_miscellaneous = fields.Char(string='Miscellaneous')
    bw_mobile_frameworks = fields.Char(string='Mobile Frameworks')
    bw_operating_systems = fields.Char(string='Operating Systems')
    bw_programming_languages = fields.Char(string='Programming Languages')
    bw_search_engines = fields.Char(string='Search Engines')
    bw_web_frameworks = fields.Char(string='Web Frameworks')
    bw_web_mail = fields.Char(string='Web Mail')
    bw_web_servers = fields.Char(string='Web Servers')
    bw_wikis = fields.Char(string='Wikis')
    # whois
    #{'domain_name': 'vertel.se', 
    bw_registrant_name = fields.Char(string='Registrant Name')
    bw_creation_date = fields.DateTime(string="Creation Date")
    bw_updated_date = fields.DateTime(string="Creation Date")
    bw_expiration_date = fields.DateTime(string="Expiration Date")
    bw_transfer_date = fields.DateTime(string="Transfer Date")
    bw_name_servers = fields.Char(string="Name Servers")
    bw_dnssec = fields.DateTime(string="Dnssec")
    bw_status = fields.Char(string="Status")
    bw_registrar = fields.DateTime(string="Registrar")
            
    def bw_enrich(self):
        for p in self:
            # ~ _logger.warning(f"{p.fields_get()=}")
            
# ~ 'type': 'char'
# ~ 'type': 'date'
# ~ 'type': 'datetime'
# ~ 'type': 'float'
# ~ 'type': 'html'
# ~ 'type': 'integer'
# ~ 'type': 'many2many'
# ~ 'type': 'many2one'
# ~ 'type': 'monetary'
# ~ 'type': 'one2many'
# ~ 'type': 'selection'

            if not p.website:
                p.website = name2url(p.name)
            
            bw = builtwith(p.website)
            _logger.warning(f"{bw=}")

            rec = {}
            f = p.fields_get()
            # ~ _logger.warning(f"{f=}")

            for k in bw.keys():
                key = f'bw_{k}'.replace('-','_')
                if not key in f.keys():
                    continue
                # ~ _logger.warning(f"{key=} {bk=} {bw[bk]=}")
                if f[key]['type'] == 'char':
                    if type(bw[k]) == list:
                        rec[key] = ', '.join(bw[k])
                    else:
                        rec[key] = bw[k]
                if f[key]['type'] in ['date','datetime','float','html','monetary','selection']:
                    rec[key] = bw[k]
                if f[key]['type'] == 'integer':
                    rec[key] = int(bw[k])
                
            _logger.warning(f"{rec=}")
            # key in bw are same as field with underscrores 
            # eg marketing-automation -> bw_marketing_automation
            p.write(rec)
            if bw['image_1920']:
                p.image_1920 = bw['image_1920']
            
        # ~ p.fields_get()={
            # ~ 'name': {'type': 'char', 'change_default': False, 'company_dependent': False, 'depends': (), 'manual': False, 'readonly': False, 'required': False, 'searchable': True, 'sortable': True, 'store': True, 'string': 'Name', 'translate': False, 'trim': True}, 
        # ~ }

