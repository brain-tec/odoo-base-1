import requests
from bs4 import BeautifulSoup
from PIL import Image
import base64

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
            logo_url = img_tag['src']+'id'
            break
            
        if 'logo' in img_tag.get('class', []):
            logo_url = img_tag['src']+'class'
            break
            
        if "logo" in img_tag.get('src',''):
            # ~ print(img_tag)
            logo_url = img_tag['src']+'src'
            break
    if logo_url == 'none':
        return None
    if not 'http' in logo_url:
        logo_url = url+'/'+logo_url
    return base64.b64encode(Image.open(requests.get(logo_url, stream=True).raw))
