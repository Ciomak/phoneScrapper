import requests
import time
from bs4 import BeautifulSoup
from Terminal import Session, Terminal  # , TerminalStage

session = Session()

mainUrl = 'https://www.mgsm.pl'

vendorsResponse = requests.get(mainUrl + '/pl/katalog/')

if vendorsResponse.status_code == 200:
    vendorsBs = BeautifulSoup(vendorsResponse.text, 'html.parser')

terminal_id = 0

for vendorCatalog in vendorsBs.find_all('div', {'class': 'brand-box__inner'}):
    nextPag = True

    while nextPag:
        vendorCatalogResp = requests.get(mainUrl + vendorCatalog.find('a').get('href'))
        print('Vendor Url {}'.format(vendorCatalogResp.url))
        print('Vendor Response {}'.format(vendorCatalogResp.status_code))

        if vendorCatalogResp.status_code == 200:
            vendorCatalogBS = BeautifulSoup(vendorCatalogResp.text, 'html.parser')
            containers = vendorCatalogBS.find_all('div', {'class': 'phone-container'})

        phones = []

        for container in containers:
            for phone in container.find_all('div', {'class': 'phone-item'}):
                phones.append(phone.find('a').get('href'))

        for phone in phones:
            print(phone)
            phoneUrl = mainUrl + phone
            print('Phone Url {}'.format(phoneUrl))
            phoneSpec = requests.get(phoneUrl)

            bs = BeautifulSoup(phoneSpec.text, 'html.parser')

            print(phoneUrl)

            t1 = Terminal(phoneUrl, terminal_id, bs)

            if t1.release_date and t1.release_date >= '2016Q1':
                session.add(t1)
                session.commit()

            time.sleep(45)

            terminal_id += 1

        pagination = vendorCatalogBS.find_all('li', {'class': 'arrow'})
        if pagination:
            for pag in pagination:
                if not pag.has_attr('aria-disabled'):
                    vendorCatalog = pag
        else:
            nextPag = False
