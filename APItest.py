# -*- coding: utf-8 -*-
"""
Created on Sun Feb  4 15:51:49 2018

@author: taketoshi

アマゾン検索機能が使えるか単純確認
"""

#import sqlite3
import datetime
import random
import AmazonClass
import csv
import sys
import time
from bs4 import BeautifulSoup
import mwstestClass


def get_contents(p, tag):
    if p.find(tag) is None:
        return "None"
    else:
        return p.find(tag).string
def get_price_jp(p):
    if p.find("landedprice") is None:
        return "None"
    else:
        return p.find("landedprice").find("amount").string

def get_price_us(p):
    if p.find("price") is None:
        return "None"
    else:
        return p.find("price").find("formattedprice").string


def get_price_us_old(p):
    if p.find("lowestnewprice") is None:
        return "None"
    else:
        return p.find("lowestnewprice").find("formattedprice").string

todaydetail  =    datetime.datetime.today()
yymmdd = todaydetail.strftime("%Y-%m-%d")
hhmmss = todaydetail.strftime("%H:%M:%S")


SellerID           = "A2ILL9FJMGGGDJ"
AWSAccesKeyId      = "AKIAIA4ALUSZTLIJU2IQ"
AWSSecretAccessKey = "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"

product = mwstestClass.Products(
    AWSAccessKeyId=AWSAccesKeyId,
    AWSSecretAccessKey=AWSSecretAccessKey,
    SellerId=SellerID,
    Region='US')
MarketplaceId      = product.domain#A1VC38T7YXB528


SearchWords = ["All"]

newlist = ["All"]
asins = ["B006GA7FEM"]
response = product.get_matching_product(MarketplaceId,asins)
soup = BeautifulSoup(response,"lxml")  
print(soup.prettify())




sys.exit()

ama = AmazonClass.AmazonOrigin()

for s in SearchWords:#検索キーワード
    for c in newlist:#カテゴリ名
        
        with open(r'D:\workspace\result2.csv','a',newline='') as f:
            writer = csv.writer(f)
            writer.writerow([s,c,yymmdd,hhmmss])
        
        response = product.list_matching_products(MarketplaceId, s, c)
        soup = BeautifulSoup(response,"lxml")  

        JP_ASIN = []
        JP_price = []
        JP_rank = []
        JP_category = []
        JP_manufacturer = []
        JP_title = []
        
        for p in soup.findAll("product"):
            JP_ASIN.append(get_contents(p, "asin"))
            JP_rank.append(get_contents(p, "rank"))
            JP_category.append(get_contents(p, "ns2:productgroup"))
            JP_manufacturer.append(get_contents(p, "ns2:manufacturer"))
            JP_title.append(get_contents(p, "ns2:title"))
            
        
        response = product.get_competitive_pricing_for_asin(MarketplaceId, JP_ASIN)
        soup = BeautifulSoup(response,"lxml")
        
        for p2 in soup.findAll("getcompetitivepricingforasinresult"):
            JP_price.append(get_price_jp(p2))
        
        #「,」区切りのASINを作る
        ASINs = ','.join('%s' % a for a in JP_ASIN)

        ##ItemlookupでUSを検索する
        US_ASIN = []
        US_price = []
        US_rank = []
        US_category = []
        US_manufacturer = []
        US_title = []
        
        
        
        ama.set_access_key("US")
        US_response = ama.AsinSearch2(ASINs)

        
        if US_response != "None":
        
        
            US_soup = BeautifulSoup(US_response,"lxml")
            

            
            for item in US_soup.findAll("item"):
                US_ASIN.append(get_contents(item, "asin"))
                US_price.append(get_price_us(item))
                US_rank.append(get_contents(item, "salesrank"))
                US_category.append(get_contents(item, "productgroup"))
                US_manufacturer.append(get_contents(item, "manufacturer"))
                US_title.append(get_contents(item, "title"))
        
        
print("終了")


