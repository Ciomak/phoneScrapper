import requests
import re
from bs4 import BeautifulSoup

url = 'https://www.mgsm.pl/pl/katalog/samsung/galaxya8s/Samsung-Galaxy-A8s.html'
req = requests.get(url)

bs = BeautifulSoup(req.text, 'html.parser')