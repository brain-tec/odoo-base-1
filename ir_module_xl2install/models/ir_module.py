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
    

class module2install(models.TransientModel):
    _name = 'ir.module.install_wizard'
    _description = 'Modules to install'
    
    to_be_installed_modules_ids = fields.One2many(comodel_name='ir.module.install_wizard.to_be_installed', inverse_name='wizard_id', string='To Be Installed', readonly=True)
    missing_modules_ids = fields.One2many(comodel_name='ir.module.install_wizard.missing_module', inverse_name='wizard_id', string='To Be Installed', readonly=True)
    
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
            found_modules_obj = self.env['ir.module.module'].search([('name','in',wanted_modules),('state','!=','uninstallable')])
            found_modules = [m.name for m in found_modules_obj]
            missing_modules = [set(wanted_modules) - set(found_modules)]
            
            self.to_be_installed_modules_ids = False
            self.missing_modules_ids = False
           
                
            for found_module_id in found_modules_obj:
                self.env['ir.module.install_wizard.to_be_installed'].create({'name':found_module_id.name, 'wizard_id':self.id, 'module_id': found_module_id.id})
                

            # ~ for m in found_modules_obj:
                # ~ m.button_install()
                
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

