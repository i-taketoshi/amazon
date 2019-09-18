# coding: utf-8

import urllib.parse
import urllib.request

import xml.etree.ElementTree as ET

import hmac
import time
from bs4 import BeautifulSoup

from hashlib import sha256
from base64 import b64encode

import requests

import sqlite3
import datetime
import random
#https://github.com/czpython/python-amazon-mws

MARKETPLACES = {
    "CA" : ("https://mws.amazonservices.ca", "A2EUQ1WTGCTBG2"),
    "US" : ("https://mws.amazonservices.com", "ATVPDKIKX0DER"), 
    "DE" : ("https://mws-eu.amazonservices.com", "A1PA6795UKMFR9"),
    "ES" : ("https://mws-eu.amazonservices.com", "A1RKKUPIHCS9HS"),
    "FR" : ("https://mws-eu.amazonservices.com", "A13V1IB3VIYZZH"),
    "IN" : ("https://mws.amazonservices.in", "A21TJRUUN4KGV"),
    "IT" : ("https://mws-eu.amazonservices.com", "APJ6JRA9NG5V4"),
    "UK" : ("https://mws-eu.amazonservices.com", "A1F83G8C2ARO7P"),
    "JP" : ("https://mws.amazonservices.jp", "A1VC38T7YXB528"),
    "CN" : ("https://mws.amazonservices.com.cn", "AAHKV2X7AFYLW"),
    "MX" : ("https://mws.amazonservices.com.mx", "A1AM78C64UM0Y8")
}


class MWSError(Exception):
    pass

# ベースクラス
class BaseObject(object):

    URI = "/"
    VERSION = "2009-01-01"
    NS = ''
    

    def __init__(self, AWSAccessKeyId=None, AWSSecretAccessKey=None,
            SellerId=None, Region='US', Version="", domain='', uri="", MWSAuthToken=""):

        self.AWSAccessKeyId     = AWSAccessKeyId
        self.AWSSecretAccessKey = AWSSecretAccessKey
        self.SellerId = SellerId
        self.Region   = Region
        self.Version  = Version or self.VERSION
        self.uri = uri or self.URI
        self.dbname = r'D:\workspace\sqlite\sample.sqlite3'    

        if Region in MARKETPLACES:
            self.service_domain = MARKETPLACES[self.Region][0]
        else:
            raise MWSError("Incorrrect region supplied {region}".format(**{"region": Region}))
        
        if domain:
            self.domain = domain
        elif Region in MARKETPLACES:
            self.domain = MARKETPLACES[Region][1]

    def r(self, item, tag):
        if item.find(tag) is None:
            return "None"
        else:
            return item.find(tag).text
        
    # APIを叩く
    def request(self, method="POST", **kwargs):
        params = {
            "AWSAccessKeyId": self.AWSAccessKeyId,
            "SellerId": self.SellerId,
            "SignatureVersion": 2,
            "Timestamp": self.timestamp,
            "Version": self.Version,
            "SignatureMethod": "HmacSHA256"
        }
       
        params.update(kwargs)
        
        signature, query_string = self.signature(method, params)
        
        

        url = 'https://{}{}?{}&Signature={}'.format(self.service_domain.replace("https://", ""), self.uri, query_string, signature)
        #print(url)
        #print("#############################")
        r = requests.post(url)
        #print("#############################")
        #print(r.content.decode())
        #print(url)
        return r.content.decode()
    
    def signature(self, method, params):
        
        #ソートして＆で結合
        query_string = self.quote_query(params)
        #print(params)
        
        #署名対象文字作成
        #こんな感じにする
        #POST
        #mws.amazonservices.jp
        #/Orders/2013-09-01
        #AWSAccessKeyId＝....&.....&....
        canonical = method + "\n" + self.service_domain.replace("https://", "") + "\n" + self.uri  + "\n" + query_string
                                                          
        if type(self.AWSSecretAccessKey) is str:
            self.AWSSecretAccessKey = self.AWSSecretAccessKey.encode('utf-8')

        if type(canonical) is str:
            canonical = canonical.encode('utf-8')

        digest = hmac.new(self.AWSSecretAccessKey, canonical, sha256).digest()
        return (urllib.parse.quote(b64encode(digest)), query_string)

    @staticmethod
    def quote_query(query):
        return "&".join("%s=%s" % (
            k, urllib.parse.quote(
                str(query[k]).encode('utf-8'), safe='-_.~'))
                for k in sorted(query))

    @property
    def timestamp(self):
        return time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    
    def enumerate_param(self, param, values):
        """
            Builds a dictionary of an enumerated parameter.
            Takes any iterable and returns a dictionary.
            ie.
            enumerate_param('MarketplaceIdList.Id', (123, 345, 4343))
            returns
            {
                MarketplaceIdList.Id.1: 123,
                MarketplaceIdList.Id.2: 345,
                MarketplaceIdList.Id.3: 4343
            }
        """
        params = {}
        if values is not None:
            if not param.endswith('.'):
                param = "%s." % param
            for num, value in enumerate(values):
                params['%s%d' % (param, (num + 1))] = value
        return params
        
    def enumerate_param2(self, marketplaceid, values1, values2):
        """
            Builds a dictionary of an enumerated parameter.
            Takes any iterable and returns a dictionary.
            ie.
            enumerate_param('MarketplaceIdList.Id', (123, 345, 4343))
            returns
            {
                MarketplaceIdList.Id.1: 123,
                MarketplaceIdList.Id.2: 345,
                MarketplaceIdList.Id.3: 4343
            }
        """

        params = {}
        if values1 is not None:
            
            for num, value in enumerate(values1):

                params.update({'FeesEstimateRequestList.FeesEstimateRequest.' + str(num + 1) + '.MarketplaceId':marketplaceid})
                params.update({'FeesEstimateRequestList.FeesEstimateRequest.' + str(num + 1) + '.IdType':'ASIN'})
                params.update({'FeesEstimateRequestList.FeesEstimateRequest.' + str(num + 1) + '.IdValue':value})
                params.update({'FeesEstimateRequestList.FeesEstimateRequest.' + str(num + 1) + '.IsAmazonFulfilled':'true'})
                params.update({'FeesEstimateRequestList.FeesEstimateRequest.' + str(num + 1) + '.Identifier':num + 1})
                params.update({'FeesEstimateRequestList.FeesEstimateRequest.' + str(num + 1) + '.PriceToEstimateFees.ListingPrice.Amount':values2[num]})
                params.update({'FeesEstimateRequestList.FeesEstimateRequest.' + str(num + 1) + '.PriceToEstimateFees.ListingPrice.CurrencyCode':'JPY'})
        return params


class Products(BaseObject):
    """ Amazon MWS Products API """

    URI = '/Products/2011-10-01'
    VERSION = '2011-10-01'
    NS = '{http://mws.amazonservices.com/schema/Products/2011-10-01}'
    
    def get_myfees_estimate_one(self, marketplaceid, asin, price):
        """ Returns a list of products and their attributes, based on a list of
            ASIN values that you specify.
        """
        data = dict(Action='GetMyFeesEstimate')
        data.update({'FeesEstimateRequestList.FeesEstimateRequest.1.MarketplaceId':marketplaceid})
        data.update({'FeesEstimateRequestList.FeesEstimateRequest.1.IdType':'ASIN'})
        data.update({'FeesEstimateRequestList.FeesEstimateRequest.1.IdValue':asin})
        data.update({'FeesEstimateRequestList.FeesEstimateRequest.1.IsAmazonFulfilled':'true'})
        data.update({'FeesEstimateRequestList.FeesEstimateRequest.1.Identifier':'1'})
        data.update({'FeesEstimateRequestList.FeesEstimateRequest.1.PriceToEstimateFees.ListingPrice.Amount':price})
        data.update({'FeesEstimateRequestList.FeesEstimateRequest.1.PriceToEstimateFees.ListingPrice.CurrencyCode':'JPY'})
        
        return self.request(**data)

    def get_myfees_estimate_test(self, marketplaceid, asins, prices):
        #data = dict(Action=)
        params = {
            "AWSAccessKeyId": self.AWSAccessKeyId,
            "Action": 'GetMyFeesEstimate'
        }
        params.update(self.enumerate_param2(marketplaceid, asins, prices))
        params.update({
            "SellerId": self.SellerId,
            "SignatureMethod": "HmacSHA256",
            "SignatureVersion": 2,
            "Timestamp": self.timestamp,
            "Version": self.Version
        })
        
        query =  "&".join("%s=%s" % (
            k, urllib.parse.quote(
                str(params[k]).encode('utf-8'), safe='-_.~'))
                for k in params)
        #print(query)
        canonical = "POST" + "\n" + self.service_domain.replace("https://", "") + "\n" + self.uri  + "\n" + query
                                                          
        if type(self.AWSSecretAccessKey) is str:
            self.AWSSecretAccessKey = self.AWSSecretAccessKey.encode('utf-8')

        if type(canonical) is str:
            canonical = canonical.encode('utf-8')

        digest = hmac.new(self.AWSSecretAccessKey, canonical, sha256).digest()
        signature = urllib.parse.quote(b64encode(digest))
        posturl = {
            "AWSAccessKeyId": self.AWSAccessKeyId,
            "Action": 'GetMyFeesEstimate',
            "SellerId": self.SellerId,
            "SignatureVersion": 2,
            "Timestamp": self.timestamp,
            "Version": self.Version,
            "Signature": signature,
            "SignatureMethod": "HmacSHA256",
        }
        before =  "&".join("%s=%s" % (
            k, urllib.parse.quote(
                str(posturl[k]).encode('utf-8'), safe='-_.~'))
                for k in posturl)
        
        tmp = self.enumerate_param2(marketplaceid, asins, prices)
        after =  "&".join("%s=%s" % (
            k, urllib.parse.quote(
                str(tmp[k]).encode('utf-8'), safe='-_.~'))
                for k in tmp)
        url = 'https://mws.amazonservices.jp/Products/2011-10-01?{}&{}'.format(before, after)
        #url = 'https://{}{}?{}&Signature={}'.format(self.service_domain.replace("https://", ""), self.uri, query, signature)
        #print(url)
        r = requests.post(url)
        return r.content.decode()
        
 
    
    def get_myfees_estimate(self, marketplaceid, asins, price):
        """ Returns a list of products and their attributes, based on a list of
            ASIN values that you specify.
        """
        data = dict(Action='GetMyFeesEstimate')
        
        data.update(self.enumerate_param2(marketplaceid, asins, price))
        
        return self.request(**data)



    def get_matching_product(self, marketplaceid, asins):
        """ Returns a list of products and their attributes, based on a list of
            ASIN values that you specify.
        """
        data = dict(Action='GetMatchingProduct', MarketplaceId=marketplaceid)
        data.update(self.enumerate_param('ASINList.ASIN.', asins))
        return self.request(**data)
    
    def get_matching_product_forid(self, marketplaceid, asins):
        """ Returns a list of products and their attributes, based on a list of
            ASIN values that you specify.
        """
        data = dict(Action='GetMatchingProductForId', MarketplaceId=marketplaceid, IdType='ASIN')
        data.update(self.enumerate_param('IdList.Id.', asins))
        return self.request(**data)
    
    
    def list_matching_products(self, marketplaceid, query, contextid=None):
        """ Returns a list of products and their attributes, ordered by
            relevancy, based on a search query that you specify.
            Your search query can be a phrase that describes the product
            or it can be a product identifier such as a UPC, EAN, ISBN, or JAN.
        """
        data = dict(Action='ListMatchingProducts',
                    MarketplaceId=marketplaceid,
                    Query=query,
                    QueryContextId=contextid)
        return self.request(**data)

    def get_competitive_pricing_for_asin(self, marketplaceid, asins):
        """ Returns the current competitive pricing of a product,
            based on the ASIN and MarketplaceId that you specify.
        """
        data = dict(Action='GetCompetitivePricingForASIN', MarketplaceId=marketplaceid)
        data.update(self.enumerate_param('ASINList.ASIN.', asins))
        return self.request(**data)

    def get_competitive_pricing_for_asin_test(self, marketplaceid, asins):
        """ Returns the current competitive pricing of a product,
            based on the ASIN and MarketplaceId that you specify.
            This is test
        """
        data = dict(Action='GetCompetitivePricingForASIN', MarketplaceId=marketplaceid)
        data.update(self.enumerate_param('ASINList.ASIN.', asins))
        return data

    def put_searchflag(self, word):
         #DB接続
        conn = sqlite3.connect(self.dbname)
        c = conn.cursor()
        #検索済みにチェックをする
        updateg = "update amazonranking set do = 1 where trend = '" + word + "'";                                                                                                                   
        c.execute(updateg)
        
        updateg = "update google set do = 1 where trend = '" + word + "'"; 
        c.execute(updateg)
        
        conn.commit()
        conn.close()
        
    def get_searchwords(self, yymmdd, searchnum):
        
         #DB接続
        conn = sqlite3.connect(self.dbname)
        c = conn.cursor()
        
        
        #todaydetail  =    datetime.datetime.today()
        #yymmdd = todaydetail.strftime("%Y-%m-%d")
        #hhmmss = todaydetail.strftime("%H:%M:%S")
        
        
        #アマゾンテーブルから検索用のワードを検索する                            
        sql = u"select * from amazonranking where yymmdd = '" + yymmdd + "' and do is NULL"
        c.execute(sql)
        amazonranking = c.fetchall()
        
        #グーグルテーブルから検索用のワードを検索する
        sqlg = u"select * from google where yymmdd = '" + yymmdd + "' and do is NULL"
        c.execute(sqlg)
        google = c.fetchall()
        
        if len(amazonranking) == 0 and len(google) == 0:
            return 0
            
            
        #検索用のワードのみを取得
        googletrend = []
        for row in google:
            googletrend.append(row[1])
            
        if searchnum != 'All':
            #ランダムでアマゾンランキングを抽出
            index = random.sample(range(1, len(amazonranking)), searchnum)
            SearchWords = [amazonranking[i][1] for i in index]
        else:
            #全アマゾンランキング
            SearchWords = [amazonranking[i][1] for i in range(len(amazonranking))]
        
        conn.commit()
        conn.close()
        
        
        #Googleトレンドとアマゾンランキングを結合
        for g in googletrend:
            SearchWords.append(g)

        return SearchWords
    


if __name__ == "__main__":

    
    
    
    SellerID           = "A2ILL9FJMGGGDJ"
    AWSAccesKeyId      = "AKIAIA4ALUSZTLIJU2IQ"
    AWSSecretAccessKey = "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"
    
    product = Products(
        AWSAccessKeyId=AWSAccesKeyId,
        AWSSecretAccessKey=AWSSecretAccessKey,
        SellerId=SellerID,
        Region='JP')
    MarketplaceId      = product.domain#A1VC38T7YXB528

    asins = ["B077G5RNMZ", "B078HGG68W"]
    #response = product.get_matching_product(MarketplaceId,asins)
    
    response = product.get_matching_product_forid(MarketplaceId, asins)
    soup = BeautifulSoup(response,"lxml")
    #print(soup.prettify())
    
    #print(soup.findAll("getcompetitivepricingforasinresult"))
    for p in soup.findAll("getcompetitivepricingforasinresult"):
        print(p.find("asin"))
        print(p.find("landedprice").find("amount"))
        print(p.find("shipping").find("amount"))
        print(p.find("rank"))
        print("###")
        
          
    '''
    #####
    response = product.list_matching_products(MarketplaceId, "ベイブレード", "All")
    
    soup = BeautifulSoup(response,"lxml")
    #print(soup.prettify())
    
    for p in soup.findAll("product"):
        print(p.find("asin").text)
        print(p.find("rank").text)
        
        print(p.find("ns2:title").text)
        print(p.find("ns2:productgroup").text)
        #print(p.find("ns2:brand").text)
        
        print(product.r(p, "ns2:brand"))
        #if p.find("ns2:brand") is None: 
        #    print("NOne")
        
        
        
        print("################")
        
      ####  
    '''
    
    #ListMatchingProducts
    #GetCompetitivePricingForASIN
    
'''QueryCOntextId
All
Apparel
Automotive
Baby
Beauty
Books
Classical
DVD
Electronics
ForeignBooks
Grocery
HealthPersonalCare
Hobbies
HomeImprovement
Jewelry
Kitchen
MP3Downloads
Music
MusicalInstruments
MusicTracks
OfficeProducts
Shoes
Software
SportingGoods
Toys
VHS
Video
VideoGames
Watches

'''