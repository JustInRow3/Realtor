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
    # req = Request(link_, headers=head)
    try:
        # web_byte = urlopen(req, timeout=10)
        # webpage = web_byte.read().decode('utf-8')
        session = HTMLSession()
        r = session.get(link_, headers=headers_fagents,
                        timeout=10)
        r.session.close()
        soup = BeautifulSoup(r.html.raw_html, features='lxml')
        time.sleep(1)
        fullname = ifexist(soup, 'h2', 'class', "base__StyledType-rui__sc-108xfm0-0 bICTqR")
        photo = soup.find('img', class_="jsx-832586154 profile-img").get('src')
        company = ifexist(soup, 'p', 'class', "base__StyledType-rui__sc-108xfm0-0 fgiRuk")
        ratings = ifexist(soup, 'span', 'class', "jsx-832586154 review")
        review = ifexist(soup, 'span', 'class', "jsx-832586154 gray-font")
        recommended = ifexist(soup, 'span', 'class', "jsx-832586154 review pr-2")
        section_mobile = ifexist_href(soup, 'a', 'class', "jsx-832586154 track-my-clicks")
        section_website = ifexist_href(soup, 'a', 'class', "jsx-787916864 website-link")
        section_address = ifexist(soup, 'div', 'class', "jsx-1192639173 better-homes-and-gar-icon-right")
        section_share = ifexist_href(soup, 'a', 'class', "jsx-39586221 track-my-clicks mobile-number")
        script_data = soup.find('script', id='__NEXT_DATA__')
        if script_data:
            script_data_website = script_data.text
            json_data = json.loads(script_data_website)
            # # Write JSON data to the file
            # with open('all_out.json', 'w') as json_file:
            #     json.dump(json_data, json_file, indent=2)
            flattened_data = json_normalize((((json_data.get('props', {})).get('initialReduxState', {})).get('profile', {})).get('agentdetail', {}))
            flattened_data.to_excel('output.xlsx', index=False)
            # website = json_data.get()
            time.sleep(1)
        # section = soup.findAll('a', class_="jsx-832586154 track-my-clicks")
        # section = soup.findAll(soup, 'div', 'class', 'jsx-787916864 preview-main-content-form')
        # listings = ifexist(soup, 'div', 'data-testid', "component-contactDetails")
        print(soup.prettify(formatter='html'))
        time.sleep(1)
        # phone = soup.find('p', class_="jsx-787916864 d-flex")
        # mobile = soup.find('span', class_="jsx-787916864 mobile-number")
        # website = soup.find('a', class_="jsx-787916864 website-link")
        # location = soup.find('p', class_="jsx-1192639173 addressspace")
        # experience = soup.find('div', class_="jsx-1251629822 preview-profile-info preview-profile-info-right")
        # credentials =
        # pricerange = soup.find('div', class_="jsx-1251629822 preview-profile-info-left")
        # areaserve = soup.find('div', class_="jsx-1418565729 preview-more-details-profile-mian")
        # specialization = soup.find('ul', class_="jsx-1418565729 data preview-more-details-profile-li1")
        # language = soup.find('li', class_="jsx-1418565729")

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




# session = HTMLSession()
# r = session.get('https://www.realtor.com/realestateagents/566b2816bb954c01006758f2', headers=headers_fagents, timeout=10)
# time.sleep(1)