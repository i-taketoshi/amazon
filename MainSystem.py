# -*- coding: utf-8 -*-
"""
Created on Sun Feb  4 15:51:49 2018

@author: taketoshi
"""

import sqlite3
import datetime
import random
import AmazonClass
import csv
import sys
from bs4 import BeautifulSoup

def get_contents(tag):
    if item.find(tag) is None:
        return "None"
    else:
        return item.find(tag).string

def get_price(tag):
    if item.find(tag) is None:
        return "None"
    else:
        return item.find("price").find("amount").string

dbname = r'D:\workspace\sqlite\sample.sqlite3'
 #DB接続
conn = sqlite3.connect(dbname)
c = conn.cursor()


todaydetail  =    datetime.datetime.today()
yymmdd = todaydetail.strftime("%Y-%m-%d")
hhmmss = todaydetail.strftime("%H:%M:%S")


#アマゾンテーブルから検索用のワードを検索する                            
sql = u"select * from amazonranking where yymmdd = '" + yymmdd + "'"
c.execute(sql)
amazonranking = c.fetchall()

#グーグルテーブルから検索用のワードを検索する
sqlg = u"select * from google where yymmdd = '" + yymmdd + "'"
c.execute(sqlg)

#検索済みにチェックをする
google = c.fetchall()
for g in google:
    updateg = "update google set do = 1 where no = " + str(g[0]);                                                          
    c.execute(updateg)


#検索用のワードのみを取得
googletrend = []
for row in google:
    googletrend.append(row[1])
    

#ランダムでアマゾンランキングを抽出
index = random.sample(range(1, len(amazonranking)), 10)#抽出する添字を取得
SearchWords = [amazonranking[i][1] for i in index]

#検索済みにチェックをする
for i in index:
    updatea = "update amazonranking set do = 1 where no = " + str(amazonranking[i][0]);
    c.execute(updatea)

conn.commit()
conn.close()


#Googleトレンドとアマゾンランキングを結合
for g in googletrend:
    SearchWords.append(g)



list = [
    ["All",""],
    ["Apparel","salesrank","-price","relevancerank"],
    ["Automotive","salesrank","relevancerank","-price","reviewrank"],
    ["Beauty","-price","relevancerank","reviewrank"],
    ["Classical","salesrank","-pricerank","-price","titlerank","-titlerank","-orig-rel-date","orig-rel-date","releasedate","-releasedate"],
    ["DVD","salesrank","-pricerank","-price","titlerank","-titlerank","-orig-rel-date","orig-rel-date","releasedate","-releasedate"],
    ["Electronics","salesrank","-price","titlerank","-titlerank","-releasedate","releasedate"],
    ["HealthPersonalCare","salesrank","inverse-pricerank","daterank","titlerank","-titlerank"],
    ["Hobbies","salesrank","-price","titlerank","-titlerank","release-date","-release-date","mfg-age-min","-mfg-age-min"],
    ["HomeImprovement","salesrank","-price","reviewrank"],    
    ["Kitchen","salesrank","-price","titlerank","-titlerank","-release-date","release-date"],
    ["Music","salesrank","-pricerank","-price","titlerank","-titlerank","-orig-rel-date","orig-rel-date","releasedate","-releasedate"],    
    ["OfficeProducts","salesrank","-price","relevancerank","reviewrank"],
    ["Shoes","salesrank","-price","titlerank","-titlerank","-release-date","release-date","releasedate","-releasedate"],    
    ["SportingGoods","salesrank","-price","titlerank","-titlerank","releasedate","-releasedate"],
    ["Toys","salesrank","-price","titlerank","-titlerank","-release-date","release-date"],    
    ["Video","salesrank","-price","-pricerank","titlerank","-titlerank","-orig-rel-date","orig-rel-date","releasedate","-releasedate"],
    ["VideoGames","salesrank","-price","titlerank","-titlerank","-release-date","release-date"]
    
]
#["Baby","salesrank","-price","titlerank"],
#["Watches","salesrank","-price","titlerank","-titlerank"]

#検索カテゴリをランダムで選択
index = random.sample(range(1,len(list)), 9)#抽出する添字を取得
randomList = [list[i] for i in index]
randomList.insert(0, list[0])

#処理回数を記載
cnt = 0
for r in randomList:
    cnt += len(r)



ama = AmazonClass.AmazonOrigin()
loopcnt = 0
page = 5

#検索キーワード、カテゴリ、ソート
for s in SearchWords:#検索キーワード
    for i in range(len(randomList)):#カテゴリ名
        for j in range(len(randomList[i])-1):#ソート方法
            for p in range(0,page):#ページ番号分
                #print("ワード：{0}, カテゴリ：{1}, ソート：{2}, ページ：{3}".format(s, ListIndex[i], list[i][j+1], p+1))
                loopcnt +=1
                print(str(loopcnt) +"回目の処理")
                #response = ama.KeyWordsSearch2(keywords="s", category="All", sort="-price", page='1')
                #日本ASIN検索
                
                print(j)
                
                print(randomList[i][j+1])
                
                ama.set_access_key("JP")
                response = ama.KeyWordsSearch2(keywords=str(s), category=str(randomList[i][0]), sort=str(randomList[i][j+1]), page=str(p+1))
                
                
                #ログの取得
                #検索ワード、カテゴリ、ソート、ページ数、進捗,成否
                if response != False:
                    soup = BeautifulSoup(response,"lxml")
                    ama.WriteLog(s,randomList[i][0],randomList[i][j+1],p+1,str(loopcnt) + "/" + str((cnt-10)*5) + "回目の処理",True)
                else:
                    ama.WriteLog(ama.WriteLog(s,randomList[i][0],randomList[i][j+1],p+1,str(loopcnt) + "/" + str((cnt-10)*5) + "回目の処理"),"False")
                    break


                #配列の初期化
                JP_ASIN = []
                JP_price = []
                JP_rank = []
                JP_category = []
                JP_manufacturer = []
                JP_title = []
                ASINs = ""
                
                #入手した情報を格納
                for item in soup.findAll("item"):
                    JP_ASIN.append(get_contents("asin"))
                    JP_price.append(get_price("price"))
                    JP_rank.append(get_contents("salesrank"))
                    JP_category.append(get_contents("productgroup"))
                    JP_manufacturer.append(get_contents("manufacturer"))
                    JP_title.append(get_contents("title"))
                
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
                    f = open(r'D:\workspace\amazon.txt','wb')
                    f.write(US_soup.prettify().encode('utf-8'))
                    f.close()
                    for item in US_soup.findAll("item"):
                        print(get_contents("title"))
                        US_ASIN.append(get_contents("asin"))
                        US_price.append(get_price("price"))
                        US_rank.append(get_contents("salesrank"))
                        US_category.append(get_contents("productgroup"))
                        US_manufacturer.append(get_contents("manufacturer"))
                        US_title.append(get_contents("title"))
  
                
                for a,b in enumerate(JP_ASIN):
                    try:
                        idx = US_ASIN.index(b)
                                
                    except ValueError:
                        idx = 9999
                    
                    #USのAPIが失敗してた時 or USのASINがない時
                    if idx == 9999:
                        
                        val = (JP_ASIN[a], "", JP_price[a], "", JP_rank[a], "", JP_title[a], "",JP_category[a],JP_manufacturer[a],yymmdd,'1')
                        sql = 'insert into ASINs(JP_ASIN,US_ASIN,JP_rank,US_rank,JP_price,US_price,JP_title,US_title,category,manufacturer,yymmdd,do) values(?,?,?,?,?,?,?,?,?,?,?,?)'
                        
                    else:
                        
                        val = (JP_ASIN[a], US_ASIN[idx], JP_price[a], US_price[idx], JP_rank[a], US_rank[idx], JP_title[a], US_title[idx],JP_category[a],JP_manufacturer[a],yymmdd,'1')
                        sql = 'insert into ASINs(JP_ASIN,US_ASIN,JP_rank,US_rank,JP_price,US_price,JP_title,US_title,category,manufacturer,yymmdd,do) values(?,?,?,?,?,?,?,?,?,?,?,?)'

                    db_r = ama.DatabaseProcess(sql,val)
                    print(db_r)
                
print("処理終了")