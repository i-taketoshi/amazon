import urllib.request
import urllib.parse


# coding: UTF-8
from bs4 import BeautifulSoup

# アクセスするURL
url = "https://info.finance.yahoo.co.jp/fx/detail/?code=USDJPY=FX"

# URLにアクセスする htmlが帰ってくる → <html><head><title>経済、株価、ビジネス、政治のニュース:日経電子版</title></head><body....
html = urllib.request.urlopen(url)

# htmlをBeautifulSoupで扱う
soup = BeautifulSoup(html, "lxml")

USDJPY = soup.find(id='USDJPY_detail_bid')
print(USDJPY.text)

print(float(USDJPY.text))

aa = 10 * float(USDJPY.text)

print(aa)