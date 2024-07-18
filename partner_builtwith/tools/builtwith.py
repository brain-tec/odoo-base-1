from builtwith import builtwith as bw, data
from odoo.addons.partner_builtwith.tools.logoscrape import LogoScrape
from googlesearch import search
from whois import whois
from urllib.parse import urlparse
from dns.resolver import resolve
import smtplib
import socket
import logging
_logger = logging.getLogger(__name__)
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
    
    _logger.warning(f'{url=}')    
    res = bw(url,headers,html,user_agent)
    _logger.warning(f'{res=}')
    # ~ res = {}
    res['image_1920'] = LogoScrape(url)
    domain = '.'.join(urlparse(url).netloc.split('.')[-2:])
    _logger.warning(f'{domain=}')
    w = whois(domain)
    _logger.warning(f'whois {w}')
    res.update(whois(domain))
    
    
    # ~ # Whois - registrar + ns
    # ~ # w = whois.whois('vertel.se')
    # ~ #{'domain_name': 'vertel.se', 'registrant_name': 'andkre4798-00001', 'creation_date': datetime.datetime(2004, 7, 14, 0, 0), 'updated_date': datetime.datetime(2024, 6, 3, 0, 0), 'expiration_date': datetime.datetime(2025, 7, 14, 0, 0), 'transfer_date': datetime.datetime(2019, 2, 14, 0, 0), 'name_servers': ['ns1.kreawit.se 79.99.1.214', 'ns2.kreawit.se 81.216.50.110'], 'dnssec': 'unsigned delegation', 'status': 'ok', 'registrar': 'Loopia AB'}
    #    {'domain_name': ['NORRLAB.COM', 'norrlab.com'], 'registrar': 'One.com A/S', 
    # 'whois_server': 'whois.one.com', 'referral_url': None, 
    #      'updated_date': datetime.datetime(2023, 12, 12, 0, 28, 34), 'creation_date': datetime.datetime(2020, 1, 11, 19, 46, 48), 
    #      'expiration_date': datetime.datetime(2025, 1, 11, 19, 46, 48), 
    #      'name_servers': ['NS01.ONE.COM', 'NS02.ONE.COM', 'ns02.one.com', 'ns01.one.com'], 
    #      'status': 'ok https://icann.org/epp#ok', 'emails': ['abuse@one.com', 'hostmaster@one.com'], 
    #      'dnssec': 'unsigned', 'name': 'REDACTED FOR PRIVACY', 'org': 'REDACTED FOR PRIVACY', 
    #      'address': 'REDACTED FOR PRIVACY', 'city': 'REDACTED FOR PRIVACY', 
    #      'state': None, 'registrant_postal_code': 'REDACTED FOR PRIVACY', 'country': 'SE'} 
    
    
          # ~ try:
         # ~ answers = None
         # ~ answers = dns.resolver.query(lookuplist[i][1], 'MX')
      # ~ except dns.exception.DNSException:
         # ~ #Do nothing here if there is no MX
         # ~ pass

    get_dns_records(domain,['SOA','NS','A','CNAME','MX','TXT'],res)
    _logger.warning(f"{res=}")
    
    # Mailserver
    res['mail_server'] = get_mail_server_software(domain)


    # ~ #Social media
    try:
        sm = [s for s in search(url,num_results=20)]
        _logger.warning(f"Social Media {sm=}")

        for sm_type in ['github','facebook','instagram','linkedin','my.ai','x','brainville','odoo-community','linkopingsciencepark']:
            if sm_type in sm:
                res[f'bw_{sm_type}'] = [s for s in sm if sm_type in l][0]
                _logger.warning(f"bw_{sm_type}=")
        if not 'bw_instagram' in res:
            sm = [s for s in search(url+' instagram',num_results=20)]
            _logger.warning(f"{sm=} insta")

            if len(sm) > 0:
                res['bw_instagram'] = [0]
    except Exception as e:
        _logger.warning(f"Social Media: An unexpected error occurred: {e}")    
        
        
    return res

def name2url(name):
    return [a for a in search(name,1)][0]

def get_dns_records(domain,rrec,res):
    for r in rrec:
        try:
            f = f'dns_{r.lower()}'
            res[f] = ', '.join([dns.to_text() for dns in resolve(domain, r.upper()).rrset.items])
            _logger.warning(f"{f} {res[f]=}")
        except Exception as e:
            _logger.warning(f"DNS: An unexpected error occurred: {e}")



def get_mail_server_software(domain,smtp_port=25):
    try:
        mx_primary = sorted([mx for mx in resolve(domain, 'MX').rrset.items], key=lambda r: r.preference)[0].exchange.to_text()[:-1]    
        _logger.warning(f"{mx_primary=}")
        
        if 'outlook' in mx_primary:
            return "MS365"
        if 'google' in mx_primary:
            return 'Google'
        else:
            return "Other"


        # Create a connection to the SMTP server
        server = smtplib.SMTP(mx_primary, smtp_port, timeout=10)
        
        # Initiate the connection and retrieve the banner message
        server.ehlo_or_helo_if_needed()
        
        # Close the connection
        server.quit()
        
        # Extract and print the mail server software information from the banner
        banner = server.sock.recv(1024).decode()
        return banner.strip()
    except (smtplib.SMTPConnectError, smtplib.SMTPServerDisconnected, socket.timeout) as e:
        return f"Error connecting to SMTP server: {e}"
    except Exception as e:
        return f"An unexpected error occurred: {e}"

