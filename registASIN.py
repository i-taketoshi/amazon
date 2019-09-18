# -*- coding: utf-8 -*-
"""
Created on Mon Jun 19 01:55:56 2017
amazon DBから重複なしASIN検索、既存のASINDBと比較し、
新しいASINをASIN DBと比較しへ登録
@author: taketoshi
"""

import sqlite3
import os.path
import sys
import datetime
import random
import AmazonClass
import csv

dbname = r'D:\workspace\sqlite\sample.sqlite3'
 #DB接続

sys.path.append(r'C:\Users\taketoshi\Anaconda3\envs\amazon\Lib\site-packages')
import bottlenose
from bs4 import BeautifulSoup
ACCESS_KEY = "AKIAIHLYHT6UO2GVALVQ"
SECRET_ACCESS_KEY = "UOlJsX1JAhm8B3iLmIN5MnDJ47n84UkHUC26aUaB"
ASSOCIATE_TAG = "take061-22"


country = "JP"


dbname = r'D:\workspace\sqlite\sample.sqlite3'
if os.path.exists(dbname) is False:
    dbname = r'C:\Users\VJP1311\workspace\sqlite\sample.sqlite3'



amazon = bottlenose.Amazon(ACCESS_KEY, SECRET_ACCESS_KEY, ASSOCIATE_TAG, Region=country)

conn = sqlite3.connect(dbname)
c = conn.cursor()
#sql = 'select DISTINCT amazon.asin from amazon left outer join asin on (asin.asin = amazon.asin) where asin.asin is null;'
sql = 'select DISTINCT a3.asin from amazon3 as a3 left outer join AnalyzeASIN as a on (a.JP_ASIN = a3.asin) where a.JP_ASIN is null'
c.execute(sql)
asin = c.fetchall()
conn.close()

import itertools


#print(asin[0][0])
textlist = []
for a in itertools.zip_longest(*[iter(asin)]*10):
    textlist.append(','.join('%s' % b for b in a if b is not None))


'''
for t in textlist:
        #JPで検索
        response = amazon.ItemLookup(ItemId=t, ResponseGroup="ItemAttributes,Large")
        
        #USで検索
        pass
    
        

'''

response = amazon.ItemLookup(ItemId="B078HGG68W,123456G68W", ResponseGroup="ItemAttributes,Large")

soup = BeautifulSoup(response,"lxml")

#テキストへHTML情報書き込み
f = open(r'D:\workspace\amazon.txt','wb')
f.write(soup.prettify().encode('utf-8'))
f.close()

if soup.find("message") is not None:
    print("検索結果0")
    #sys.exit()    

#JP_ASIN,US_ASIN,JP_rank,US_rank,JP_price,US_price,yymmdd,do
#APIとSQL実行
JP_ASIN = []
JP_price = []
JP_rank = []
for item in soup.findAll("item"):
    #print(item.find("asin").string)
    JP_ASIN.append(item.find("asin").string)
    
    #print(item.find("listprice").find("amount").string)
    #print(item.find("lowestnewprice").find("amount").string)
    #print(item.find("price").find("amount").string)
    JP_price.append(item.find("price").find("amount").string)
    JP_rank.append(item.find("salesrank").string)
    


'''
USへのAPI実行後
'''    
US_ASIN = []
US_price = []
US_rank = []

todaydetail  =    datetime.datetime.today()
yymmdd = todaydetail.strftime("%Y-%m-%d")
#hhmmss = todaydetail.strftime("%H:%M:%S")

US_ASIN.append("123456G68W")
US_ASIN.append("B078HGG68W")
US_price.append("1000")
US_price.append("2000")
US_rank.append("10")
US_rank.append("20")

for i,jp in enumerate(JP_ASIN):
    if jp in US_ASIN:
        
        idx = US_ASIN.index(jp)
        
        print("カウント：" + str(idx))
        print("idx：" + str(idx))
        print(US_price[idx])

        val = (JP_ASIN[i], US_ASIN[idx], JP_price[i], US_price[idx], JP_rank[i], US_rank[idx], yymmdd,'1')

        sql = 'insert into AnalyzeAsin(JP_ASIN,US_ASIN,JP_rank,US_rank,JP_price,US_price,yymmdd,do) values(?,?,?,?,?,?,?,?)'
        print(sql,val)
        
conn = sqlite3.connect(dbname)
c = conn.cursor()

#val = (JP_ASIN[i], US_ASIN[idx], JP_price[i], US_price(idx), JP_rank[i], US_rank[idx], yymmdd,'1')

#sql = 'insert into AnalyzeAsin(JP_ASIN,US_ASIN,JP_rank,US_rank,JP_price,US_price,yymmdd,do) \
#        values(?,?,?,?,?,?,?,?)'

#c.execute(sql, val)
#conn.commit()
conn.close()

#print(sql,val)
    



