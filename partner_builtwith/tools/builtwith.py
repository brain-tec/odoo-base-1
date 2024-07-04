from builtwith import builtwith as bw, data
from odoo.addons.partner_builtwith.tools.logoscrape import LogoScrape
from googlesearch import search
from whois


# ~ from dns import resolver

def builtwith(url, headers=None, html=None, user_agent='builtwith'):
    """Detect the technology used to build a website

    >>> builtwith('http://wordpress.com') 
    {u'blogs': [u'PHP', u'WordPress'], u'font-scripts': [u'Google Font API'], u'web-servers': [u'Nginx'], u'javascript-frameworks': [u'Modernizr'], u'programming-languages': [u'PHP'], u'cms': [u'WordPress']}
    >>> builtwith('http://webscraping.com') 
    {u'javascript-frameworks': [u'jQuery', u'Modernizr'], u'web-frameworks': [u'Twitter Bootstrap'], u'web-servers': [u'Nginx']}
    >>> builtwith('http://microsoft.com') 
    {u'javascript-frameworks': [u'jQuery'], u'mobile-frameworks': [u'jQuery Mobile'], u'operating-systems': [u'Windows Server'], u'web-servers': [u'IIS']}
    >>> builtwith('http://jquery.com') 
    {u'cdn': [u'CloudFlare'], u'web-servers': [u'Nginx'], u'javascript-frameworks': [u'jQuery', u'Modernizr'], u'programming-languages': [u'PHP'], u'cms': [u'WordPress'], u'blogs': [u'PHP', u'WordPress']}
    >>> builtwith('http://joomla.org') 
    {u'font-scripts': [u'Google Font API'], u'miscellaneous': [u'Gravatar'], u'web-servers': [u'LiteSpeed'], u'javascript-frameworks': [u'jQuery'], u'programming-languages': [u'PHP'], u'web-frameworks': [u'Twitter Bootstrap'], u'cms': [u'Joomla'], u'video-players': [u'YouTube']}
    """
    techs = {}
    
    
    res = bw(url,headers,html,user_agent)
    
    # ~ res['image_1920'] = LogoScrape(url)
    
    # Whois - registrar + ns
    # w = whois.whois('vertel.se')
    #{'domain_name': 'vertel.se', 'registrant_name': 'andkre4798-00001', 'creation_date': datetime.datetime(2004, 7, 14, 0, 0), 'updated_date': datetime.datetime(2024, 6, 3, 0, 0), 'expiration_date': datetime.datetime(2025, 7, 14, 0, 0), 'transfer_date': datetime.datetime(2019, 2, 14, 0, 0), 'name_servers': ['ns1.kreawit.se 79.99.1.214', 'ns2.kreawit.se 81.216.50.110'], 'dnssec': 'unsigned delegation', 'status': 'ok', 'registrar': 'Loopia AB'}

    
    
    # MX
    
    return res




def name2url(name):
    return [a for a in search(name)][0]

    

def get_mailserver():
    answers = dns.resolver.resolve('vertel.se', 'MX')
    for rdata in answers:
        print('Host', rdata.exchange, 'has preference', rdata.preference)
