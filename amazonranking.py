# -*- coding: utf-8 -*-
"""
Created on Fri Feb  2 21:43:53 2018

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
import random
import datetime
import sqlite3
dbname = r'D:\workspace\sqlite\sample.sqlite3'
path = r'D:\workspace\amazon\chromedriver.exe'
todaydetail  =    datetime.datetime.today()
yymmdd = todaydetail.strftime("%Y-%m-%d")

#categoryLists = [ "おもちゃ","ゲーム"]
categoryLists = ["Prime Video","Androidアプリ","DIY・工具・ガーデン","DVD","Kindleストア","PCソフト","おもちゃ",
                 "ゲーム","シューズ＆バッグ","ジュエリー","スポーツ＆アウトドア","デジタルミュージック","ドラッグストア","パソコン・周辺機器",
                 "ビューティー","ファッション","ベビー＆マタニティ","ペット用品","ホビー","ホーム＆キッチン","ミュージック","大型家電","家電＆カメラ",
                 "文房具・オフィス用品","服＆ファッション小物","本","楽器・音響機器","洋書","産業・研究開発用品","腕時計","車＆バイク",
                 "食品・飲料・お酒"]


path = r'D:\workspace\amazon\chromedriver.exe'

options = Options()
options.add_argument("--disable-extentions")
options.add_argument("--ignore-certificate-errors")
#options.add_argument("--headless")


driver = webdriver.Chrome(path, chrome_options=options)

driver.get("https://www.amazon.co.jp/trends/aps?ref=crw_ratp_ts")
time.sleep(random.randint(5,10))




#DBに登録
conn = sqlite3.connect(dbname)
c = conn.cursor()
sql = 'insert into AmazonRanking(trend, category, yymmdd) values (?,?,?)'
    
                         

for cl in categoryLists:
    
    try:
        driver.find_element_by_link_text(cl).click()
        time.sleep(random.randint(5,10))
        
        data = driver.page_source
        soup = BeautifulSoup(data,"lxml")
        
        hottrends = soup.find_all(class_="trending-keyword")
        
        for hottrend in hottrends:
            #print(hottrend.text)
            v = (hottrend.text.strip(), cl, yymmdd)
            c.execute(sql, v)
        
    except:
        pass
    
    
conn.commit()
conn.close()
 

driver.quit()

