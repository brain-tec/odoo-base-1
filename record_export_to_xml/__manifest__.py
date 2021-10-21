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
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

{
    'name': 'Export Records to XML',
    'summary': 'Export Records to XML',
    'author': 'Vertel AB',
    'contributor': '',
    'maintainer': 'Vertel AB',
    'repository': 'https://github.com/vertelab/odoo-event.git',
    'category': 'Extra Tools',
    'version': '14.0.0.1.1',
    # Version ledger: 14.0 = Odoo version. 1 = Major. Non regressionable code. 2 = Minor. New features that are regressionable. 3 = Bug fixes
    'license': 'AGPL-3',
    'website': 'https://vertel.se/',
    'description': """
        Export Records to XML - Models you can import include: \n
            - users
            - contacts
            - sale orders
            - events
            - hr employee
            - project/tasks
        \n 14.0.0.1.1 - Added Documentations
    """,
    'depends': ['base', 'event', 'hr', 'sale', 'project'],
    'data': [
        "security/ir.model.access.csv",
        "views/export_view.xml",
        "data/data.xml",
    ],
    'installable': True,
    'auto_install': False,
}
