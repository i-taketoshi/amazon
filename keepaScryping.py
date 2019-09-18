# -*- coding: utf-8 -*-
"""
Created on Fri Feb  2 22:45:09 2018

@author: taketoshi
"""

# -*- coding: utf-8 -*-
"""
GOOGLEトレンドから急上昇ワードを取得する

"""

from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.chrome.options import Options
import time
#from selenium.webdriver.support.ui import WebDriverWait
#from selenium.webdriver.support import expected_conditions as EC
#from selenium.webdriver.common.by import By

from selenium.webdriver.common.action_chains import ActionChains

import re
import random 
import datetime
import sqlite3
dbname = r'D:\workspace\sqlite\sample.sqlite3'
path = r'D:\workspace\amazon\chromedriver.exe'
todaydetail  =    datetime.datetime.today()
yymmdd = todaydetail.strftime("%Y-%m-%d")
path = r'D:\workspace\amazon\chromedriver.exe'

options = Options()
options.add_argument("--disable-extentions")
options.add_argument("--ignore-certificate-errors")
#options.add_argument("--headless")


driver = webdriver.Chrome(path, chrome_options=options)

driver.get("https://keepa.com/#!deals")
time.sleep(random.randint(5,10))


driver.find_element_by_class_name('languageMenuText').click()
time.sleep(1)

driver.find_element_by_xpath("//div[@id='language_domains']/div[1]/span[1]").click()
time.sleep(3)


driver.find_element_by_xpath("//div[@id='dealPriceTypesFilter']/div[1]").click()
time.sleep(random.randint(3,6))
driver.find_element_by_xpath("//div[@id='dealDateRange']/div[1]").click()
time.sleep(random.randint(3,6))
driver.find_element_by_xpath("//div[@id='dealSortType']/div[5]").click()
time.sleep(random.randint(3,6))

for l in range(1):
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(random.randint(5,12))

data = driver.page_source
soup = BeautifulSoup(data,"lxml")
                        
r = re.compile('product/1-([a-zA-Z0-9]+)')

#DBに登録
conn = sqlite3.connect(dbname)
c = conn.cursor()
sql = 'insert into Keepa(asin, yymmdd) values (?,?)'
    
                                
for link in soup.findAll("a"):
    m = r.search(str(link.get('href')))
    if m:
        #print(m.group(1))
        v = (m.group(1), yymmdd)
        c.execute(sql, v)
    
conn.commit()
conn.close()
                
        
prettify = soup.prettify()    
f = open(r'D:\workspace\GoogleTrend.txt','wb')
f.write(prettify.encode('utf-8'))
f.close()

driver.quit()


