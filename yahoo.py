# -*- coding: utf-8 -*-
"""
Created on Sun May 21 02:50:39 2017
@author: taketoshi
"""


def getcontents(item, index):
    #print(item)
    try:
        
        if item is None:
            return "None"
        return item.contents[index]
    except:
        return "None"
    


import sys
sys.path.append(r'C:\Users\taketoshi\Anaconda3\envs\amazon\Lib\site-packages')
#sys.path.append(r'C:\Users\VJP1311\Anaconda3\envs\amazon\Lib\site-packages')
#import datetime
from bs4 import BeautifulSoup
#import sqlite3
import os.path
import urllib.request
import re
import sqlite3

dbname = r'D:\workspace\sqlite\sample.sqlite3'
if os.path.exists(dbname) is False:
    dbname = r'D:\workspace\sqlite\sample.sqlite3'

url = 'http://shopping.yahooapis.jp/ShoppingWebService/V1/itemSearch?appid=dj0zaiZpPUw4T2RoZHhmZTFJMSZzPWNvbnN1bWVyc2VjcmV0Jng9OGQ-&query=vaio&condition=new&hits=50'
#url = 'https://shopping.yahooapis.jp/ShoppingWebService/V1/categoryRanking?appid=dj0zaiZpPUw4T2RoZHhmZTFJMSZzPWNvbnN1bWVyc2VjcmV0Jng9OGQ-&category_id=2494'
response = urllib.request.urlopen(url)
#data = response.read()
soup = BeautifulSoup(response, "lxml")


prettify = soup.prettify()
#print(prettify)

conn = sqlite3.connect(dbname)
c = conn.cursor()
for item in soup.findAll(re.compile("^hit")):
    if getcontents(item.find("jancode"), 0) != "None":
        print(getcontents(item.find("name"), 0))
        print(getcontents(item.find("price"), 0))
        print(getcontents(item.find("jancode"), 0))
        '''
        sql = 'insert into yahoo(jancode, name, price) values(?,?,?)'
        val = (getcontents(item.find("jancode"), 0),getcontents(item.find("name"), 0), getcontents(item.find("price"), 0))
        c.execute(sql, val)
        conn.commit()
        break
        '''
    
        
conn.close()

#getcontents(item.find("publisher"), 0)

'''
f = open(r'D:\workspace\amazon.txt','wb')
f.write(prettify.encode('utf-8'))
f.close()
'''