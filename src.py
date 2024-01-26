import re
import math
import time
from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
import urllib.parse
from requests_html import HTMLSession
import json
import pandas as pd
from pandas import json_normalize
from ratelimit import limits, sleep_and_retry
from retrying import retry
from ast import literal_eval
import sys
from fake_useragent import UserAgent

non_decimal = re.compile(r'[^\d.]+')
url_agentlist = 'https://www.realtor.com/realestateagents/'
url_absolute = 'https://www.realtor.com'
ua = UserAgent()

headers_fhome = {'User-Agent': ua.random}
# headers_fhome = {
#     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
#     'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
#     'Cache-Control': 'max-age=0',
#     'Referer': 'https://www.realtor.com/'}

headers_fagents = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'Cache-Control': 'max-age=0',
    'Referer': 'https://www.realtor.com/realestateagents'}


def get_locationlist(path):
    @sleep_and_retry
    @limits(calls=5, period=1)  # 5 requests per second
    # Define a retry decorator with exponential backoff
    @retry(wait_exponential_multiplier=1000, wait_exponential_max=10000, stop_max_attempt_number=5)
    def get_soup(path, head):
        session = HTMLSession()
        r = session.get(path, headers=head,
                        timeout=10)
        r.session.close()
        return BeautifulSoup(r.html.raw_html, features='lxml')
    location_links = []

    try:
        i = 0
        while i <= 5:
            headers_fhome = {'User-Agent': ua.random}
            soup = get_soup(path, headers_fhome)
            script_data = soup.find('script', id='__NEXT_DATA__')
            if script_data:
                script_data_website = script_data.text
                json_data = json.loads(script_data_website)
                clean_json = format_json(json_data)

                # Write the formatted JSON data to the file
                with open('loclist.json', 'w') as json_file:
                    json_file.write(clean_json)
                break
            else:
                pass
            # ul = soup.findAll('li', class_="ListItemstyles__StyledListItem-rui__zdhuws-0 fVswxu")
            # if ul:
            #     pass
            # else:
            #     break
            i += 1
            time.sleep(3)
        for link in ul:
            link_true = link.find('a', class_="base__StyledAnchor-rui__ermeke-0 eMbFNh", href=True)['href']
            if link_true.split('/')[1] == 'realestateagents':
                location_links.append(link_true)
                # print(link_true)
        print(f'Locations:', location_links)
        return location_links
    except urllib.error.URLError as e:
        print(f"Error: {e}")


def try_locationlist(list):
    for _ in list:
        print('\nLocation: ' + str(_))
        location_agent = {}
        allagentid = []
        link_ = urllib.parse.urljoin(url_absolute, _)
        @sleep_and_retry
        @limits(calls=5, period=1)  # 5 requests per second
        # Define a retry decorator with exponential backoff
        @retry(wait_exponential_multiplier=1000, wait_exponential_max=10000, stop_max_attempt_number=5)
        def get_soup(path, head):
            session = HTMLSession()
            r = session.get(path, headers=head,
                            timeout=10)
            r.session.close()
            return BeautifulSoup(r.html.raw_html, features='lxml')
        try:
            soup = get_soup(link_, headers_fagents)
            # Get profiles
            allpage = literal_eval(non_decimal.sub('', (soup.find('span', class_="jsx-1552726949").text).split()[0]))
            print('Agents = ' + str(allpage))
            if allpage > 20:
                pages = math.ceil(allpage / 20)
            else:
                pages = 1
            for item in range(1, pages + 1):
                sys.stdout.write('\r' + 'Page ' + str(item) + ' of ' + str(pages))
                sys.stdout.flush()
                # print('Page ' + str(item))
                if item == 1:
                    path = urllib.parse.urljoin(url_absolute, _)
                else:
                    page = str(_) + '/pg-' + str(item)
                    # url/location/page
                    path = urllib.parse.urljoin(url_absolute, page)
                allagentid = get_agentids(path, allagentid)
                time.sleep(1.5)
            allagentid = set(allagentid)
            location_agent[_] = allagentid
        except urllib.error.URLError as e:
            print(f"Error: {e}")
            print('Error in: ' + str(_))
    return location_agent


def get_agentids(path, agentid):
    @sleep_and_retry
    @limits(calls=5, period=1)  # 5 requests per second
    # Define a retry decorator with exponential backoff
    @retry(wait_exponential_multiplier=1000, wait_exponential_max=10000, stop_max_attempt_number=5)
    def get_soup(pathx, head):
        session = HTMLSession()
        r = session.get(pathx, headers=head,
                        timeout=10)
        r.session.close()
        return BeautifulSoup(r.html.raw_html, features='lxml')
    # Get profiles
    try:
        soup = get_soup(path, headers_fagents)
        script_data = soup.find('script', id='__NEXT_DATA__')
        if script_data:
            script_data_website = script_data.text
            json_data = json.loads(script_data_website)
            agents = json_data['props']['pageProps']['pageData']['agents']
            if agents:
                agentid.extend([i['id'] for i in agents])
                return agentid
            else:
                pass
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


