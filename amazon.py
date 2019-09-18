# -*- coding: utf-8 -*-
"""
Spyderエディタ
これは一時的なスクリプトファイルです
ランダムキーワードから商品を検索するプログラム

完成。
SearchWordsさえ渡せば動く

ASIN検索はItemLookUP
JAN検索はItemSearch
"""

import sys
sys.path.append(r'C:\Users\taketoshi\Anaconda3\envs\amazon\Lib\site-packages')
#sys.path.append(r'C:\Users\VJP1311\Anaconda3\envs\amazon\Lib\site-packages')
import datetime
import bottlenose
import sqlite3
import time
import re
import os.path
from bs4 import BeautifulSoup
global item
import csv


ACCESS_KEY = "AKIAIVNSYSDOII5JOAEA"
SECRET_ACCESS_KEY = "xljOT/AAHxo7dzHs5jQ+ZIh0h9wYEQviPFiiO+58"
ASSOCIATE_TAG = "tsunotsuki-22"

country = "JP"
dbname = r'D:\workspace\sqlite\sample.sqlite3'
if os.path.exists(dbname) is False:
    dbname = r'C:\Users\VJP1311\workspace\sqlite\sample.sqlite3'
    

amazon = bottlenose.Amazon(ACCESS_KEY, SECRET_ACCESS_KEY, ASSOCIATE_TAG, Region=country)

def getcontents(item, index):
    #print(item)
    if item is None:
        return "None"
    return item.contents[index]    

def get_price(item, price):
    p = re.compile('[0-9]+')
    try:
        P = item.select(price)
        m = p.search(str(P[0]))
        return m.group(0)
    
    except:
        return "No price"
        
def get_contents(item, tag):
    if item.find(tag) is None:
        return "None"
    else:
        return item.find(tag).string

def GET_UNITS(item, dimension):
    
    r = re.compile("{\'Units\': \'(\\w+)\'}")
    
    if isinstance(item.find("ItemDimensions"),type(None)) == True and \
       isinstance(item.find("PackageDimensions"),type(None)) == True:
            return "None"
    
    
    if isinstance(item.find("ItemDimensions").find(dimension),type(None)) == False:
            Dimension_attrs = str(item.find("ItemDimensions").find(dimension).attrs)
            return r.sub(r"\1", Dimension_attrs)
    
    if isinstance(item.find("PackageDimensions").find(dimension),type(None)) == False:
            Dimension_attrs = str(item.find("PackageDimensions").find(dimension).attrs)
            return r.sub(r"\1", Dimension_attrs)
    
    return "None"
    
def GET_DIMENSIONS(item, dimension):
    #if isinstance(item.find("ItemDimensions"),type(None)) == False:
    if isinstance(item.find("ItemDimensions"),type(None)) == True and \
       isinstance(item.find("PackageDimensions"),type(None)) == True:
            return "None"
            
    if isinstance(item.find("ItemDimensions").find(dimension),type(None)) == False:
        return item.find("ItemDimensions").find(dimension).string
    
    if isinstance(item.find("PackageDimensions").find(dimension),type(None)) == False:
        return item.find("PackageDimensions").find(dimension).string
    return "None"    

def KeyWordsSearch(keywords, category, sort, page):
        
        #DB接続
        conn = sqlite3.connect(dbname)
        c = conn.cursor()
        result = "FAULT"
        
        #5回トライしてダメだめだったら諦める
        for i in range(5):
            try:
                if category == "All":#Allの場合はソートなし
                    response = amazon.ItemSearch(Keywords=keywords, SearchIndex=category, ItemPage=page, ResponseGroup="ItemAttributes,Large")                     
                else:#ソートあり
                    response = amazon.ItemSearch(Keywords=keywords, SearchIndex=category, ItemPage=page, ResponseGroup="ItemAttributes,Large", Sort=sort) 
                
                result = "SUCCESS"
            except:    
                print("API err")
                time.sleep(2)
                continue
                
            #1時間2000制限用
            time.sleep(1.8)
            
            #API実行時間取得
            todaydetail  =    datetime.datetime.today()
            yymmdd = todaydetail.strftime("%Y-%m-%d")
            hhmmss = todaydetail.strftime("%H:%M:%S")
            
            soup = BeautifulSoup(response,"lxml")
            
            #検索結果0
            if soup.find("message") is not None:
                
                conn.close()
                return None
            
            #APIとSQL実行
            for item in soup.findAll("item"):
                try:
                    val = (get_contents(item, "ASIN"),  get_contents(item, "EAN"),  get_contents(item, "Title"),  get_contents(item, "Edition"),  \
                           get_contents(item, "ISBN"),  get_contents(item, "ProductGroup"),  get_price(item, "ListPrice > Amount"),  \
                           get_price(item, "LowestNewPrice > Amount"),  get_price(item, "LowestUsedPrice > Amount"),  get_price(item, "Price > Amount"),  \
                           get_contents(item, "SalesRank"), get_contents(item, "Manufacturer"),  GET_DIMENSIONS(item, "Height"), GET_UNITS(item, "Height"), GET_DIMENSIONS(item, "Length"), GET_UNITS(item, "Length"),  \
                           GET_DIMENSIONS(item, "Width"), GET_UNITS(item, "Width"),  GET_DIMENSIONS(item, "Weight"), GET_UNITS(item, "Weight"), get_contents(item, "ProductTypeName"),  get_contents(item, "Publisher"),  \
                           get_contents(item, "Studio"),  country,  get_contents(item, "DetailPageURL"),  yymmdd,  hhmmss)
                    val = (get_contents(item, "asin"),  get_contents(item, "ean"),  get_contents(item, "title"),  get_contents(item, "edition"),  \
                           get_contents(item, "isbn"),  get_contents(item, "productgroup"),  get_price(item, "listprice > amount"),  \
                           get_price(item, "lowestnewprice > amount"),  get_price(item, "lowestusedprice > amount"),  get_price(item, "price > amount"),  \
                           get_contents(item, "salesrank"), get_contents(item, "manufacturer"),  GET_DIMENSIONS(item, "height"), GET_UNITS(item, "height"), GET_DIMENSIONS(item, "length"), GET_UNITS(item, "length"),  \
                           GET_DIMENSIONS(item, "width"), GET_UNITS(item, "width"),  GET_DIMENSIONS(item, "weight"), GET_UNITS(item, "weight"), get_contents(item, "producttypename"),  get_contents(item, "publisher"),  \
                           get_contents(item, "studio"),  country,  get_contents(item, "detailpageurl"),  yymmdd,  hhmmss)
                    sql = 'insert into amazon3(ASIN, EAN, Title, Edition, ISBN, ProductGroup, ListPrice, LowestNewPrice, LowestUsedPrice, Price, SalesRank,Manufacturer, Height, Heightunits, Length, Lengthunits, Width, Widthunits, Weight, Weightunits, \
                                               ProductTypeName, Publisher, Studio, Country, DetailPageURL, yymmdd, hhmmss) values(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)'

                    c.execute(sql, val)
                except:
                    print("SQL err")
                    
                conn.commit()
            
            break
                            
            
        conn.close()
        
        return result


'''            
list = [
    ["All"."dammy"],
    ["Apparel","price","-price","relevancerank","salesrank"],
    ["Automotive","relevancerank","salesrank","price","-price","reviewrank"],
    ["Baby","psrank","salesrank","price","-price","titlerank"],
    ["Beauty","price","-price","relevancerank","reviewrank"],
    ["Classical","salesrank","pricerank","-pricerank","price","-price","titlerank","-titlerank","-orig-rel-date","orig-rel-date","releasedate","-releasedate"],
    ["DVD","salesrank","pricerank","-pricerank","price","-price","titlerank","-titlerank","-orig-rel-date","orig-rel-date","releasedate","-releasedate"],
    ["Electronics","salesrank","price","-price","titlerank","-titlerank","-releasedate","releasedate"],
    ["HealthPersonalCare","salesrank","pricerank","inverse-pricerank","daterank","titlerank","-titlerank"],
    ["Hobbies","salesrank","price","-price","titlerank","-titlerank","release-date","-release-date","mfg-age-min","-mfg-age-min"],
    ["HomeImprovement","salesrank","price","-price","reviewrank"],    
    ["Kitchen","salesrank","price","-price","titlerank","-titlerank","-release-date","release-date"],
    ["Music","salesrank","pricerank","-pricerank","price","-price","titlerank","-titlerank","-orig-rel-date","orig-rel-date","releasedate","-releasedate"],    
    ["OfficeProducts","salesrank","price","-price","relevancerank","reviewrank"],
    ["Shoes","salesrank","price","-price","titlerank","-titlerank","-release-date","release-date","releasedate","-releasedate"],    
    ["SportingGoods","salesrank","price","-price","titlerank","-titlerank","releasedate","-releasedate"],
    ["Toys","salesrank","price","-price","titlerank","-titlerank","-release-date","release-date"],    
    ["Video","salesrank","price","-price","pricerank","-pricerank","titlerank","-titlerank","-orig-rel-date","orig-rel-date","releasedate","-releasedate"],
    ["VideoGames","salesrank","price","-price","titlerank","-titlerank","-release-date","release-date"],
    ["Watches","salesrank","price","-price","titlerank","-titlerank"]

    
    ["ForeignBooks","salesrank","pricerank","inverse-pricerank","daterank","titlerank","-titlerank"],
    ["VHS","salesrank","pricerank","-pricerank","price","-price","titlerank","-titlerank","-orig-rel-date","orig-rel-date","releasedate","-releasedate"],
    ["Software","salesrank","price","-price","titlerank","-titlerank","releasedate","-releasedate"],
    ["MusicTracks","titlerank","-titlerank"],
    ["Jewelry","salesrank","price","-price","reviewrank"],
    ["Grocery","salesrank","price","-price","reviewrank"],
    ["Books","salesrank","pricerank","inverse-pricerank","daterank","titlerank","-titlerank"],
]
SearchWords = [
            "日本未発売","海外","USA","米国",
            "英国","世界限定","限定","希少",
            "コラボ ","limited edition","着用モデル","廃盤",
            "廃番","国内発送","即納","並行輸入","import",
            "輸入","インポート","北米","アメリカ",
            "並行輸入　ランキング","並行輸入　おもちゃ"
        ]
ListIndex = [
    "All","Apparel","Automotive","Baby",
    "Beauty","Books","Classical","DVD",
    "Electronics","ForeignBooks","Grocery","HealthPersonalCare",
    "Hobbies","HomeImprovement","Jewelry","Kitchen",
    "Music","MusicTracks","OfficeProducts","Shoes",
    "Software","SportingGoods","Toys","VHS",
    "Video","VideoGames","Watches"
]
'''

if __name__ == '__main__':

    list = [
        ["All","dammy"],
        ["Apparel","price"],
    ]
    SearchWords = ["日本未発売","海外"]
    ListIndex = ["All","Apparel"]
    

    #検索キーワード、カテゴリ、ソート
    for s in SearchWords:#検索キーワード
        for i in range(len(ListIndex)):#カテゴリ名
            for j in range(len(list[i])-1):#ソート方法
                for p in range(0,1):#ページ番号分

                    #print("ワード：{0}, カテゴリ：{1}, ソート：{2}, ページ：{3}".format(s, ListIndex[i], list[i][j+1], p+1))
                    result = KeyWordsSearch(keywords=s, category=ListIndex[i], sort=list[i][j+1], page=p+1)
                    
                    if result is None:
                        break
                    else:
                        csvFile = open(r"D:\workspace\result.csv", 'at', newline = '', encoding='shift_jis')
                        
                        writer = csv.writer(csvFile)
                        
                        #検索結果を記載
                        try:
                            
                            csvRow = []
                            csvRow.append("")
                            csvRow.append(s)
                            csvRow.append(ListIndex[i])
                            csvRow.append(list[i][j+1])
                            csvRow.append(p+1)
                            todaydetail  =    datetime.datetime.today()
                            yymmdd = todaydetail.strftime("%Y-%m-%d")
                            hhmmss = todaydetail.strftime("%H:%M:%S")
                            csvRow.append(yymmdd)
                            csvRow.append(hhmmss)
                            
                            
                            writer.writerow(csvRow)
                            
                        finally:
                            csvFile.close()

                        print(result)
                    
    print("処理終了")
