# -*- coding: utf-8 -*-
"""
GOOGLEトレンドから急上昇ワードを取得する

"""

from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.chrome.options import Options
import time
import datetime
import sqlite3
dbname = r'D:\workspace\sqlite\sample.sqlite3'
path = r'D:\workspace\amazon\chromedriver.exe'

options = Options()
options.add_argument("--disable-extentions")
options.add_argument("--ignore-certificate-errors")
#options.add_argument("--headless")


driver = webdriver.Chrome(path, chrome_options=options)

driver.get("https://trends.google.co.jp/trends/hottrends#pn=p4")
time.sleep(3)

data = driver.page_source
soup = BeautifulSoup(data,"lxml")

'''
prettify = soup.prettify()    
f = open(r'D:\workspace\GoogleTrend.txt','ab')
f.write(prettify.encode('utf-8'))
f.close()
'''
driver.quit()


hottrends = soup.find_all(class_="hottrends-single-trend-title ellipsis-maker-inner")

todaydetail  =    datetime.datetime.today()
yymmdd = todaydetail.strftime("%Y-%m-%d")

#DBに登録
conn = sqlite3.connect(dbname)
c = conn.cursor()
sql = 'insert into Google(trend, yymmdd) values (?,?)'
    
for hottrend in hottrends:
    v = (hottrend.text, yymmdd)
    c.execute(sql, v)
    
conn.commit()
conn.close()
