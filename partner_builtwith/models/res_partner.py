from odoo import models, fields, api, _
from datetime import date
import logging
from odoo.exceptions import ValidationError
from odoo.addons.partner_builtwith.tools.builtwith import builtwith, builtwith_sm, data, name2url, LogoScrape

_logger = logging.getLogger(__name__)



class ResPartnerMixin(models.AbstractModel):
    _name = "res.builtwith.mixin"
    
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
    bw_domain_name = fields.Char(string='Domain Name')
    bw_registrant_name = fields.Char(string='Registrant Name')
    bw_creation_date = fields.Datetime(string="Creation Date")
    bw_updated_date = fields.Datetime(string="Creation Date")
    bw_expiration_date = fields.Datetime(string="Expiration Date")
    bw_transfer_date = fields.Datetime(string="Transfer Date")
    bw_name_servers = fields.Text(string="Name Servers")
    bw_dnssec = fields.Char(string="Dnssec")
    bw_status = fields.Char(string="Status")
    bw_registrar = fields.Char(string="Registrar")
    # DNS/mail
    bw_dns_a = fields.Char(string="A")
    bw_dns_cname = fields.Char(string="CNAME")
    bw_dns_mx = fields.Text(string="MX")
    bw_dns_ns = fields.Text(string="NS")
    bw_dns_soa = fields.Char(string="SOA")
    bw_dns_txt = fields.Char(string="TXT")
    bw_mail_server = fields.Char(string="Mail Server")
    #Social media
    bw_brainville = fields.Char(string="Brainville")
    bw_facebook = fields.Char(string="Facebook")
    bw_github = fields.Char(string="Github")
    bw_instagram = fields.Char(string="Instagram")
    bw_linkedin = fields.Char(string="Linkedin")
    bw_linkopingsciencepark = fields.Char(string="Linköping Science Park")
    bw_myai = fields.Char(string="AI Sweden")
    bw_odoo_community = fields.Char(string="Odoo Community")
    bw_x = fields.Char(string="X")
    
    @api.model
    def name2website(self,name):
        website = [w for w in name2url(name) if not "allabolag" in w][0] 
        _logger.warning(f'{website=}')
        return website

    def bw_enrich(self):
        for p in self:
            bw = builtwith(p.website)
            bw,update(builtwith_sm(p.name))
            _logger.warning(f"{bw=}")

            rec = {}
            f = p.fields_get()
            # ~ _logger.warning(f"{f=}")

            for k in bw.keys():
                key = f'bw_{k}'.replace('-','_')
                key = key.replace('.','')
                _logger.warning(f"working with field {key=}  {bw[k]=} {type(bw[k])=}")

                if not key in f.keys():
                    _logger.warning(f"missing field {key=}")
                    continue
                # ~ _logger.warning(f"{key=} {bk=} {bw[bk]=}")
                _logger.warning(f"working with field {key=}  {bw[k]=}  {f[key]['type']=}  {type(bw[k])=}")

                if f[key]['type'] == 'char':
                    if type(bw[k]) == list:
                        rec[key] = ', '.join(bw[k])
                    else:
                        rec[key] = bw[k]
                elif f[key]['type'] in ['date','float','html','monetary','selection','text']:
                    rec[key] = bw[k]
                elif f[key]['type'] in ['Datetime','datetime']:
                    if type(bw[k]) == str:
                        rec[key] = bw[k]
                    else:
                        # ~ rec[key] = bw[k].strftime("%Y-%m-%d %H:%M:%S")
                        rec[key] = bw[k]
                else:
                    _logger.warning(f"{key=} {f[key]['type']=}")
                    
                        
                if f[key]['type'] == 'integer':
                    rec[key] = int(bw[k])
                
            # key in bw are same as field with underscrores 
            # eg marketing-automation -> bw_marketing_automation
            _logger.warning(f"{rec=}")

            p.write(rec)
            
            
   


    
class ResPartner(models.Model):
    _name = 'res.partner'
    _inherit = ["res.partner",'res.builtwith.mixin']

    def partner_enrich(self):
        _logger.warning(f"builtwith partner_enrich {self=}")
         
        for partner in self:
            if not partner.website:
                try:
                    partner.website = self.name2website(partner.name)
                except Exception as e:
                    partner.message_post(body=_(f'Could not get website for {partner.name}: {e}'), message_type='notification')
                    continue
            partner.bw_enrich()
            try:
                partner.image_1920 = LogoScrape(partner.website)
            except Exception as e:
                _logger.warning(f"LogoScrape error {e}")
                partner.message_post(body=_(f'Could not get logo for {partner.name}: {e}'), message_type='notification')
                
        super(ResPartner,self).partner_enrich()

    @api.model
    def enrich_company(self, company_domain, partner_gid, vat):
        res = {}
        _logger.warning(f"builtwith enrich_company {company_domain=} {partner_gid=} {vat=} {self=}")
        if COMPANY_NO_IAP == True:
            res = super(ResPartner, self).enrich_company(company_domain,partner_gid,vat)
        return res

