from odoo import models, fields, api, _
from datetime import date
import logging
from GoogleNews import GoogleNews

from odoo.exceptions import ValidationError
_logger = logging.getLogger(__name__)

class ResPartnerNews(models.Model):
    _name = 'res.partner.news'

    partner_id = fields.Many2one(comodel_name='res.parter',string="Partner",help="") # domain|context|ondelete="'set null', 'restrict', 'cascade'"|auto_join|delegate
    gn_title = fields.Char(string='Title', size=64, trim=True, )
    gn_desc = fields.Text(string='Description')
    gn_date = fields.Char(string='When', size=64, trim=True, )
    gn_datetime = fields.Datetime(string='Date',default=fields.Datetime.now()) # fields.datetime.add|context_timestamp|end_of|now|start_of|substract|to_datetime|to_string|today
    gn_link = fields.Char(string='Link', size=64, trim=True, )
    gn_img = fields.Binary(string="Image")
    gn_media = fields.Char(string='Media', size=64, trim=True, )
    gn_site = fields.Char(string='Site', size=64, trim=True, )
    gn_reporter = fields.Char(string='Reporter', size=64, trim=True, )


class ResPartner(models.Model):
    _inherit = 'res.partner'

    partner_news_ids = fields.One2many(comodel_name='res.partner.news',inverse_name='partner_id',string="News",help="") # domain|context|auto_join|limit
    
    @api.model
    def google_news_cron(self):
        gn = GoogleNews(lang=self.env['ir.config_parameter'].sudo().get_param('partner_google_news.lang'),
                        period=self.env['ir.config_parameter'].sudo().get_param('partner_google_news.period'))
        gn.set_topic(self.env['ir.config_parameter'].sudo().get_param('partner_google_news.topic1'))
        gn.set_topic(self.env['ir.config_parameter'].sudo().get_param('partner_google_news.topic2'))
        gn.set_topic(self.env['ir.config_parameter'].sudo().get_param('partner_google_news.topic3'))
        gn.set_topic(self.env['ir.config_parameter'].sudo().get_param('partner_google_news.topic4'))
        gn.get_news()
        news = gn.results()
        _logger.warning(f"{news=}")
        for partner in self.env['res.partner'].search([]):
            for article in news:
                if partner.name in article['title'] or partner.name in article['desc']:
                    _logger.warning(f"{partner.name=} {article=}")
                    self.env['res.partner.news'].create({
                        'gn_title': article['title'],
                        'gn_desc': article['desc'],
                        'gn_date': article['date'],
                        'gn_datetime': article['datetime'],
                        'gn_link': article['link'],
                        'gn_img': article['img'],
                        'gn_media': article['media'],
                        'gn_site': article['site'],
                        'gn_reporter': article['reporter'],
                    })


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    gn_topic1 = fields.Char(string='Topic 1', size=100, trim=True, config_parameter='partner_google_news.topic1' )
    gn_topic2 = fields.Char(string='Topic 2', size=100,trim=True, config_parameter='partner_google_news.topic2')
    gn_topic3 = fields.Char(string='Topic 3', size=100,trim=True, config_parameter='partner_google_news.topic3')
    gn_topic4 = fields.Char(string='Topic 4', size=100,trim=True, config_parameter='partner_google_news.topic4')
    
    gn_lang = fields.Char(string='Language', default='sv', config_parameter='partner_google_news.lang')
    gn_period = fields.Char(string='Period', default='1d', config_parameter='partner_google_news.period')

    @api.model
    def get_values(self):
        res = super(ResConfigSettings, self).get_values()
        return res

    def set_values(self):
        super(ResConfigSettings, self).set_values()

