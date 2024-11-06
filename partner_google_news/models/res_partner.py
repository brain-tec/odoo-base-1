from odoo import models, fields, api, _
from datetime import date, datetime
import logging
from GoogleNews import GoogleNews
import base64
import requests


from odoo.exceptions import ValidationError
_logger = logging.getLogger(__name__)


TOPICS=[
    ("CAAqIggKIhxDQkFTRHdvSkwyMHZNR1F3ZG5GdUVnSnpkaWdBUAE",'Sverige'),
    ('CAAqJggKIiBDQkFTRWdvSUwyMHZNRFZxYUdjU0FuTjJHZ0pUUlNnQVAB','Huvudnyheter'),
    ('CAAqJggKIiBDQkFTRWdvSUwyMHZNRGx1YlY4U0FuTjJHZ0pUUlNnQVAB','Världen'),
    ('CAAqJggKIiBDQkFTRWdvSUwyMHZNRGx6TVdZU0FuTjJHZ0pUUlNnQVAB','Ekonomi'),
    ('CAAqKAgKIiJDQkFTRXdvSkwyMHZNR1ptZHpWbUVnSnpkaG9DVTBVb0FBUAE','Vetenskap/teknik'),
    ('CAAqJggKIiBDQkFTRWdvSUwyMHZNREpxYW5RU0FuTjJHZ0pUUlNnQVAB','Underhållning'),
    ('CAAqJggKIiBDQkFTRWdvSUwyMHZNRFp1ZEdvU0FuTjJHZ0pUUlNnQVAB',"Sport"),
    ('CAAqIQgKIhtDQkFTRGdvSUwyMHZNR3QwTlRFU0FuTjJLQUFQAQ','Hälsa'),
    ('CAAqIQgKIhtDQkFTRGdvSUwyMHZNRFp0ZUhNU0FuTjJLQUFQAQ','Lokalt (Stockholm)'),
    ('CAAqIQgKIhtDQkFTRGdvSUwyMHZNRE0wTTE4U0FuTjJLQUFQAQ','Lokalt (Göteborg)'),
    ('CAAqJQgKIh9DQkFTRVFvTEwyMHZNREV4YkRnNU5Ia1NBbk4yS0FBUAE','Lokalt (Malmö)'),
    ('CAAqKAgKIiJDQkFTRXdvTkwyY3ZNVEZ3ZUhsdWNtdHJaQklDYzNZb0FBUAE','Lokalt (Skåne)'),
    ('CAAqIQgKIhtDQkFTRGdvSUwyMHZNRGQwWTNNU0FuTjJLQUFQAQ','Lokalt (Uppsala)'),
    ('CAAqIggKIhxDQkFTRHdvSkwyMHZNRE42YW5kdEVnSnpkaWdBUAE','Lokalt (Örebro)'),
    ('CAAqIggKIhxDQkFTRHdvSkwyMHZNRE41YTJOMkVnSnpkaWdBUAE','Lokalt (Jönköping)'),
    ('CAAqKAgKIiJDQkFTRXdvTkwyY3ZNVEZ3ZUhseE5IZHFNaElDYzNZb0FBUAE','Lokalt (Östergötland)'),
    ('CAAqIQgKIhtDQkFTRGdvSUwyMHZNSHAzTVY4U0FuTjJLQUFQAQ','Lokalt (Linköping)'),
]

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
    
    def _news_record(self,article):
        if article['img'] == None:
            img = ''
        elif 'http' in article['img']:
            response = requests.get(article['img'], allow_redirects=True)
            if response.status_code == 200:
                encoded_image = base64.b64encode(response.content).decode('utf-8')
                img = f'<img src="data:image/png;base64,{encoded_image}"/>'
            else:
                img = ''
        else:
            img = f"<img src=\"{article['img']}\"/>"
        _logger.warning(f"{img=}")

        if article['link']:
            site = f"{article['site']} [{article['media']}]" if article['site'] else article['media']
            link = f"<a href=\"{article['link']}\"  target=\"_blank\">{site}</a>"
        else:
            link = ''
        _logger.warning(f"{link=}")
        if isinstance(article['datetime'],datetime):
            dt = article['datetime'].strftime('%Y%m%d %H:%M')
        else:
            dt = ''
        return f"""<h2>{article['title']}</h2>
    {img}
    <p>{article['desc'] if article['desc'] != None else ''}
    </p>
    <span>{dt}</span>
    <span>{link}</span><br/>
    <small>{article['reporter'] if article['reporter'] else ''}</small>
    """
    
    
    @api.model
    def google_news_cron(self):
        gn = GoogleNews(lang=self.env['ir.config_parameter'].sudo().get_param('partner_google_news.lang','sv'),
                        period=self.env['ir.config_parameter'].sudo().get_param('partner_google_news.period','1d'),
                        region=self.env['ir.config_parameter'].sudo().get_param('partner_google_news.region','SE'),
                        )
        all_news = []
        for topic in ['topic1','topic2','topic3','topic4']:
            topic_id = self.env['ir.config_parameter'].sudo().get_param(f'partner_google_news.{topic}',None)
            if topic_id:
                gn.set_topic(topic_id)
                gn.get_news()
                news = gn.results()
                all_news += news
        _logger.warning(f"{all_news=}  {len(all_news)=}")
        titles = '\n'.join([txt['title'] for txt in all_news])
        _logger.warning(f"{titles=}  {len(all_news)=}")
        for partner in self.env['res.partner'].search([]):
            for article in all_news:
                if partner.name in f"{article['title']}{article['desc']}":
                    _logger.warning(f"----------------> {partner.name=} {article=}")
                    partner.message_post(body=self._news_record(article),
                                            message_type="comment")
                    # ~ self.env['res.partner.news'].create({
                        # ~ 'gn_title': article['title'],
                        # ~ 'gn_desc': article['desc'],
                        # ~ 'gn_date': article['date'],
                        # ~ 'gn_datetime': article['datetime'],
                        # ~ 'gn_link': article['link'],
                        # ~ 'gn_img': article['img'],
                        # ~ 'gn_media': article['media'],
                        # ~ 'gn_site': article['site'],
                        # ~ 'gn_reporter': article['reporter'],
                    # ~ })
                    
# ~ import base64
# ~ import requests

# ~ def post_message_with_fetched_image(self):
    # ~ image_url = "https://www.example.com/path/to/your/image.png"
    # ~ link_url = "https://www.example.com"
    # ~ link_text = "Click here for more information"
    
    # Fetch the image
    # ~ response = requests.get(image_url, allow_redirects=True)
    # ~ if response.status_code == 200:
        # ~ encoded_image = base64.b64encode(response.content).decode('utf-8')
        # ~ image_html = f'<img src="data:image/png;base64,{encoded_image}"/>'
    # ~ else:
        # ~ image_html = f'<p>Failed to load image from {image_url}</p>'
    
    # ~ body_html = f"""
    # ~ <p>Your message text here.</p>
    # ~ <p>For additional details, <a href="{link_url}">{link_text}</a>.</p>
    # ~ {image_html}
    # ~ """
    
    # ~ self.message_post(
        # ~ body=body_html,
        # ~ message_type='comment',
        # ~ subtype='mail.mt_note'
    # ~ )


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'
    gn_topic1 = fields.Selection(selection=TOPICS,string='Topic 1', config_parameter='partner_google_news.topic1' )
    gn_topic2 = fields.Selection(selection=TOPICS,string='Topic 2', config_parameter='partner_google_news.topic2' )
    gn_topic3 = fields.Selection(selection=TOPICS,string='Topic 3', config_parameter='partner_google_news.topic3' )
    gn_topic4 = fields.Selection(selection=TOPICS,string='Topic 4', config_parameter='partner_google_news.topic4' )
    gn_topic5 = fields.Selection(selection=TOPICS,string='Topic 5', config_parameter='partner_google_news.topic5' )
    
    gn_lang = fields.Char(string='Language', default='sv', config_parameter='partner_google_news.lang')
    gn_period = fields.Char(string='Period', default='1d', config_parameter='partner_google_news.period')
    gn_region = fields.Char(string='Region', default='SE', config_parameter='partner_google_news.region')

    @api.model
    def get_values(self):
        res = super(ResConfigSettings, self).get_values()
        return res

    def set_values(self):
        super(ResConfigSettings, self).set_values()

