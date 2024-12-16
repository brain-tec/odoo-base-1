# -*- coding: utf-8 -*-
from odoo import models, modules, fields, api, _
import odoo

import os
from odoo.tools.parse_version import parse_version
from odoo.addons.base.models.ir_module import assert_log_admin_access
# from odoo.odoo.modules.module import _DEFAULT_MANIFEST

import odoo.tools as tools

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
            manifest_file = os.path.join(mod_path, '__manifest__.py')

            if not os.path.isfile(manifest_file):
                return {}

            manifest = copy.deepcopy(_DEFAULT_MANIFEST)

            # Handle icon path
            icon_path = os.path.join(mod_path, 'static', 'description', 'icon.png')
            manifest['icon'] = f"/{module}/static/description/icon.png" if os.path.exists(icon_path) else None

            try:
                with open(manifest_file, 'r') as f:
                    manifest.update(ast.literal_eval(f.read()))
            except Exception as e:
                _logger.error("Error loading manifest for %s: %s", module, e)
                return {}

            if not manifest.get('license'):
                manifest['license'] = 'LGPL-3'

            if isinstance(manifest['auto_install'], collections.abc.Iterable):
                manifest['auto_install'] = set(manifest['auto_install'])
                non_dependencies = manifest['auto_install'].difference(manifest['depends'])
                assert not non_dependencies, \
                    "auto_install triggers must be dependencies, found " \
                    "non-dependencies [%s] for module %s" % (
                        ', '.join(non_dependencies), module
                    )
            elif manifest['auto_install']:
                manifest['auto_install'] = set(manifest['depends'])

            try:
                manifest['version'] = modules.adapt_version(manifest['version'])
            except ValueError as e:
                if manifest.get("installable", True):
                    raise ValueError(f"Module {module}: invalid manifest") from e

            manifest['addons_path'] = os.path.dirname(mod_path)
            return manifest

        def my_get_modules(directory):
            if not os.path.exists(directory):
                return []

            def is_module(name):
                manifest_path = os.path.join(directory, name, '__manifest__.py')
                return os.path.isfile(manifest_path)

            try:
                return [
                    name for name in os.listdir(directory)
                    if os.path.isdir(os.path.join(directory, name)) and is_module(name)
                ]
            except OSError:
                return []

        def my_update_list(directory):
            res = [0, 0]  # [update, add]

            default_version = modules.adapt_version('1.0')
            known_mods = self.with_context(lang=None).search([])
            known_mods_names = {mod.name: mod for mod in known_mods}

            # Add directory to odoo.addons.__path__ temporarily
            if directory not in odoo.addons.__path__:
                odoo.addons.__path__.append(directory)

            for mod_name in my_get_modules(directory):
                mod = known_mods_names.get(mod_name)
                mod_path = os.path.join(directory, mod_name)
                terp = my_load_manifest(mod_name, mod_path)

                if not terp:
                    continue

                values = self.get_values_from_terp(terp)

                if mod:
                    updated_values = {}
                    for key in values:
                        old = getattr(mod, key)
                        if (old or values[key]) and values[key] != old:
                            updated_values[key] = values[key]
                    if terp.get('installable', True) and mod.state == 'uninstallable':
                        updated_values['state'] = 'uninstalled'
                    if parse_version(terp.get('version', default_version)) > parse_version(
                        mod.latest_version or default_version):
                        res[0] += 1
                    if updated_values:
                        mod.write(updated_values)
                else:
                    state = "uninstalled" if terp.get('installable', True) else "uninstallable"
                    try:
                        mod = self.create(dict(name=mod_name, state=state, **values))
                        res[1] += 1
                    except Exception as e:
                        _logger.error("Failed to create module %s: %s", mod_name, e)
                        continue

                try:
                    mod._update_dependencies(terp.get('depends', []))
                    mod._update_exclusions(terp.get('excludes', []))
                    mod._update_category(terp.get('category', 'Uncategorized'))
                except Exception as e:
                    _logger.error("Failed to update dependencies for %s: %s", mod_name, e)

            return res

        addons_directory = os.path.join(os.path.dirname(tools.config.addons_data_dir), self.env.cr.dbname)
        if os.path.exists(addons_directory):
            _logger.info("Found database-specific addons directory: %s", addons_directory)
            my_update_list(addons_directory)

        return super().update_list()
