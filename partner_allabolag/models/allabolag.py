from odoo import models, fields, api, _
import logging

_logger = logging.getLogger(__name__)


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    # ~ sftp_bind = fields.Char(string='Document_SFTP Bind', config_parameter='sftp_bind')
    # ~ sftp_host_key = fields.Char(string='Document_SFTP Host key', config_parameter='sftp_host_key')

a ="""Översikt - Namn
Översikt - VD
Översikt - Bolagsform
Översikt - F-Skatt
Översikt - Moms
Översikt - Registreringsår
* Översikt - Besöksadress
* Översikt - Ort
* Översikt - Län
Översikt - account_figures_year
* Översikt - Omsättning
Översikt - Res. e. fin
* Översikt - Årets resultat
Översikt - Summa tillgångar
Aktivitet och status - 63910
Aktivitet och status - Status
Aktivitet och status - Bolaget registrerat
Aktivitet och status - F-Skatt
Aktivitet och status - Startdatum för F-Skatt
Aktivitet och status - Moms
Aktivitet och status - Startdatum för moms
Aktivitet och status - Bolagsform
Aktivitet och status - Ägandeförhållande
Aktivitet och status - Länsäte
Aktivitet och status - Kommunsäte
* Aktivitet och status - Verksamhet & ändamål
Aktivitet och status - SNI-kod
Aktivitet och status - SNI-bransch
Resultaträkning (tkr) - Nettoomsättning
Resultaträkning (tkr) - Övrig omsättning
Resultaträkning (tkr) - Rörelseresultat (EBIT)
Resultaträkning (tkr) - Resultat efter finansnetto
Resultaträkning (tkr) - Årets resultat
Balansräkningar (tkr) - Tillgångar
Balansräkningar (tkr) - Tecknat ej inbetalt kapital
Balansräkningar (tkr) - Anläggningstillgångar
Balansräkningar (tkr) - Omsättningstillgångar
Balansräkningar (tkr) - Skulder, eget kapital och avsättningar
Balansräkningar (tkr) - Eget kapital
Balansräkningar (tkr) - Obeskattade reserver
Balansräkningar (tkr) - Avsättningar (tkr)
Balansräkningar (tkr) - Långfristiga skulder
Balansräkningar (tkr) - Kortfristiga skulder
Balansräkningar (tkr) - Skulder och eget kapital
Löner & utdelning (tkr) - Löner till styrelse & VD
Löner & utdelning (tkr) - Varav tantiem till styrelse & VD
Löner & utdelning (tkr) - Löner till övriga anställda
Löner & utdelning (tkr) - Varav resultatlön till övriga anställda
Löner & utdelning (tkr) - Sociala kostnader
Löner & utdelning (tkr) - Utdelning till aktieägare
Löner & utdelning (tkr) - Omsättning
* Nycketal - Antal anställda
Nycketal - Nettoomsättning per anställd (tkr)
Nycketal - Personalkostnader per anställd (tkr)
Nycketal - Rörelseresultat, EBITDA
* Nycketal - Nettoomsättningförändring
Nycketal - Du Pont-modellen
* Nycketal - Vinstmarginal
Nycketal - Bruttovinstmarginal
Nycketal - Rörelsekapital/omsättning
* Nycketal - Soliditet
* Nycketal - Kassalikviditet"""
