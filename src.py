from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
import urllib.parse

url_agentlist = 'https://www.realtor.com/realestateagents/'

headers_fhome = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
           'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
           'Cache-Control': 'max-age=0',
           'Cookie': 'split=n; split_tcv=173; __vst=26f8d4f0-7353-43fd-bcc0-ccc07731d9e0; __ssn=54ee61ed-aadb-41b4-9a07-218944269851; __ssnstarttime=1702862188; __bot=false; permutive-id=4c077a97-e0fd-4d16-9d8a-d59e9107d466; _pxvid=161bd472-9d43-11ee-87e4-b5033f3a715c; pxcts=161be382-9d43-11ee-87e4-ff04d18ffb56; AMCVS_8853394255142B6A0A4C98A4%40AdobeOrg=1; s_ecid=MCMID%7C92030571829663310514257404779208405396; AMCV_8853394255142B6A0A4C98A4%40AdobeOrg=-1124106680%7CMCIDTS%7C19710%7CMCMID%7C92030571829663310514257404779208405396%7CMCAAMLH-1703466996%7C6%7CMCAAMB-1703466996%7CRKhpRz8krg2tLO6pguXWp5olkAcUniQYPHaMWWgdJ3xzPWQmdj0y%7CMCOPTOUT-1702869397s%7CNONE%7CMCAID%7CNONE%7CvVersion%7C5.2.0; __split=8; _gcl_au=1.1.1992479585.1702862200; _px3=a9af9df9896bc47c53d623046baa2671b634127e55a77ca47afb889a5c68d3cb:M4C+UG4lUqw4IcIQI4/gcokTgNFTrtkqWmTeuvhqnxLbctYPwPlWudaaJoiYXIUNcOKVZFgFk4fnUhc5KQTYKg==:1000:K+npeJ0vhBGxyxUaFy2sxj5ePsSbi9ETg83qntm0K+1MKPN5mbIafCudbwZsJ1WyTTu5Vx4FL2yCNsUEGeLj/fNRQkbvi2Y2aQjNZBhDHUvM4ItGlICn6fsTyd90rC7qajUiGagMh8wcuCZJaJsRb6xvT/R7LOwQBGKLMWkQ5VFwvmi/DKQ6g5HndH5iMmY+SU3bUklgosMVVkDg4V6FIxjmX9/GmDxj8iU+i30OTGk=; _lr_sampling_rate=0; _rdt_uuid=1702862200938.2b27688a-c4ec-4245-ad62-f7e51c43b748; _tac=false~self|not-available; _ta=us~1~89df68bc35032d48c293adce8574aa42; _tas=sw0eto7nlv8; _scid=25bf01a3-62b0-45db-89e6-d6a303010144; _scid_r=25bf01a3-62b0-45db-89e6-d6a303010144; _lr_retry_request=true; _lr_env_src_ats=false; _ncg_sp_ses.cc72=*; _ncg_id_=87cad74b-d446-4d8e-ba7a-b591702348e9; G_ENABLED_IDPS=google; _ncg_sp_id.cc72=87cad74b-d446-4d8e-ba7a-b591702348e9.1702862204.1.1702862205.1702862204.9a8090bd-3b01-4ed2-b1f7-a77cbf1da499; _sctr=1%7C1702828800000; _tt_enable_cookie=1; _ttp=gTYXxpNUsWQQZP_qaXGatYs7JHT; _ncg_domain_id_=87cad74b-d446-4d8e-ba7a-b591702348e9.1.1702862203743.1765934203743; AMCVS_AMCV_8853394255142B6A0A4C98A4%40AdobeOrg=1; AMCV_AMCV_8853394255142B6A0A4C98A4%40AdobeOrg=-1124106680%7CMCMID%7C92030571829663310514257404779208405396%7CMCIDTS%7C19710%7CMCOPTOUT-1702869409s%7CNONE%7CvVersion%7C5.2.0; __qca=P0-353878915-1702862203159; adcloud={%22_les_v%22:%22y%2Crealtor.com%2C1702864009%22}; _ncg_g_id_=b1e85376-602d-485a-ba06-779493190c68.3.1702862208.1765934203743; ajs_anonymous_id=7c14312a-36e2-403f-ac33-9ad9f0e69a56; g_state={"i_p":1702869410361,"i_l":1}; _ga_MS5EHT6J6V=GS1.1.1702862206.1.0.1702862210.0.0.0; _ga=GA1.2.319100801.1702862198; _gid=GA1.2.611048740.1702862211; _gat=1; _uetsid=1f4242f09d4311ee88e69957a2a64e1c; _uetvid=1f423f009d4311ee8dbc0912b7840db2; mdLogger=false; kampyle_userid=c648-1aa2-6a7f-e8ae-b799-7cac-dd0e-5080; kampyleUserSession=1702862214405; kampyleUserSessionsCount=1; kampyleSessionPageCounter=1; ab.storage.sessionId.7cc9d032-9d6d-44cf-a8f5-d276489af322=%7B%22g%22%3A%221b950f8e-1579-1628-02ef-fe18635c22e9%22%2C%22e%22%3A1702864014494%2C%22c%22%3A1702862214494%2C%22l%22%3A1702862214494%7D; ab.storage.deviceId.7cc9d032-9d6d-44cf-a8f5-d276489af322=%7B%22g%22%3A%2222688168-2524-a2d4-c640-8f821afeb9f3%22%2C%22c%22%3A1702862214486%2C%22l%22%3A1702862214494%7D; ab.storage.userId.7cc9d032-9d6d-44cf-a8f5-d276489af322=%7B%22g%22%3A%22visitor_26f8d4f0-7353-43fd-bcc0-ccc07731d9e0%22%2C%22c%22%3A1702862214493%2C%22l%22%3A1702862214495%7D; cto_bundle=AVEZV19hSWs4SHRGblhYRDNid0lUMTN6RURyaWoxNGFITmtYN1E5VzFhekp0bnEybTN3UXVJRWlmMGs5MlIxSFJ0ak52Y0RTbGZ2a2FZSSUyQjhhMHJlbHQxcWhuYiUyQlBYbkJKblFBbXMzRzFIU0xrbzFRV1pDdkVlRVdIdllucGZqd2NQM08yMlpoZUxFSyUyRlRuJTJCRkpEVW9hZU1OQSUzRCUzRA; _iidt=5BOUgrG6IV/RnkOhLsHCBiQih21PESo33Fl2WA2qV2n2xm+ksUeHm28RQsYLaTiNJuZX2ErFLG+rK0qbpNfMxZ0TfXuMIXBqSQ==; _vid_t=0DOOXiDO3Y7kEL0aoQYJ+EqbddPRtB3MGtltJo86I4PAGQb1QKWblLVdcsQRcT6GKQ1SCZU4WJEGi2C024aUx0vtXbZ/nDx4YA==; __fp=zu2DWeOmVPIn4yCk6Lqs',
           'Referer': 'https://www.realtor.com/'}

def get_agentlist(path, head):
    location_links = [] #initialize location list
    req = Request(path, headers=head)
    web_byte = urlopen(req, timeout=10)
    if web_byte.getcode() != 200:
        return ['Error']
    webpage = web_byte.read().decode('utf-8')
    soup = BeautifulSoup(webpage, 'html.parser')
    ul = soup.findAll('li', class_="ListItemstyles__StyledListItem-rui__zdhuws-0 fVswxu")
    for link in ul:
        link_true = link.find('a', class_="base__StyledAnchor-rui__ermeke-0 eMbFNh", href=True)['href']
        if link_true.split('/')[1] == 'realestateagents':
            location_links.append(link_true)
            # print(link_true)
    return location_links