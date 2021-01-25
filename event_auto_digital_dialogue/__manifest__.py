# -*- coding: utf-8 -*-
##############################################################################
#
#    Odoo, Open Source Management Solution, third party addon
#    Copyright (C) 2004-2019 Vertel AB (<http://vertel.se>).
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
    'name': 'Replace Event Automatic Digital Dialogue',
    'version': '12.0.0.0.2',       
    'category': '',
    'description': """
Module that changes event view to an automatic digital dialogue view
================================================================================================
This module alters, adds and removes fields in the event view \n
Replace by:\n
https://github.com/vertelab/odoo-af/tree/Dev-12.0-Fenix-Sprint-02/af_automatic_customer_dialogue/static/description
""",
    'author': 'Vertel AB',
    'license': 'AGPL-3',
    'website': 'http://www.vertel.se',
    'depends': ['website_event', 'event'],
    'data': [
			'views/event_event.xml'
        ],
    'application': False,
    'installable': True,
}
