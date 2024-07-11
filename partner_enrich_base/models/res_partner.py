from odoo import models, fields, api, _
from datetime import date
import logging
from odoo.exceptions import ValidationError
from odoo.addons.partner_builtwith.tools.builtwith import builtwith, data, name2url

_logger = logging.getLogger(__name__)



    # -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

import logging
import json
from odoo import api, fields, models, exceptions, _
from odoo.addons.iap.tools import iap_tools
# TDE FIXME: check those errors at iap level ?
from requests.exceptions import ConnectionError, HTTPError

_logger = logging.getLogger(__name__)

DEFAULT_ENDPOINT = 'https://partner-autocomplete.odoo.com'
COMPANY_NO_IAP=True

class ResPartner(models.Model):
    _inherit = 'res.partner'

    def partner_enrich(self):
        pass
        
        
    @api.model
    def orgnr2vat(self,company_registry):
        return f"SE{company_registry.replace('-','')}01"
        
    @api.model
    def _rpc_remote_api(self, action, params, timeout=15):
        _logger.warning(f"_rpc_remote_api {action=} {params=}")
        return [],'No IAP'
        #return super(ResPartner, self)._rpc_remote_api(action, params, timeout)

    @api.model
    def autocomplete(self, query):
        _logger.warning(f"autocomplete {query=}")
        return super(ResPartner, self).autocomplete_override(query)

    @api.model
    def read_by_vat(self, vat):
        _logger.warning(f"read_by_vat {vat=}")
        # ~ return super(ResPartner, self).read_by_vat(vat)
        return []

    @api.model
    def enrich_company(self, company_domain, partner_gid, vat):
        res = {}
        if COMPANY_NO_IAP == True:
            res = super(ResPartner, self).enrich_company(company_domain,partner_gid,vat)
        return res

    # ~ def _is_synchable(self):
        # ~ already_synched = self.env['res.partner.autocomplete.sync'].search([('partner_id', '=', self.id), ('synched', '=', True)])
        # ~ return self.is_company and self.partner_gid and not already_synched

    # ~ def _update_autocomplete_data(self, vat):
        # ~ self.ensure_one()
        # ~ if vat and self._is_synchable() and self._is_vat_syncable(vat):
            # ~ self.env['res.partner.autocomplete.sync'].sudo().add_to_queue(self.id)

    # ~ @api.model_create_multi
    # ~ def create(self, vals_list):
        # ~ partners = super(ResPartner, self).create(vals_list)
        # ~ if len(vals_list) == 1:
            # ~ partners._update_autocomplete_data(vals_list[0].get('vat', False))
            # ~ if partners.additional_info:
                # ~ template_values = json.loads(partners.additional_info)
                # ~ template_values['flavor_text'] = _("Partner created by Odoo Partner Autocomplete Service")
                # ~ partners.message_post_with_view(
                    # ~ 'iap_mail.enrich_company',
                    # ~ values=template_values,
                    # ~ subtype_id=self.env.ref('mail.mt_note').id,
                # ~ )
                # ~ partners.write({'additional_info': False})

        # ~ return partners

    # ~ def write(self, values):
        # ~ res = super(ResPartner, self).write(values)
        # ~ if len(self) == 1:
            # ~ self._update_autocomplete_data(values.get('vat', False))

        # ~ return res
