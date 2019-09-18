# -*- coding: utf-8 -*-
"""
Created on Mon Jun 12 01:03:12 2017
@author: taketoshi
デイリー急上昇ワード or 最新急上昇ワード
"""

# coding: UTF-8
try:
    import urllib2
except ImportError:
    import urllib.request as urllib2
    
from bs4 import BeautifulSoup
import datetime
import sqlite3



class Scryping:
    """A simple example class"""         # 三重クォートによるコメント

    def __init__(self, ):                  # コンストラクタ
        self.url = ""

    def getBurstRanking(self):                   # getName()メソッド
        #url = "https://searchranking.yahoo.co.jp/burst_ranking/"
        #url = "https://searchranking.yahoo.co.jp/rt_burst_ranking/"
        
        # URLにアクセスする htmlが帰ってくる → <html><head><title>経済、株価、ビジネス、政治のニュース:日経電子版</title></head><body....
        html = urllib2.urlopen(self.url)
        
        # htmlをBeautifulSoupで扱う
        soup = BeautifulSoup(html, "html.parser")
        
        elms = soup.find('div', {'class': 'listRowlink'})
        links = elms.find_all('a')
        
        SearchWords = []
        for link in links:
            
            #２ワード以上から成る単語を分解
            words = link.contents[0].split(" ")
            for word in words:
                #print(word)
                SearchWords.append(word)
            
            #複数ワードを分割しない
            if len(words) != 1:
                #print(link.contents[0])
                SearchWords.append(link.contents[0])
        
        #print(SearchWords)
        return SearchWords
        
    def getTweet(self):
        #url = "https://searchranking.yahoo.co.jp/realtime_buzz/"

        # URLにアクセスする htmlが帰ってくる → <html><head><title>経済、株価、ビジネス、政治のニュース:日経電子版</title></head><body....
        html = urllib2.urlopen(self.url)
        
        # htmlをBeautifulSoupで扱う
        soup = BeautifulSoup(html, "html.parser")
        
        elms = soup.find('div', {'class': 'listRowlink'})
        h3s = elms.find_all('h3')
        
        SearchWords = []
        for h3 in h3s:
            a = h3.find('a')
            SearchWords.append(a.contents[0])
            #print(a.contents[0])
        #print(SearchWords)
        return SearchWords
            
    def setURL(self, url):             # setName()メソッド
        self.url = url
    
    def getSearchWords(self):
        self.SearchWords = [
            "日本未発売","海外","USA","米国",
            "英国","世界限定","限定","希少",
            "コラボ ","limited edition","着用モデル","廃盤",
            "廃番","国内発送","即納","並行輸入","import",
            "輸入","インポート","北米","アメリカ",
            "並行輸入　ランキング","並行輸入　おもちゃ"
        ]
        
        #print(self.SearchWords)
        return self.SearchWords
        

if __name__ == "__main__":
    
    # URLにアクセスする htmlが帰ってくる → <html><head><title>経済、株価、ビジネス、政治のニュース:日経電子版</title></head><body....


    '''
    ### amajanからASINとJANコードとランキングを取得する####
    #### start
        url = 'http://www.hikaku123.info/amajan/?asin=B074P457BC&amd=off'
        res = urllib2.urlopen(url)
        
        soup = BeautifulSoup(res,"lxml")
        
        
        asintag = soup.find_all("b", text=re.compile("ASIN"))
        
        jantag = soup.find_all("b", text=re.compile("JAN"))
        
        ranktag = soup.find_all("b", text=re.compile("Amazon ランキング"))
        
        a_re = re.search(r":(\w+)",asintag[0].text)
        j_re = re.search(r":(\w+)",jantag[0].text)
        r_re = re.search(r":(\w+)",ranktag[0].text)
        
        if a_re:
            print("ASIN:" + a_re.group(1))
        if j_re:
            print("jan:" + j_re.group(1))
        if r_re:
            print("rank:" + r_re.group(1))
    
    ### end
    '''
    
    '''
    prettify = soup.prettify()    
    f = open(r'D:\workspace\aaa.txt','wb')
    f.write(prettify.encode('utf-8'))
    f.close()
    '''

    
    
    dbname = r'D:\workspace\sqlite\sample.sqlite3'

    todaydetail  =    datetime.datetime.today()
    yymmdd = todaydetail.strftime("%Y-%m-%d")
    
    #DBに登録
    conn = sqlite3.connect(dbname)
    c = conn.cursor()
    sql = 'insert into yahootrend(trend, category, yymmdd) values (?,?,?)'
    
    # デイリーランキング - 急上昇ワード
    #前日に比べて検索数が急増したワードのランキング
    url = "https://searchranking.yahoo.co.jp/burst_ranking/"
    a = Scryping()
    a.setURL(url)
    words = a.getBurstRanking()
    
    for w in words:
        v = (w.strip("とは"), "burst_ranking",yymmdd)
        c.execute(sql, v)
    

    #最新 - 急上昇ワード
    #検索数が急増しているワードを紹介
    #1時間更新
    url = "https://searchranking.yahoo.co.jp/rt_burst_ranking/"
    a.setURL(url)
    words = a.getBurstRanking()
    for w in words:
        v = (w.strip("とは"), "rt_burst_ranking",yymmdd)
        c.execute(sql, v)
        

    
    
    #最新 - つぶやき
    #リアルタイム検索で話題のワードを紹介
    url = "https://searchranking.yahoo.co.jp/realtime_buzz/"
    a.setURL(url)
    words = a.getTweet()
    for w in words:
        v = (w.strip("とは"), "realtime_buzz",yymmdd)
        c.execute(sql, v)

    
    
conn.commit()
conn.close()

    #a = Scryping()
    #words = a.getSearchWords()
    #print(words)
    