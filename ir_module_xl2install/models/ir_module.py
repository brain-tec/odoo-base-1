# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import UserError
from odoo import http
import base64
from datetime import datetime
import odoo



from openpyxl import load_workbook
from xlrd import open_workbook, XLRDError
from xlrd.book import Book
from xlrd.sheet import Sheet

import sys

import logging

_logger = logging.getLogger(__name__)

class module2installMissingModule(models.TransientModel):
    _name = 'ir.module.install_wizard.missing_module'
    name = fields.Char()
    wizard_id = fields.Many2one('ir.module.install_wizard')  
      
    
class module2installToBeInstalled(models.TransientModel):
    _name = 'ir.module.install_wizard.to_be_installed'
    name = fields.Char()
    module_id = fields.Many2one('ir.module.module')  
    wizard_id = fields.Many2one('ir.module.install_wizard')
    state = fields.Selection(related='module_id.state', readonly=True)

class module2installMissingModuleEnterprise(models.TransientModel):
    _name = 'ir.module.install_wizard.enterprise'
    name = fields.Char()
    module_id = fields.Many2one('ir.module.module')  
    wizard_id = fields.Many2one('ir.module.install_wizard')
    state = fields.Selection(related='module_id.state', readonly=True)
    

class module2install(models.TransientModel):
    _name = 'ir.module.install_wizard'
    _description = 'Modules to install'

    ee_modules = ['documents_project_sale', 'account_accountant', 'web_studio', 'documents_fsm', 'l10n_account_customer_statements', 'crm_enterprise', 'account_saft', 'hr_holidays_contract_gantt', 'web_map', 'account_disallowed_expenses', 'planning_contract', 'web_cohort', 'website_event_social', 'sale_account_accountant', 'account_reports_tax_reminder', 'account_batch_payment', 'hr_appraisal_skills', 'social_sale', 'mrp_maintenance', 'l10n_be_reports_post_wizard', 'room', 'l10n_mx_reports_closing', 'test_mail_enterprise', 'mrp_workorder_plm', 'industry_fsm_report', 'website_appointment_sale', 'l10n_be_codabox_bridge_wizard', 'l10n_us_1099', 'delivery_bpost', 'documents_hr', 'l10n_in_reports_gstr_spreadsheet', 'test_web_gantt', 'whatsapp_account', 'l10n_ma_reports', 'website_helpdesk_slides_forum', 'project_enterprise', 'product_unspsc', 'mrp_mps', 'l10n_br_edi_services', 'social_facebook', 'industry_fsm_sale_subscription', 'l10n_au_hr_payroll', 'social_test_full', 'l10n_ee_reports', 'stock_barcode_quality_mrp', 'l10n_lt_intrastat', 'project_account_asset', 'l10n_in_hr_payroll', 'l10n_us_reports', 'l10n_lu_hr_payroll', 'hr_referral', 'purchase_mrp_workorder_quality', 'sign_itsme', 'l10n_co_reports', 'whatsapp_delivery', 'documents_l10n_ke_hr_payroll', 'whatsapp_sale', 'hr_work_entry_contract_planning_attendance', 'helpdesk_fsm_sale', 'l10n_au_hr_payroll_account', 'l10n_lt_hr_payroll', 'stock_barcode', 'contacts_enterprise', 'web_enterprise', 'website_sale_dashboard', 'account_asset_fleet', 'l10n_nl_reports_sbr', 'l10n_cl_edi_stock', 'mail_enterprise', 'voip_onsip', 'website_enterprise', 'website_sale_ups', 'l10n_tn_reports', 'l10n_ch_hr_payroll', 'sale_loyalty_taxcloud', 'pos_hr_mobile', 'l10n_ae_hr_payroll_account', 'l10n_es_real_estates', 'pos_self_order_iot', 'hr_attendance_gantt', 'l10n_eu_oss_reports', 'account_invoice_extract', 'appointment_google_calendar', 'mrp_subcontracting_studio', 'delivery_shiprocket', 'helpdesk_sale_timesheet', 'knowledge', 'pos_order_tracking_display', 'sale_management_renting', 'website_sale_renting_product_configurator', 'hr_payroll_planning', 'l10n_be_hr_payroll_sd_worx', 'documents', 'l10n_ca_reports', 'documents_project_sign', 'pos_iot', 'spreadsheet_dashboard_sale_subscription', 'l10n_br_avatax', 'l10n_bg_reports', 'spreadsheet_dashboard_crm', 'helpdesk_fsm_report', 'approvals_purchase', 'pos_restaurant_preparation_display', 'sale_account_taxcloud', 'social_demo', 'l10n_in_reports_gstr', 'project_enterprise_hr', 'l10n_nl_hr_payroll', 'l10n_zm_reports', 'delivery_dhl', 'documents_l10n_hk_hr_payroll', 'documents_project', 'l10n_fi_reports', 'l10n_in_qr_code_bill_scan', 'quality_mrp_workorder', 'website_sale_external_tax', 'l10n_in_documents', 'social', 'hr_work_entry_contract_enterprise', 'mail_mobile', 'account_reports', 'hr_payroll_expense', 'account_sepa', 'l10n_mx_edi_stock', 'timesheet_grid_holidays', 'base_automation_hr_contract', 'l10n_be_hr_payroll_account', 'website_helpdesk_sale_loyalty', 'mrp_workorder_iot', 'project_hr_payroll_account', 'l10n_sa_hr_payroll_account', 'sale_intrastat', 'l10n_sk_hr_payroll', 'l10n_se_reports', 'pos_settle_due', 'l10n_mz_reports', 'delivery_easypost', 'l10n_nl_reports_sbr_ob_nummer', 'website_appointment', 'hr_payroll_account_sepa', 'project_sale_subscription', 'l10n_ae_hr_payroll', 'account_asset', 'l10n_be_hr_payroll_dimona', 'account_avatax_stock', 'l10n_ec_reports', 'l10n_lt_saft_import', 'hr_payroll', 'planning_holidays', 'hr_work_entry_contract_attendance', 'l10n_dk_reports', 'l10n_tw_reports', 'event_social', 'helpdesk_account', 'l10n_sa_hr_payroll', 'whatsapp', 'worksheet', 'spreadsheet_dashboard_account_accountant', 'website_crm_iap_reveal_enterprise', 'l10n_fr_hr_payroll_account', 'whatsapp_event', 'website_helpdesk', 'helpdesk_stock', 'l10n_cl_edi', 'analytic_enterprise', 'l10n_br_edi', 'l10n_br_reports', 'social_instagram', 'l10n_nl_hr_payroll_account', 'digest_enterprise', 'website_helpdesk_slides', 'l10n_in_reports', 'l10n_se_sie_import', 'l10n_mx_xml_polizas', 'website_sale_renting', 'stock_barcode_picking_batch', 'website_event_track_gantt', 'test_data_cleaning', 'pos_iot_six', 'project_timesheet_forecast_sale', 'l10n_dk_edi', 'l10n_be_us_consolidation_demo', 'mrp_plm', 'snailmail_account_followup', 'documents_spreadsheet', 'l10n_pe_edi_stock', 'delivery_usps', 'pos_account_reports', 'documents_hr_expense', 'website_studio', 'quality_mrp_workorder_worksheet', 'sale_mrp_renting', 'partner_commission', 'spreadsheet_dashboard_documents', 'l10n_hk_hr_payroll_account', 'account_disallowed_expenses_fleet', 'test_timer', 'account_consolidation', 'account_avatax', 'l10n_au_reports', 'l10n_lt_hr_payroll_account', 'sale_renting', 'helpdesk_timesheet', 'l10n_au_keypay', 'whatsapp_pos', 'mrp_subcontracting_quality', 'hr_payroll_account', 'l10n_de_pos_cert', 'l10n_ec_reports_ats', 'appointment_account_payment', 'voip', 'l10n_pk_reports', 'sale_amazon', 'spreadsheet_edition', 'l10n_generic_coa', 'l10n_in_hr_payroll_account', 'currency_rate_live', 'voip_crm', 'test_rental_product_configurators', 'hr_payroll_holidays', 'hr_expense_predict_product', 'crm_enterprise_partner_assign', 'whatsapp_website_sale', 'payment_sepa_direct_debit', 'website_appointment_account_payment', 'account_budget', 'l10n_be_codabox', 'documents_hr_payroll', 'mrp_workorder_hr_account', 'appointment_crm', 'website_documents', 'test_web_cohort', 'stock_barcode_quality_control', 'l10n_mx_edi_stock_extended', 'data_merge_project', 'pos_l10n_se', 'l10n_lt_saft', 'quality', 'l10n_be_codabox_bridge', 'account_bank_statement_import_camt', 'industry_fsm_sale', 'l10n_be_intrastat', 'helpdesk_sms', 'account_auto_transfer', 'helpdesk_repair', 'data_merge_crm', 'sale_renting_crm', 'l10n_th_reports', 'l10n_ar_reports', 'stock_account_enterprise', 'mrp_subcontracting_enterprise', 'marketing_automation_sms', 'l10n_ch_reports', 'test_l10n_ch_hr_payroll_account', 'l10n_pl_reports', 'l10n_ro_hr_payroll_account', 'l10n_de_reports', 'documents_hr_contract', 'l10n_nl_reports_sbr_status_info', 'spreadsheet_dashboard_hr_contract', 'account_intrastat', 'documents_hr_holidays', 'project_helpdesk', 'crm_helpdesk', 'appointment', 'l10n_cl_edi_pos', 'l10n_be_disallowed_expenses', 'l10n_din5008_industry_fsm', 'mrp_subcontracting_account_enterprise', 'helpdesk_sale_loyalty', 'l10n_be_reports_sms', 'l10n_dk_saft_import', 'account_external_tax', 'documents_approvals', 'l10n_mx_edi_landing', 'account_taxcloud', 'pos_sale_stock_renting', 'l10n_mx_edi_website_sale', 'hr_recruitment_extract', 'data_merge', 'pos_blackbox_be', 'l10n_hk_hr_payroll', 'hr_work_entry_holidays_enterprise', 'hr_contract_salary_payroll', 'l10n_mx_edi_stock_extended_30', 'l10n_si_reports', 'quality_control_worksheet', 'test_appointment_full', 'iot', 'documents_sign', 'l10n_es_reports', 'sale_stock_renting', 'stock_barcode_mrp', 'l10n_mx_edi_pos', 'whatsapp_payment', 'iap_extract', 'sale_subscription_external_tax', 'l10n_mx_edi_stock_30', 'delivery_ups', 'industry_fsm_sale_report', 'l10n_us_hr_payroll', 'l10n_uk_customer_statements', 'account_accountant_fleet', 'website_twitter_wall', 'website_knowledge', 'approvals_purchase_stock', 'spreadsheet_dashboard_edition', 'l10n_be_coda', 'hr_contract_salary', 'l10n_tr_reports', 'l10n_rs_reports', 'account_invoice_extract_purchase', 'l10n_ro_reports', 'purchase_intrastat', 'l10n_pl_hr_payroll_account', 'l10n_din5008_sale_renting', 'account_bacs', 'l10n_din5008_account_followup', 'pos_preparation_display', 'quality_mrp', 'account_avatax_sale', 'sign', 'account_bank_statement_import_qif', 'test_sale_subscription', 'helpdesk_stock_account', 'sale_purchase_inter_company_rules', 'account_reports_cash_basis', 'sale_external_tax', 'pos_restaurant_appointment', 'appointment_hr', 'account_inter_company_rules', 'pos_enterprise', 'sale_amazon_taxcloud', 'sale_subscription_stock', 'website_sale_fedex', 'mrp_workorder', 'industry_fsm_stock', 'project_enterprise_hr_contract', 'l10n_at_saft', 'sale_loyalty_taxcloud_delivery', 'social_twitter', 'stock_enterprise', 'pos_pricer', 'l10n_mx_hr_payroll', 'spreadsheet_dashboard_helpdesk', 'l10n_fr_hr_payroll', 'account_accountant_batch_payment', 'l10n_ca_check_printing', 'l10n_mx_reports', 'test_web_studio', 'web_mobile', 'l10n_do_reports', 'l10n_br_edi_sale_services', 'helpdesk_mail_plugin', 'helpdesk', 'event_enterprise', 'test_l10n_be_hr_payroll_account', 'pos_self_order_preparation_display', 'l10n_lt_reports', 'l10n_hu_reports', 'l10n_ie_reports', 'l10n_pe_edi', 'data_cleaning', 'test_marketing_automation', 'website_helpdesk_knowledge', 'l10n_pl_reports_pos_jpk', 'documents_hr_recruitment', 'hr_contract_reports', 'test_discuss_full_enterprise', 'stock_barcode_product_expiry', 'documents_account', 'marketing_automation_crm', 'helpdesk_fsm', 'l10n_mx_edi', 'l10n_my_reports', 'l10n_ke_hr_payroll', 'l10n_it_reports', 'l10n_be_hr_payroll', 'l10n_lu_hr_payroll_account', 'l10n_br_sale_subscription', 'social_linkedin', 'account_bank_statement_import_csv', 'l10n_be_soda', 'delivery_ups_rest', 'l10n_co_edi', 'hr_recruitment_reports', 'industry_fsm_sms', 'l10n_be_hr_payroll_attendance', 'mrp_workorder_expiry', 'hr_appraisal_survey', 'test_website_sale_full', 'hr_expense_extract', 'helpdesk_holidays', 'website_appointment_crm', 'data_merge_helpdesk', 'marketing_automation', 'delivery_sendcloud', 'l10n_be_hr_contract_salary', 'sale_ebay', 'l10n_mx_edi_extended', 'l10n_cl_edi_website_sale', 'hr_work_entry_contract_planning', 'account_saft_import', 'l10n_cz_reports', 'l10n_hr_reports', 'website_sale_stock_renting', 'sale_planning', 'web_grid', 'website_event_twitter_wall', 'hr_payroll_fleet', 'hr_contract_salary_holidays', 'website_delivery_sendcloud', 'project_forecast', 'l10n_bo_reports', 'l10n_be_reports', 'spreadsheet_dashboard_hr_referral', 'sale_amazon_avatax', 'website_helpdesk_livechat', 'delivery_iot', 'l10n_ar_edi', 'l10n_ke_reports', 'quality_mrp_workorder_iot', 'website_event_track_social', 'l10n_de_pos_res_cert', 'planning_hr_skills', 'l10n_us_payment_nacha', 'frontdesk', 'project_account_budget', 'hr_contract_sign', 'account_bank_statement_import', 'l10n_be_account_disallowed_expenses_fleet', 'spreadsheet_dashboard_mrp_account', 'documents_fleet', 'social_push_notifications', 'sale_timesheet_enterprise', 'sale_renting_sign', 'l10n_lu_reports', 'l10n_sk_hr_payroll_account', 'stock_barcode_mrp_subcontracting', 'spreadsheet_dashboard_stock', 'test_l10n_us_hr_payroll_account', 'spreadsheet_dashboard_hr_payroll', 'industry_fsm', 'sale_timesheet_enterprise_holidays', 'website_sale_subscription', 'l10n_at_reports', 'l10n_in_reports_gstr_pos', 'l10n_nl_intrastat', 'sale_subscription', 'stock_accountant', 'documents_l10n_be_hr_payroll', 'l10n_fr_reports', 'account_avatax_geolocalize', 'stock_barcode_quality_control_picking_batch', 'l10n_ma_hr_payroll', 'l10n_dz_reports', 'l10n_mx_hr_payroll_account', 'l10n_ph_reports', 'maintenance_worksheet', 'hr_holidays_gantt', 'hr_gantt', 'timer', 'delivery_fedex', 'hr_recruitment_sign', 'account_3way_match', 'web_gantt', 'timesheet_grid', 'social_youtube', 'account_online_synchronization', 'planning', 'hr_mobile', 'account_winbooks_import', 'account_bank_statement_import_ofx', 'data_merge_utm', 'approvals', 'project_holidays', 'l10n_mn_reports', 'l10n_mx_edi_sale', 'quality_control_picking_batch', 'documents_spreadsheet_account', 'l10n_es_sale_amazon', 'mass_mailing_sale_subscription', 'account_sepa_direct_debit', 'mrp_accountant', 'l10n_be_hr_payroll_fleet', 'account_base_import', 'l10n_nl_reports_sbr_icp', 'l10n_us_check_printing', 'website_sale_account_taxcloud', 'hr_appraisal_contract', 'website_helpdesk_forum', 'l10n_ec_edi', 'documents_product', 'quality_iot', 'l10n_br_edi_sale', 'l10n_pt_reports', 'l10n_ro_hr_payroll', 'l10n_ro_saft', 'hr_payroll_attendance', 'l10n_uk_reports', 'l10n_ke_hr_payroll_account', 'mrp_account_enterprise', 'test_whatsapp', 'documents_spreadsheet_crm', 'l10n_kz_reports', 'l10n_br_avatax_services', 'l10n_sg_reports', 'l10n_us_hr_payroll_account', 'l10n_fr_fec_import', 'documents_l10n_ch_hr_payroll', 'sale_project_forecast', 'sale_subscription_taxcloud', 'l10n_ch_hr_payroll_account', 'l10n_ro_saft_import', 'l10n_au_aba', 'test_spreadsheet_edition', 'l10n_nl_reports', 'account_followup', 'l10n_pe_reports', 'helpdesk_sale', 'project_timesheet_forecast', 'l10n_pl_hr_payroll', 'data_merge_stock_account', 'appointment_hr_recruitment', 'l10n_syscohada_reports', 'delivery_starshipit', 'l10n_no_reports', 'test_l10n_hk_hr_payroll_account', 'l10n_cl_edi_boletas', 'l10n_gr_reports', 'l10n_cl_reports', 'l10n_br_test_avatax_sale', 'quality_control', 'spreadsheet_dashboard_sale_renting', 'l10n_cl_edi_exports', 'hr_appraisal', 'appointment_sms', 'quality_control_iot', 'l10n_ma_hr_payroll_account', 'social_crm', 'l10n_no_saft', 'pos_online_payment_self_order_preparation_display', 'stock_intrastat', 'website_generator']
        
    to_be_installed_modules_ids = fields.One2many(comodel_name='ir.module.install_wizard.to_be_installed', inverse_name='wizard_id', string='To Be Installed', readonly=True)
    missing_modules_ids = fields.One2many(comodel_name='ir.module.install_wizard.missing_module', inverse_name='wizard_id', string='To Be Installed', readonly=True)
    missing_modules_enterprise_ids = fields.One2many(comodel_name='ir.module.install_wizard.enterprise', inverse_name='wizard_id', string='Missing Enterprise Modules', readonly=True)
    
    data = fields.Binary('File')
    filename = fields.Char(string='Filename')
    state = fields.Selection([('choose', 'choose'), ('get', 'get'), ], default="choose")
    result = fields.Text()
    import_message = fields.Text()
    
    
    def import_module(self):
        self.ensure_one()
        IrModule = self.env['ir.module.module']
        zip_data = base64.decodebytes(self.module_file)
        fp = BytesIO()
        fp.write(zip_data)
        # ~ res = IrModule._import_zipfile(fp, force=self.force, with_demo=self.with_demo)
        return {
            'type': 'ir.actions.act_url',
            'target': 'self',
            'url': '/web',
        }
    def install_modules(self):
         self.to_be_installed_modules_ids.module_id.button_immediate_install()
         #self.to_be_installed_modules_ids.module_id.button_immediate_upgrade()
         return {
                'type': 'ir.actions.act_window',
                'res_model': 'ir.module.install_wizard',
                'view_mode': 'form',
                'res_id': self.id,
                'target': 'new',
                'flags': {'mode': 'edit'},
          }
     
    
    def send_form(self):
        self.ensure_one()

        if self.data:  # IMPORT TRIGGERED
            data_file = base64.decodebytes(self.data)
            
            try:
                xldata = open_workbook(file_contents=data_file).sheet_by_index(0)
            except XLRDError as e:
                _logger.error(u'Could not read file (SEB Kontohändelser.xlsx)')
                raise ValueError(e)
            pos = [i for i,c in enumerate(xldata.row(0)) if c.value.lower() in ["tekniskt namn","technical name"]]
            if len(pos) == 1:
                pos = pos[0]
            else:
                raise UserWarning(_('You should have a colume for Technical Name'))
            wanted_modules = [xldata.cell(r+1,pos).value.lower() for r in range(xldata.nrows-1)]
            found_modules_obj = self.env['ir.module.module'].search([('name','in',wanted_modules)])
            found_modules = [m.name for m in found_modules_obj]
            missing_modules = [set(wanted_modules) - set(found_modules)]
            
            self.to_be_installed_modules_ids = False
            self.missing_modules_ids = False
           
                
            for found_module_id in found_modules_obj:
                if found_module_id.state != "uninstallable":
                   self.env['ir.module.install_wizard.to_be_installed'].create({'name':found_module_id.name, 'wizard_id':self.id, 'module_id': found_module_id.id})
                else:
                    self.env['ir.module.install_wizard.enterprise'].create({'name':found_module_id.name, 'wizard_id':self.id, 'module_id': found_module_id.id})
                
            if missing_modules:
               for missing_module in missing_modules[0]:
                    self.env['ir.module.install_wizard.missing_module'].create({'name':missing_module, 'wizard_id':self.id})
               self.import_message = f"""
Missing Modules.
            """
            
            return {
                'type': 'ir.actions.act_window',
                'res_model': 'ir.module.install_wizard',
                'view_mode': 'form',
                'res_id': self.id,
                'target': 'new',
                'flags': {'mode': 'edit'},
            }


            # ~ return {
                    # ~ 'type': 'ir.actions.client',
                    # ~ 'tag': 'display_notification',
                    # ~ 'params': {
                        # ~ 'title': "Missing Accounts",
                        # ~ 'message': self.import_message ,
                        # ~ 'sticky': False,
                    # ~ }
             # ~ }
            
        
  


class Module(models.Model):
    _inherit = "ir.module.module"





    # ~ @assert_log_admin_access
    # ~ def button_install(self):
        # ~ # domain to select auto-installable (but not yet installed) modules
        # ~ auto_domain = [('state', '=', 'uninstalled'), ('auto_install', '=', True)]

        # ~ # determine whether an auto-install module must be installed:
        # ~ #  - all its dependencies are installed or to be installed,
        # ~ #  - at least one dependency is 'to install'
        # ~ install_states = frozenset(('installed', 'to install', 'to upgrade'))
        # ~ def must_install(module):
            # ~ states = {dep.state for dep in module.dependencies_id if dep.auto_install_required}
            # ~ return states <= install_states and 'to install' in states

        # ~ modules = self
        # ~ while modules:
            # ~ # Mark the given modules and their dependencies to be installed.
            # ~ modules._state_update('to install', ['uninstalled'])

            # ~ # Determine which auto-installable modules must be installed.
            # ~ modules = self.search(auto_domain).filtered(must_install)

        # ~ # the modules that are installed/to install/to upgrade
        # ~ install_mods = self.search([('state', 'in', list(install_states))])

        # ~ # check individual exclusions
        # ~ install_names = {module.name for module in install_mods}
        # ~ for module in install_mods:
            # ~ for exclusion in module.exclusion_ids:
                # ~ if exclusion.name in install_names:
                    # ~ raise UserError(_('Modules %r and %r are incompatible.', module.shortdesc, exclusion.exclusion_id.shortdesc))

        # ~ # check category exclusions
        # ~ def closure(module):
            # ~ todo = result = module
            # ~ while todo:
                # ~ result |= todo
                # ~ todo = todo.dependencies_id.depend_id
            # ~ return result

        # ~ exclusives = self.env['ir.module.category'].search([('exclusive', '=', True)])
        # ~ for category in exclusives:
            # ~ # retrieve installed modules in category and sub-categories
            # ~ categories = category.search([('id', 'child_of', category.ids)])
            # ~ modules = install_mods.filtered(lambda mod: mod.category_id in categories)
            # ~ # the installation is valid if all installed modules in categories
            # ~ # belong to the transitive dependencies of one of them
            # ~ if modules and not any(modules <= closure(module) for module in modules):
                # ~ labels = dict(self.fields_get(['state'])['state']['selection'])
                # ~ raise UserError(
                    # ~ _('You are trying to install incompatible modules in category %r:%s', category.name, ''.join(
                        # ~ f"\n- {module.shortdesc} ({labels[module.state]})"
                        # ~ for module in modules
                    # ~ ))
                # ~ )

        # ~ return dict(ACTION_DICT, name=_('Install'))

    # ~ @assert_log_admin_access
    # ~ def button_immediate_install(self):
        # ~ """ Installs the selected module(s) immediately and fully,
        # ~ returns the next res.config action to execute

        # ~ :returns: next res.config item to execute
        # ~ :rtype: dict[str, object]
        # ~ """
        # ~ _logger.info('User #%d triggered module installation', self.env.uid)
        # ~ # We use here the request object (which is thread-local) as a kind of
        # ~ # "global" env because the env is not usable in the following use case.
        # ~ # When installing a Chart of Account, I would like to send the
        # ~ # allowed companies to configure it on the correct company.
        # ~ # Otherwise, the SUPERUSER won't be aware of that and will try to
        # ~ # configure the CoA on his own company, which makes no sense.
        # ~ if request:
            # ~ request.allowed_company_ids = self.env.companies.ids
        # ~ return self._button_immediate_function(self.env.registry[self._name].button_install)

