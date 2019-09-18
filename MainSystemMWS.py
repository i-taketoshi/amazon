# -*- coding: utf-8 -*-
"""
Created on Sun Feb  4 15:51:49 2018

@author: taketoshi

DBから検索用ワードを抽出し、MWSで商品を検索する
検索した商品をUSのPA-APIで検索し、
JPとUSの商品情報を入手する


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

list = [
"All","Apparel","Automotive","Baby","Beauty","Books","DVD","Electronics","HealthPersonalCare",
"Hobbies","HomeImprovement","Kitchen","Music","MusicalInstruments","OfficeProducts","Shoes",
"Software","SportingGoods","Toys","Video","VideoGames","Watches"
]
'''
"Classical","MusicTracks","VHS","MP3Downloads","Jewelry","Grocery","ForeignBooks",
'''

SellerID           = "--------------------------"
AWSAccesKeyId      = "--------------------------"
AWSSecretAccessKey = "--------------------------"

product = mwstestClass.Products(
    AWSAccessKeyId=AWSAccesKeyId,
    AWSSecretAccessKey=AWSSecretAccessKey,
    SellerId=SellerID,
    Region='JP')
MarketplaceId      = product.domain#A1VC38T7YXB528




SearchWords = product.get_searchwords(yymmdd,'All')


if SearchWords == 0:
    print("検索ワードがDBから検索できません。システムを強制終了します")
    
    #list = ["All"]
    #SearchWords = ["ベイブレード"]
    sys.exit()

ama = AmazonClass.AmazonOrigin()



#ランダムでカテゴリを10個抽出
#Allは固定
index = random.sample(range(2, len(list)), 10)#抽出する添字を取得
index.insert(0,0)

newlist= [list[idx] for idx in index]

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
        
        
        for a,b in enumerate(JP_ASIN):
            #JPASINとUSASINの要素番号を合わせる
            try:
                idx = US_ASIN.index(b)
                val = (JP_ASIN[a], US_ASIN[idx], JP_price[a], US_price[idx], JP_rank[a], US_rank[idx], JP_title[a], US_title[idx],JP_category[a],JP_manufacturer[a],yymmdd,'1')

            #USにJPのASINがないときの処理
            except ValueError:
                val = (JP_ASIN[a], "", JP_price[a], "", JP_rank[a], "", JP_title[a], "",JP_category[a],JP_manufacturer[a],yymmdd,'1')
                
            sql = 'insert into ASINs(JP_ASIN,US_ASIN,JP_price,US_price,JP_rank,US_rank,JP_title,US_title,category,manufacturer,yymmdd,do) values(?,?,?,?,?,?,?,?,?,?,?,?)'

            db_r = ama.DatabaseProcess(sql,val)
            print(db_r)
        
        time.sleep(7)
        

        
print("終了")


