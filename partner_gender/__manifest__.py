# -*- coding: utf-8 -*-
##############################################################################
#
#    Odoo SA, Open Source Management Solution, third party addon
#    Copyright (C) 2021- Vertel AB (<https://vertel.se>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program. If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

{
    'name': 'Base: Partner Gender',
    'summary': 'Adds a "Personal information" tab on res_partners with a gender field.',
    'author': 'Vertel AB',
    'contributor': '',
    'maintainer': 'Vertel AB',
    'repository': 'https://github.com/vertelab/odoo-base.git',
    'category': 'Customer Relationship Management',
    'version': '14.0.0.1',
    # Version ledger: 14.0 = Odoo version. 1 = Major. Non regressionable code. 2 = Minor. New features that are regressionable. 3 = Bug fixes
    'license': 'AGPL-3',
    'website': 'https://vertel.se/apps/base',
    'description': """
        Features:\n
        * Adds a "Personal information" tab on res_partners with a gender field.\n
        * Adds an select box for gender on personal details form in the user portal.\n
        This module is maintained from: https://github.com/vertelab/odoo-base/\n
    """,
    'depends': ['partner_ssn', 'website_contact_management'],
    'data': [
        'views/res_partner.xml',
        'views/templates.xml',
    ],
    'installable': True,
}
