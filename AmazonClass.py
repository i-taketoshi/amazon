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

class AmazonOrigin:
    
            
    def __init__(self):
        self.searchMethod = "word"
        #self.searchMethod = "word"
        self.country = "JP"
        '''
        self.ACCESS_KEY = "AKIAIVNSYSDOII5JOAEA"
        self.SECRET_ACCESS_KEY = "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"
        self.ASSOCIATE_TAG = "tsunotsuki-22"
        
        
        self.ACCESS_KEY = "AKIAIZ57MAOLLMWZZBAQ"
        self.SECRET_ACCESS_KEY = "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"
        self.ASSOCIATE_TAG = "take"
        
        self.ACCESS_KEY = "AKIAJX7TZ7O4YLOTUCAQ"
        self.SECRET_ACCESS_KEY = "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"
        self.ASSOCIATE_TAG = "take0a-20"
        
        
        '''
        
        self.ACCESS_KEY = "AKIAI5YMAQGGHZ4KOZ2A"
        self.SECRET_ACCESS_KEY = "GBcYRiFqmwZD3PyS5N0Ks3Ohl7EC8MvS3qH5mBfU"
        self.ASSOCIATE_TAG = "take0e-22"



        self.dbname = r'D:\workspace\sqlite\sample.sqlite3'
        if os.path.exists(self.dbname) is False:
            self.dbname = r'C:\Users\VJP1311\workspace\sqlite\sample.sqlite3'

        self.amazon = bottlenose.Amazon(self.ACCESS_KEY, self.SECRET_ACCESS_KEY, self.ASSOCIATE_TAG, Region=self.country)
        
        
    def set_access_key(self, country):
        
        if country == "JP":
            self.ASSOCIATE_TAG = "take0e-22"
            self.ACCESS_KEY = "AKIAI5YMAQGGHZ4KOZ2A"
            self.SECRET_ACCESS_KEY = "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"
            self.country = "JP"
            self.amazon = bottlenose.Amazon(self.ACCESS_KEY, self.SECRET_ACCESS_KEY, self.ASSOCIATE_TAG, Region=self.country)

        else:
            self.ASSOCIATE_TAG = "take025-20"
            self.ACCESS_KEY = "AKIAJ5VV5S2OQBB2ZDIA"
            self.SECRET_ACCESS_KEY = "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"            
            self.country = "US"
            self.amazon = bottlenose.Amazon(self.ACCESS_KEY, self.SECRET_ACCESS_KEY, self.ASSOCIATE_TAG, Region=self.country)
        
        
        
        
    def getcontents(self, item, index):
        #print(item)
        if item is None:
            return "None"
        return item.contents[index]    
    
    def get_price(self, item, price):
        
        item.select(price)
        
        p = re.compile('[0-9]+')
        try:
            P = item.select(price)
            m = p.search(str(P[0]))
            return m.group(0)
        
        except:
            return "No price"
            
    def get_contents(self, item, tag):
        if item.find(tag) is None:
            return "None"
        else:
            return item.find(tag).string
    
    def GET_UNITS(self, item, dimension):
        
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
        
    def GET_DIMENSIONS(self, item, dimension):
        #if isinstance(item.find("ItemDimensions"),type(None)) == False:
        if isinstance(item.find("ItemDimensions"),type(None)) == True and \
           isinstance(item.find("PackageDimensions"),type(None)) == True:
                return "None"
                
        if isinstance(item.find("ItemDimensions").find(dimension),type(None)) == False:
            return item.find("ItemDimensions").find(dimension).string
        
        if isinstance(item.find("PackageDimensions").find(dimension),type(None)) == False:
            return item.find("PackageDimensions").find(dimension).string
        return "None"    
    
    def OnceSearch(self, keywords, category, sort, page):
        result = False
        for i in range(5):
                try:
                    if category == "":
                        response = self.amazon.ItemLookup(ItemId=keywords, ResponseGroup="ItemAttributes,Large")
                        return response
                    
                    else:
                        if category == "All":#Allの場合はソートなし
                            response = self.amazon.ItemSearch(Keywords=keywords, SearchIndex=category, ItemPage=page, ResponseGroup="ItemAttributes,Large")    
                        else:#ソートあり
                            response = self.amazon.ItemSearch(Keywords=keywords, SearchIndex=category, ItemPage=page, ResponseGroup="ItemAttributes,Large", Sort=sort) 
                    
                except:    
                    print("API err")

                    time.sleep(2)
                    continue
        else:
            if result == False:
                return "None"

    def DatabaseProcess(self, sql, val):
        #DB接続
        try:
            conn = sqlite3.connect(self.dbname)
            c = conn.cursor()
            c.execute(sql, val)
            conn.commit()
            conn.close()
            
            return "DB Process Success"
            
        except:
            return "DB Proces Fault"
      
    def AsinSearch2(self, asins):
            
            response = "None"
            
            #5回トライしてダメだめだったら諦める
            for i in range(5):
                try:
                    response = self.amazon.ItemLookup(ItemId=asins, ResponseGroup="ItemAttributes,Large")
                    break
                except:    
                    print("API err AsinSearch2")

                    time.sleep(2)
                    continue
                
            return response
        
    def KeyWordsSearch2(self, keywords, category, sort, page):
            
            response = False
            
            #5回トライしてダメだめだったら諦める
            for i in range(5):
                try:
                    if category == "All":#Allの場合はソートなし
                        response = self.amazon.ItemSearch(Keywords=keywords, SearchIndex=category, ItemPage=page, ResponseGroup="ItemAttributes,Large")
                    else:#ソートあり
                        response = self.amazon.ItemSearch(Keywords=keywords, SearchIndex=category, ItemPage=page, ResponseGroup="ItemAttributes,Large", Sort=sort) 
                    break

                except:    
                    print("API err KeyWordsSearch2")

                    time.sleep(2)
                    continue
                
            return response
        
    def WriteLog(self, *args):
    
        with open(r'D:\workspace\result.csv','a',newline='') as f:
            todaydetail  =    datetime.datetime.today()
            yymmdd = todaydetail.strftime("%Y-%m-%d")
            hhmmss = todaydetail.strftime("%H:%M:%S")
    
            writer = csv.writer(f)
            lists = list(args)
            lists.insert(0, "")
            lists.append(yymmdd)
            lists.append(hhmmss)
            writer.writerow(lists)
    
    def KeyWordsSearch(self, keywords, category, sort, page):
            
            #DB接続
            conn = sqlite3.connect(self.dbname)
            c = conn.cursor()
            result = "FAULT"
            
            #5回トライしてダメだめだったら諦める
            for i in range(5):
                try:
                    if category == "All":#Allの場合はソートなし
                        response = self.amazon.ItemSearch(Keywords=keywords, SearchIndex=category, ItemPage=page, ResponseGroup="ItemAttributes,Large")
                    else:#ソートあり
                        response = self.amazon.ItemSearch(Keywords=keywords, SearchIndex=category, ItemPage=page, ResponseGroup="ItemAttributes,Large", Sort=sort) 
                    
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
                    #print(self.get_contents(item, "asin"))
                    #print(self.get_contents(item, "ASIN"))

                    #テキストへHTML情報書き込み
                    f = open(r'D:\workspace\amazon.txt','wb')
                    f.write(soup.prettify().encode('utf-8'))
                    f.close()
                    try:
                        
                        if self.get_contents(item,"ASIN") == "None":
                            val = (self.get_contents(item, "asin"),  self.get_contents(item, "ean"),  self.get_contents(item, "title"),  self.get_contents(item, "edition"),  \
                                   self.get_contents(item, "isbn"),  self.get_contents(item, "productgroup"),  self.get_price(item, "listprice > amount"),  \
                                   self.get_price(item, "lowestnewprice > amount"),  self.get_price(item, "lowestusedprice > amount"),  self.get_price(item, "price > amount"),  \
                                   self.get_contents(item, "salesrank"), self.get_contents(item, "manufacturer"),  self.GET_DIMENSIONS(item, "height"), self.GET_UNITS(item, "height"), self.GET_DIMENSIONS(item, "length"), self.GET_UNITS(item, "length"),  \
                                   self.GET_DIMENSIONS(item, "width"), self.GET_UNITS(item, "width"),  self.GET_DIMENSIONS(item, "weight"), self.GET_UNITS(item, "weight"), self.get_contents(item, "producttypeName"),  self.get_contents(item, "publisher"),  \
                                   self.get_contents(item, "studio"),  self.country,  self.get_contents(item, "detailpageurl"),  yymmdd,  hhmmss)

                            
                        else:
                            
                            val = (self.get_contents(item, "ASIN"),  self.get_contents(item, "EAN"),  self.get_contents(item, "Title"),  self.get_contents(item, "Edition"),  \
                                   self.get_contents(item, "ISBN"),  self.get_contents(item, "ProductGroup"),  self.get_price(item, "ListPrice > Amount"),  \
                                   self.get_price(item, "LowestNewPrice > Amount"),  self.get_price(item, "LowestUsedPrice > Amount"),  self.get_price(item, "Price > Amount"),  \
                                   self.get_contents(item, "SalesRank"), self.get_contents(item, "Manufacturer"),  self.GET_DIMENSIONS(item, "Height"), self.GET_UNITS(item, "Height"), self.GET_DIMENSIONS(item, "Length"), self.GET_UNITS(item, "Length"),  \
                                   self.GET_DIMENSIONS(item, "Width"), self.GET_UNITS(item, "Width"),  self.GET_DIMENSIONS(item, "Weight"), self.GET_UNITS(item, "Weight"), self.get_contents(item, "ProductTypeName"),  self.get_contents(item, "Publisher"),  \
                                   self.get_contents(item, "Studio"),  self.country,  self.get_contents(item, "DetailPageURL"),  yymmdd,  hhmmss)

                        sql = 'insert into amazon3(ASIN, EAN, Title, Edition, ISBN, ProductGroup, ListPrice, LowestNewPrice, LowestUsedPrice, Price, SalesRank,Manufacturer, Height, Heightunits, Length, Lengthunits, Width, Widthunits, Weight, Weightunits, \
                                                   ProductTypeName, Publisher, Studio, Country, DetailPageURL, yymmdd, hhmmss) values(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)'
    
                        c.execute(sql, val)
                    except:
                        print("SQL err")
                        
                    conn.commit()
                
                break
                                
                
            conn.close()
            
            return result

if __name__ == '__main__':

    #ao = AmazonOrigin()
    #response = ao.KeyWordsSearch(keywords="天木じゅん", category="All", sort="l", page="1")
    
    #amazon.ItemSearch(Keywords="天木じゅん", SearchIndex="All", ItemPage="1", ResponseGroup="ItemAttributes,Large")

    list = [
        ["All","dammy"],
        ["Apparel","price"],
    ]
    SearchWords = ["日本未発売","海外"]
    ListIndex = ["All","Apparel"]
    
    ao = AmazonOrigin()
    result = ao.KeyWordsSearch(keywords="B016R90VBK", category="All", sort="-price", page="1")
    print(result)
    '''
    #検索キーワード、カテゴリ、ソート
    for s in SearchWords:#検索キーワード
        for i in range(len(ListIndex)):#カテゴリ名
            for j in range(len(list[i])-1):#ソート方法
                for p in range(0,1):#ページ番号分

                    #print("ワード：{0}, カテゴリ：{1}, ソート：{2}, ページ：{3}".format(s, ListIndex[i], list[i][j+1], p+1))
                    result = ao.KeyWordsSearch(keywords=s, category=ListIndex[i], sort=list[i][j+1], page=p+1)
                    
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
                        
    '''             
                        
    
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

 
