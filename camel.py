# -*- coding: utf-8 -*-
"""
Created on Sat Feb  3 13:23:43 2018

@author: taketoshi
"""


from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.chrome.options import Options
import time
#from selenium.webdriver.support.ui import WebDriverWait
#from selenium.webdriver.support import expected_conditions as EC
#from selenium.webdriver.common.by import By
import re
import random
# Selectタグが扱えるエレメントに変化させる為の関数を呼び出す
from selenium.webdriver.support.ui import Select


categoryLists = ["Prime Video","Androidアプリ","DIY・工具・ガーデン","DVD","Kindleストア","PCソフト","おもちゃ","ギフト券","ゲーム","シューズ＆バッグ","ジュエリー","スポーツ＆アウトドア","デジタルミュージック","ドラッグストア","パソコン・周辺機器","ビューティー","ファッション","ベビー＆マタニティ","ペット用品","ホビー","ホーム＆キッチン","ミュージック","大型家電","家電＆カメラ","文房具・オフィス用品","服＆ファッション小物","本","楽器・音響機器","洋書","産業・研究開発用品","腕時計","車＆バイク","食品・飲料・お酒"]


path = r'D:\workspace\amazon\chromedriver.exe'

options = Options()
options.add_argument("--disable-extentions")
options.add_argument("--ignore-certificate-errors")
#options.add_argument("--headless")


driver = webdriver.Chrome(path, chrome_options=options)

driver.get("https://camelcamelcamel.com/")
time.sleep(random.randint(5,7))

driver.execute_script("window.scrollTo(0, 700);")
time.sleep(random.randint(5,7))

el = driver.find_element_by_id("bn")
r = re.compile('/product/([a-zA-Z0-9]{10})\?')
    
for option in el.find_elements_by_tag_name('option'):
    #print(option.text)

    driver.find_element_by_xpath("//select[@id='bn']/option[text()='"+ option.text +"']").click()
    time.sleep(random.randint(5,20))

    
    data = driver.page_source
    soup = BeautifulSoup(data,"lxml")
    
                            
    for link in soup.findAll("a"):
        m = r.search(str(link.get('href')))
        if m:
            print(m.group(1))
            
    
    print("############")
    

driver.get("https://www.yahoo.co.jp/")
time.sleep(2)

    
driver.quit()
