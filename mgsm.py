import requests
import time
from bs4 import BeautifulSoup
from Terminal import Session, Terminal  # , TerminalStage
from sqlalchemy import select

session = Session()

mainUrl = 'https://www.mgsm.pl'

vendorsResponse = requests.get(mainUrl + '/pl/katalog/')

if vendorsResponse.status_code == 200:
    vendorsBs = BeautifulSoup(vendorsResponse.text, 'html.parser')

for vendorCatalog in vendorsBs.find_all('div', {'class': 'brand-box__inner'}):
    nextPag = True

    if vendorCatalog.find('span').text == 'Samsung':

        while nextPag:
            vendorCatalogResp = requests.\
                get(mainUrl + vendorCatalog.find('a').get('href'))
            print('Vendor Url {}'.format(vendorCatalogResp.url))
            print('Vendor Response {}'.format(vendorCatalogResp.status_code))

            if vendorCatalogResp.status_code == 200:
                vendorCatalogBS = BeautifulSoup(
                    vendorCatalogResp.text, 'html.parser'
                    )
                containers = vendorCatalogBS.find_all(
                    'div', {'class': 'phone-container'}
                    )

            br = None

            for container in containers:
                for phone in container.find_all(
                    'div', {'class': 'phone-item'}
                ):
                    phoneUrl = mainUrl + phone.find('a').get('href')
                    print('Phone Url {}'.format(phoneUrl))

                    stmt = select([Terminal.terminal_id]).\
                        where(Terminal.url == phoneUrl)
                    if session.execute(stmt).fetchone() is None:
                        phoneSpec = requests.get(phoneUrl)
                        bs = BeautifulSoup(phoneSpec.text, 'html.parser')

                        t1 = Terminal(phoneUrl, bs)

                        if t1.release_date is None or\
                                t1.release_date >= '2016Q1':
                            session.add(t1)
                            session.commit()
                            time.sleep(45)
                        else:
                            br = True
                            break

                if br:
                    break

                pagination = vendorCatalogBS.find_all('li', {'class': 'arrow'})
                if pagination:
                    for pag in pagination:
                        if not pag.has_attr('aria-disabled'):
                            vendorCatalog = pag
                            time.sleep(10)
                else:
                    nextPag = False

        if br:
            break

    time.sleep(10)
