# -*- coding: utf-8 -*-
"""
Created on Mon Jun 19 01:55:56 2017

@author: taketoshi
"""

import sqlite3
import os.path
import sys
import requests
import json
import urllib.request
url = r'https://www.gaitameonline.com/rateaj/getrate'

import urllib.request
import json


r = requests.get('https://www.gaitameonline.com/rateaj/getrate').json()
USD = r['quotes'][20]['ask']



print(r.text)

import bottlenose
from bs4 import BeautifulSoup
ACCESS_KEY = "AKIAIHLYHT6UO2GVALVQ"
SECRET_ACCESS_KEY = "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"
ASSOCIATE_TAG = "take061-22"


country = "JP"

sys.path.append(r'C:\Users\taketoshi\Anaconda3\envs\amazon\Lib\site-packages')
dbname = r'D:\workspace\sqlite\sample.sqlite3'
if os.path.exists(dbname) is False:
    dbname = r'C:\Users\VJP1311\workspace\sqlite\sample.sqlite3'



amazon = bottlenose.Amazon(ACCESS_KEY, SECRET_ACCESS_KEY, ASSOCIATE_TAG, Region=country)

conn = sqlite3.connect(dbname)
c = conn.cursor()
sql = 'select DISTINCT amazon.asin from amazon left outer join asin on (asin.asin = amazon.asin) where asin.asin is null;'
sql = 'select JP_ASIN from AnalyzeASIN where JP_ASIN = US_ASIN and JP_price > US_price * '
c.execute(sql)
asin = c.fetchall()
conn.close()

print("---")
