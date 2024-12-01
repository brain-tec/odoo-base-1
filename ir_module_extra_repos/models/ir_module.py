# -*- coding: utf-8 -*-
from odoo import models, modules, fields, api, _
from odoo.exceptions import UserError
import odoo

import os
from os.path import join as opj, normpath

import odoo.tools as tools
import odoo.release as release
from odoo.tools import pycompat
from odoo.tools.misc import file_path
# ~ from odoo.modules import _DEFAULT_MANIFEST

import collections.abc
import copy
import ast

import logging
_logger = logging.getLogger(__name__)

_DEFAULT_MANIFEST = {
    #addons_path: f'/path/to/the/addons/path/of/{module}',  # automatic
    'application': False,
    'bootstrap': False,  # web
    'assets': {},
    'author': 'Odoo S.A.',
    'auto_install': False,
    'category': 'Uncategorized',
    'configurator_snippets': {},  # website themes
    'countries': [],
    'data': [],
    'demo': [],
    'demo_xml': [],
    'depends': [],
    'description': '',
    'external_dependencies': {},
    #icon: f'/{module}/static/description/icon.png',  # automatic
    'init_xml': [],
    'installable': True,
    'images': [],  # website
    'images_preview_theme': {},  # website themes
    #license, mandatory
    'live_test_url': '',  # website themes
    'new_page_templates': {},  # website themes
    #name, mandatory
    'post_init_hook': '',
    'post_load': '',
    'pre_init_hook': '',
    'sequence': 100,
    'summary': '',
    'test': [],
    'update_xml': [],
    'uninstall_hook': '',
    'version': '1.0',
    'web': False,
    'website': '',
}




class Module(models.Model):
    _inherit = "ir.module.module"

    def update_list(self):
        
        def my_load_manifest(module, mod_path):
            """ Load the module manifest from the file system. """


            manifest_file = f"{mod_path}/{module}/__manifest__.py"
            
            manifest = copy.deepcopy(_DEFAULT_MANIFEST)
            manifest['icon'] = f"{module}/static/description/icon.png"

            with tools.file_open(manifest_file, mode='r') as f:
                manifest.update(ast.literal_eval(f.read()))
            if not manifest.get('license'):
                manifest['license'] = 'LGPL-3'
        

            # auto_install is either `False` (by default) in which case the module
            # is opt-in, either a list of dependencies in which case the module is
            # automatically installed if all dependencies are (special case: [] to
            # always install the module), either `True` to auto-install the module
            # in case all dependencies declared in `depends` are installed.
            if isinstance(manifest['auto_install'], collections.abc.Iterable):
                manifest['auto_install'] = set(manifest['auto_install'])
                non_dependencies = manifest['auto_install'].difference(manifest['depends'])
                assert not non_dependencies,\
                    "auto_install triggers must be dependencies, found " \
                    "non-dependencies [%s] for module %s" % (
                        ', '.join(non_dependencies), module
                    )
            elif manifest['auto_install']:
                manifest['auto_install'] = set(manifest['depends'])

            try:
                manifest['version'] = adapt_version(manifest['version'])
            except ValueError as e:
                if manifest.get("installable", True):
                    raise ValueError(f"Module {module}: invalid manifest") from e
            manifest['addons_path'] = normpath(opj(mod_path, os.pardir))

            return manifest
        
        
        def my_get_modules(dir):
            """Returns the list of module names
            """
            def listdir(dir):
                def is_really_module(name):
                    if os.path.isfile(opj(dir, name, '__manifest__.py')):
                        return True
                return [
                    it
                    for it in os.listdir(dir)
                    if is_really_module(it)
                ]

            plist = []
            plist.extend(listdir(dir))
            return sorted(set(plist))
        
        def my_update_list(dir):
            res = [0, 0]    # [update, add]

            default_version = modules.adapt_version('1.0')
            known_mods = self.with_context(lang=None).search([])
            known_mods_names = {mod.name: mod for mod in known_mods}

            # iterate through detected modules and update/create them in db
            for mod_name in my_get_modules(dir):
                mod = known_mods_names.get(mod_name)
                terp = my_load_manifest(mod_name,dir)
                values = self.get_values_from_terp(terp)

                if mod:
                    updated_values = {}
                    for key in values:
                        old = getattr(mod, key)
                        if (old or values[key]) and values[key] != old:
                            updated_values[key] = values[key]
                    if terp.get('installable', True) and mod.state == 'uninstallable':
                        updated_values['state'] = 'uninstalled'
                    if parse_version(terp.get('version', default_version)) > parse_version(mod.latest_version or default_version):
                        res[0] += 1
                    if updated_values:
                        mod.write(updated_values)
                else:
                    mod_path = dir # modules.get_module_path(mod_name)
                    _logger.warning(f"{terp=}   {mod_path=}")
                    if not mod_path or not terp:
                        continue
                    state = "uninstalled" if terp.get('installable', True) else "uninstallable"
                    mod = self.create(dict(name=mod_name, state=state, **values))
                    res[1] += 1

                mod._update_from_terp(terp)

            return res
        
        # Magic direcotry if this exists and /var/lib/odoo/.local/share/Odoo/addons/<database>
        # /var/lib/odoo/.local/share/Odoo/addons/<database> missing in addons_path
        # then add this directory and all modules for just this database
        # maybe odoo.addons.__path__ are a global? we just want to add ir.module.modules for this database
        # os.path.dirname(tools.config.addons_data_dir) == /var/lib/odoo/.local/share/Odoo/addons/
        addons_directory = f"{os.path.dirname(tools.config.addons_data_dir)}/{self.env.cr.dbname}"
        _logger.warning(f"{addons_directory=}")
        if os.path.exists(addons_directory):
            _logger.warning(f"{addons_directory=} found")
            res = my_update_list(addons_directory)
            _logger.warning(f"{res=}")
        return super(Module, self).update_list()
