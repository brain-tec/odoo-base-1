from odoo import models, fields, api, _
from odoo.addons.partner_autocomplete.models.res_company import COMPANY_AC_TIMEOUT
from datetime import date
import logging
from odoo.exceptions import ValidationError

COMPANY_NO_IAP=True


_logger = logging.getLogger(__name__)


class ResPartner(models.Model):
    _inherit = 'res.partner'

    def partner_enrich(self):
        _logger.warning(f"allabolag partner_enrich {self=}")
        for partner in self:
            _logger.warning(f'partner_enrich_base {partner.name=}')
        if hasattr(super(ResPartner, self), 'partner_enrich'):
            super(ResPartner, self).partner_enrich()

        pass
        
        
    @api.model
    def orgnr2vat(self,company_registry):
        if company_registry:
            return f"SE{company_registry.replace('-','')}01"
        else:
            return None
   
    def enrich_company(self, company_domain, partner_gid, vat,timeout=COMPANY_AC_TIMEOUT): # Override IAP-version
        res = {}
        if COMPANY_NO_IAP == True:
            res = super(ResPartner, self).enrich_company(company_domain,partner_gid,vat)
        return res
