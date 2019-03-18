import requests
from bs4 import BeautifulSoup

# session = Session()

mainUrl = 'https://www.mgsm.pl'

vendorsResponse = requests.get(mainUrl + '/pl/katalog/')

if vendorsResponse.status_code == 200:
    vendorsBs = BeautifulSoup(vendorsResponse.text, 'html.parser')

terminal_id = 0

for vendorCatalog in vendorsBs.find_all('div', {'class': 'brand-box__inner'}):
    nextPag = True

    while nextPag:
        vendorCatalogResp = requests.get(mainUrl + vendorCatalog.find('a').get('href'))
        vendorCatalogBs = BeautifulSoup(vendorCatalogResp.text, 'html.parser')

        pagination = vendorCatalogBs.find_all('li', {'class': 'arrow'})
        if pagination:
            for pag in pagination:
                if not pag.has_attr('aria-disabled'):
                    vendorCatalog = pag
        else:
            nextPag = False
