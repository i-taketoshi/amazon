# -*- coding: utf-8 -*-
"""
Created on Sun May 21 02:50:39 2017
@author: taketoshi
"""

def getcontents(item, index):
    #print(item)
    if item is None:
        return "None"
    return item.contents[index]    

import sys
sys.path.append(r'C:\Users\taketoshi\Anaconda3\envs\amazon\Lib\site-packages')
#sys.path.append(r'C:\Users\VJP1311\Anaconda3\envs\amazon\Lib\site-packages')
import datetime
import bottlenose
from bs4 import BeautifulSoup
import sqlite3

dbname = r'D:\workspace\sqlite\sample.sqlite3'

#from bs4 import BeautifulStoneSoup

ACCESS_KEY = "AKIAIVNSYSDOII5JOAEA"
SECRET_ACCESS_KEY = "xljOT/AAHxo7dzHs5jQ+ZIh0h9wYEQviPFiiO+58"
ASSOCIATE_TAG = "tsunotsuki-22"
countory = "JP"

amazon = bottlenose.Amazon(ACCESS_KEY, SECRET_ACCESS_KEY, ASSOCIATE_TAG, Region="JP")
SearchIndex = ["All",
                "All",
                "Apparel",
                "Automotive",
                "Baby",
                "Beauty",
                "Books",
                "Classical",
                "DVD",
                "Electronics",
                "ForeignBooks",
                "Grocery",
                "HealthPersonalCare",
                "Hobbies",
                "HomeImprovement",
                "Jewelry",
                "Kitchen",
                "Music",
                "MusicTracks",
                "OfficeProducts",
                "Shoes",
                "Software",
                "SportingGoods",
                "Toys",
                "VHS",
                "Video",
                "VideoGames",
                "Watches",
            ]



try:
    response = amazon.ItemSearch(Keywords="人工知能", SearchIndex="All", ItemPage="5", ResponseGroup="ItemAttributes")
except:
    print("err")
    import traceback
    traceback.print_exc()


soup = BeautifulSoup(response,"lxml")
prettify = soup.prettify()

if soup.find("message") is None:
    print("ないよ")
else:
    print("aruyo")

country = "JP"
todaydetail  =    datetime.datetime.today()

for item in soup.findAll("item"):
    print(item.find("amount"))
   # print(item.find("ean").contents[0])
   #print(getcontents(item.find("ean"), 0))
#sql = 'insert into amazon(asin,ean,title,edition,isbn,productgroup,listprice,rank,manufacturer,\
#                            height,length,width,weight,producttypename,publisher,studio,countory,\
#                            detailpageurl,yymmdd,hhmmss) values(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)'
v1 = ("asin", "ean", "title", "edition", \
       "isbn", "productgroup", "listprice", "rank", \
                  "manufacturer", "height", "length", \
                             "width", "weight", "producttypename", \
                                        "publisher", "studio", "country", "detailpageurl", "yymmdd", "hhmmss")

val = (getcontents(item.find("asin"), 0), getcontents(item.find("ean"), 0), getcontents(item.find("title"), 0), getcontents(item.find("edition"), 0), \
       getcontents(item.find("isbn"), 0), getcontents(item.find("productgroup"), 0), getcontents(item.find("amount"), 0), getcontents(item.find("rank"), 0), \
                  getcontents(item.find("manufacturer"), 0), getcontents(item.find("height"), 0), getcontents(item.find("length"), 0), \
                             getcontents(item.find("width"), 0), getcontents(item.find("weight"), 0), getcontents(item.find("producttypename"), 0), \
                                        getcontents(item.find("publisher"), 0), getcontents(item.find("studio"), 0), country, getcontents(item.find("detailpageurl"), 0), todaydetail.strftime("%Y-%m-%d"), todaydetail.strftime("%H:%M:%S"))
   


#f = open(r'D:\workspace\amazon.txt','w')
f = open(r'D:\workspace\amazon.csv','w')
#f = open(r'C:\Users\VJP1311\workspace\webAPI\amazon.txt','wb')
#f.write(prettify.encode('utf-8'))
import csv
writer = csv.writer(f,dialect="excel")
writer.writerow(v1)
writer.writerow(val)
f.close()


f = open(r'D:\workspace\amazon.txt','wb')
f.write(prettify.encode('utf-8'))
f.close()

todaydetail  =    datetime.datetime.today()
yymmdd = todaydetail.strftime("%Y-%m-%d")
hhmmss = todaydetail.strftime("%H:%M:%S")

conn = sqlite3.connect(dbname)
c = conn.cursor()

# 一度に複数のSQL文を実行したいときは，タプルのリストを作成した上で
# executemanyメソッドを実行する
sql = 'insert into amazon(asin,ean,title,edition,isbn,productgroup,listprice,rank,manufacturer,\
                            height,length,width,weight,producttypename,publisher,studio,countory,\
                            detailpageurl,yymmdd,hhmmss) values(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)'
val = (getcontents(item.find("asin"), 0), getcontents(item.find("ean"), 0), getcontents(item.find("title"), 0), \
       getcontents(item.find("edition"), 0), getcontents(item.find("isbn"), 0), getcontents(item.find("productgroup"), 0), \
       getcontents(item.find("listprice"), 0), getcontents(item.find("rank"), 0), getcontents(item.find("manufacturer"), 0), \
       getcontents(item.find("height"), 0), getcontents(item.find("length"), 0), getcontents(item.find("width"), 0), getcontents(item.find("weight"), 0), \
       getcontents(item.find("producttypename"), 0), getcontents(item.find("publisher"), 0), getcontents(item.find("studio"), 0), countory, \
       getcontents(item.find("detailpageurl"), 0),yymmdd,hhmmss)

c.execute(sql, val)

conn.commit()

print(sql,val)

conn.close()



'''
print(soup.find("detailpageurl").contents[0])
#print(soup.find("totalpages").contents[0])#ないときもある
print(soup.find("asin").contents[0])
print(soup.find("ean").contents[0])#similalyでないときもある
print(soup.find("eanlistelement").contents[0])
#print(soup.find("edition").contents[0])
#print(soup.find("isbn").contents[0])
print(soup.find("manufacturer").contents[0])
print(soup.find('height').contents[0])
print(soup.find('length').contents[0])
print(soup.find('width').contents[0])
print(soup.find('weight').contents[0])
print(soup.find("productgroup").contents[0])
print(soup.find("producttypename").contents[0])
print(soup.find("publisher").contents[0])
print(soup.find("studio").contents[0])
print(soup.find("title").contents[0])
print(retcontents(soup,"asin"))
'''


#from see import  see
#print(see(amazon))
#print(see(BeautifulSoup))
