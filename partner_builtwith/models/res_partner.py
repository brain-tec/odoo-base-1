from odoo import models, fields, api, _
from datetime import date
import logging
from odoo.exceptions import ValidationError
from odoo.addons.partner_builtwith.tools.builtwith import builtwith, data

_logger = logging.getLogger(__name__)


class ResPartner(models.Model):
    _inherit = "res.partner"
    
    # ~ data['categories']
    bw_analytics = fields.Char(string='CMS')
    bw_blogs = fields.Char(string='CMS')
    bw_cache_tools = fields.Char(string='CMS')
    bw_cdn = fields.Char(string='CMS')
    bw_cms = fields.Char(string='CMS')
    bw_database_managers = fields.Char(string='CMS')
    bw_databases = fields.Char(string='Databases')
    bw_documentation_tools = fields.Char(string='CMS')
    bw_ecommerce = fields.Char(string='CMS')
    bw_font_scripts = fields.Char(string='CMS')
    bw_issue_trackers = fields.Char(string='CMS')
    bw_javascript_frameworks = fields.Char(string='CMS')
    bw_lms = fields.Char(string='CMS')
    bw_marketing_automation = fields.Char(string='Marketing Automation')
    bw_miscellaneous = fields.Char(string='Miscellaneous')
    bw_mobile_frameworks = fields.Char(string='CMS')
    bw_operating_systems = fields.Char(string='CMS')
    bw_programming_languages = fields.Char(string='CMS')
    bw_search_engines = fields.Char(string='CMS')
    bw_web_frameworks = fields.Char(string='CMS')
    bw_web_mail = fields.Char(string='CMS')
    bw_web_servers = fields.Char(string='CMS')
    bw_wikis = fields.Char(string='CMS')
        
    @api.model
    def name2website(self,name):
        return 'https://vertel.se'
    
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
            
            bw = builtwith(p.website or self.name2website(p.name))
            _logger.warning(f"{bw=}")

            rec = {}
            f = p.fields_get()
            # ~ _logger.warning(f"{f=}")

            for k in bw.keys():
                key = f'bw_{k}'.replace('-','_')
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
            
        # ~ p.fields_get()={
            # ~ 'name': {'type': 'char', 'change_default': False, 'company_dependent': False, 'depends': (), 'manual': False, 'readonly': False, 'required': False, 'searchable': True, 'sortable': True, 'store': True, 'string': 'Name', 'translate': False, 'trim': True}, 
        # ~ }

