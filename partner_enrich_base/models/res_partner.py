from odoo import models, fields, api, _
from datetime import date
import logging
from odoo.exceptions import ValidationError

COMPANY_NO_IAP=True


_logger = logging.getLogger(__name__)


class ResPartner(models.Model):
    _inherit = 'res.partner'

    def partner_enrich(self):
        pass
        
        
    @api.model
    def orgnr2vat(self,company_registry):
        if company_registry:
            return f"SE{company_registry.replace('-','')}01"
        else:
            return None
        
    def enrich_company(self, company_domain, partner_gid, vat): # Override IAP-version
        res = {}
        if COMPANY_NO_IAP == True:
            res = super(ResPartner, self).enrich_company(company_domain,partner_gid,vat)
        return res
