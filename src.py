import html
import time
from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
import urllib.parse
from requests_html import HTMLSession
import json
import pandas as pd
from pandas import json_normalize

url_agentlist = 'https://www.realtor.com/realestateagents/'
url_absolute = 'https://www.realtor.com'

headers_fhome = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'Cache-Control': 'max-age=0',
    'Referer': 'https://www.realtor.com/'}

headers_fagents = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'Cache-Control': 'max-age=0',
    'Referer': 'https://www.realtor.com/realestateagents'}


def get_agentlist(path, head):
    session = HTMLSession()
    location_links = []  # initialize location list
    # req = Request(path, headers=head)
    try:
        r = session.get(path, headers=headers_fagents,
                        timeout=10)
        # web_byte = urlopen(req, timeout=10)
        # webpage = web_byte.read().decode('utf-8')
        soup = BeautifulSoup(r.html, 'html.parser')
        ul = soup.findAll('li', class_="ListItemstyles__StyledListItem-rui__zdhuws-0 fVswxu")
        for link in ul:
            link_true = link.find('a', class_="base__StyledAnchor-rui__ermeke-0 eMbFNh", href=True)['href']
            if link_true.split('/')[1] == 'realestateagents':
                location_links.append(link_true)
                # print(link_true)
        print(f'Locations:', location_links)
        return location_links
    except urllib.error.URLError as e:
        print(f"Error: {e}")


def try_locationlist(list, head):
    for _ in list:
        link_ = urllib.parse.urljoin(url_absolute, _)
        req = Request(link_, headers=head)
        try:
            web_byte = urlopen(req, timeout=10)
            webpage = web_byte.read().decode('utf-8')
            soup = BeautifulSoup(webpage, 'html.parser')
            # Get profiles
            profiles = soup.findAll('a', class_="jsx-3873707352")
            location = soup.find('h2', class_="base__StyledType-rui__sc-108xfm0-0 eMHlSD")
            hrefs_profiles = [link.get('href') for link in profiles if len(link.get('href').split('/')) == 3]
            hrefs_profiles.insert(0, location.text)
            set(hrefs_profiles)
            print(f'Profiles:', hrefs_profiles)
            time.sleep(2)
        except urllib.error.URLError as e:
            print(f"Error: {e}")


def get_profiledetails(link):
    link_ = urllib.parse.urljoin(url_absolute, link)
    try:
        session = HTMLSession()
        r = session.get(link_, headers=headers_fagents,
                        timeout=10)
        r.session.close()
        soup = BeautifulSoup(r.html.raw_html, features='lxml')
        time.sleep(1)
        script_data = soup.find('script', id='__NEXT_DATA__')
        if script_data:
            script_data_website = script_data.text
            json_data = json.loads(script_data_website)
            clean_json = format_json(json_data)

            # Write the formatted JSON data to the file
            with open('try.json', 'w') as json_file:
                json_file.write(clean_json)
        time.sleep(1)

    except urllib.error.URLError as e:
        print(f"Error: {e}")


def ifexist(soup, tag, tag_class=None, value_=None):
    element = soup.find(tag, attrs={tag_class: value_})
    if element:
        return element.text
    else:
        return None
def ifexist_href(soup, tag, tag_class=None, value_=None):
    element = soup.find(tag, attrs={tag_class: value_})
    if element:
        return element.get('href')
    else:
        return None


def format_json(data_json):
    """
    Format JSON data using a template.

    Parameters:
    - template_json (dict): Template JSON structure.
    - data_json (dict): Actual data to be merged with the template.

    Returns:
    - formatted_json (str): Formatted JSON string.
    """
    # Read data from the JSON file
    with open('template2.json', 'r') as json_file:
        template_json = json.load(json_file)

    # Create a copy of the template to avoid modifying it directly
    formatted_json = template_json.copy()

    # Function to recursively update the template
    def update_template(template, data):
        for key, value in template.items():
            if isinstance(value, dict) and key in data and isinstance(data[key], dict):
                update_template(value, data[key])
            else:
                template[key] = data.get(key, value)
    # Update the template with the actual data
    update_template(formatted_json, data_json)

    # Convert the merged dictionary to a formatted JSON string
    formatted_json_str = json.dumps(formatted_json, indent=2)

    print(formatted_json_str)
    return formatted_json_str


# session = HTMLSession()
# r = session.get('https://www.realtor.com/realestateagents/566b2816bb954c01006758f2', headers=headers_fagents, timeout=10)
# time.sleep(1)