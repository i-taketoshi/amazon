# -*- coding: utf-8 -*-
"""
Created on Sat Feb  3 16:44:07 2018

@author: taketoshi
"""


from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.chrome.options import Options
import time
#from selenium.webdriver.support.ui import WebDriverWait
#from selenium.webdriver.support import expected_conditions as EC
#from selenium.webdriver.common.by import By

import csv
import numpy as np

from statistics import mean, median,variance,stdev


path = r'D:\workspace\amazon\chromedriver.exe'

options = Options()
options.add_argument("--disable-extentions")
options.add_argument("--ignore-certificate-errors")
#options.add_argument("--headless")


driver = webdriver.Chrome(path, chrome_options=options)

driver.get("http://mnrate.com/item/aid/B00GKFM0KC")
time.sleep(3)

data = driver.page_source
soup = BeautifulSoup(data,"lxml")

prettify = soup.prettify()    
f = open(r'D:\workspace\GoogleTrend.txt','wb')
f.write(prettify.encode('utf-8'))
f.close()



#エラー処理（データ取得不可時）
try:
    
    item_price_sheet = soup.find(class_='item_price_sheet').get_text()
    if item_price_sheet.find('データを取得できませんでした') > 0:
        print("取得失敗")
except:
    print("None Type")


#テーブルを指定
table = soup.find(id="sheet_contents")
rows = table.findAll("tr")

rank = []
try:
    for row in rows:
        csvRow = []
        for cell in row.findAll(['td', 'th']):
            csvRow.append(str.strip(cell.get_text()))
        
        if len(csvRow) > 1 and  csvRow[1] != "":
                rank.append(int(csvRow[1]))
#        writer.writerow(csvRow)
except:
    pass
    #csvFile.close()


#販売個数取得
cnt = 0
cnt2 = 0

if len(rank) != 0:
    
    mn = min(rank)
    ranklist = ','.join(map(str,rank))
    
    for i in range(len(rank)-1):
        #前日よりランキングが上(数値指摘には下)ならカウント
        if rank[i] > rank[i+1]:
            cnt+=1
        
        #前日よりランキングが2割下がった
        if rank[i]*0.8 > rank[i+1]:
            cnt2+=1
        
    
    print("---------")
    print("rank上昇回数：" + str(cnt) + ',' + str(cnt2))
    print(mn)
    #print("rank下落率が平均値の1割以内：" + str(cnt2))

    
else:
   pass
    

                           
driver.quit()



'''
f = open(r'D:\workspace\GoogleTrend.txt','rb')
data = f.read()  # ファイル終端まで全て読んだデータを返す
f.close()
'''

#soup = BeautifulSoup(data,"lxml")

#print(soup.prettify())

print("################")