from bs4 import BeautifulSoup

# ul = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'ListItemstyles__StyledListItem-rui__zdhuws-0 fVswxu')))
#
url = 'https://www.realtor.com/realestateagents/'

from urllib.request import Request, urlopen
req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})

web_byte = urlopen(req, timeout=10).read()
webpage = web_byte.decode('utf-8')
soup = BeautifulSoup(webpage, 'html.parser')
ul = soup.findAll('li', class_="ListItemstyles__StyledListItem-rui__zdhuws-0 fVswxu")
location_links = []
for link in ul:
    link_true = link.find('a', class_="base__StyledAnchor-rui__ermeke-0 eMbFNh", href=True)['href']
    if link_true.split('/')[1] == 'realestateagents':
        location_links.append(link_true)
        # print(link_true)
agent_list = r''location_links[0]

# print(ul)
print(soup)