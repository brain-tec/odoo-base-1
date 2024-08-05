import requests
from bs4 import BeautifulSoup
from PIL import Image
import base64
import logging
_logger = logging.getLogger(__name__)

def LogoScrape(url):
    # Send an HTTP request to the website's URL to retrieve the HTML source code
    response = requests.get(url)
    html = response.text

    # Parse the HTML using Beautiful Soup
    soup = BeautifulSoup(html, 'html.parser')


    # Find all img tags
    img_tags = soup.find_all('img')


    # Iterate through the img tags and check for attributes that indicate it is a logo
    logo_url='none'
    for img_tag in img_tags:
        # ~ print(img_tag)
        if img_tag.get('id') == 'logo':
            logo_url = img_tag['src']
            break
            
        if 'logo' in img_tag.get('class', []):
            logo_url = img_tag['src']+'class'
            break
            
        if "logo" in img_tag.get('src',''):
            # ~ print(img_tag)
            logo_url = img_tag['src']
            break
    if logo_url == 'none':
        return None
    if not 'http' in logo_url:
        logo_url = url+'/'+logo_url

    _logger.warning(f'Logo {logo_url=}')

    logo = requests.get(logo_url, stream=True).raw
    _logger.warning(f'{logo=}')

    return fetch_image_as_base64(logo_url)
    return base64.b64encode(Image.open(requests.get(logo_url, stream=True).raw))
    

def fetch_image_as_base64(url):
    # Fetch the image from the URL
    response = requests.get(url)
    
    # Ensure the request was successful
    if response.status_code == 200:
        # Encode the image content in base64
        encoded_image = base64.b64encode(response.content).decode('utf-8')
        return encoded_image
    else:
        raise Exception(f"Failed to fetch image. Status code: {response.status_code}  {url=}")

