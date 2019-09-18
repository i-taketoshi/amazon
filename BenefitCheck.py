# -*- coding: utf-8 -*-
"""
Created on Sun Feb  4 15:51:49 2018

@author: taketoshi


エクセルに入力されているASINを元に詳細商品情報を入力する
testpandsの後に実行する

"""
import sys
import time
from bs4 import BeautifulSoup

import openpyxl as px
from pprint import pprint
from copy import copy
import mwstestClass

def get_price_jp(p):
    if p.find("landedprice") is None:
        return "None"
    else:
        return p.find("landedprice").find("amount").string
def isNone(p,whl):
    try:
        
        if p.find("ns2:packagedimensions").find(whl) is None:
            if p.find("ns2:itemdimensions").find(whl) is None:
                return 0
            else:
                return p.find("ns2:itemdimensions").find(whl).string
            
        else:
            return p.find("ns2:packagedimensions").find(whl).string
    except:
        return 0
            
        

def chunked(iterable, n):
    return [iterable[x:x + n] for x in range(0, len(iterable), n)]


    
start = time.time()


  
Filename = r'D:\workspace\モノレート\test.xlsm'


# ブックを開く
wb = px.load_workbook(Filename, read_only=False, keep_vba=True, data_only=True)
#シートを固定
ws = wb["diff"]
#最終行取得
max_row = 12
ws.cell(row = 5, column = 1).value = '=A2*3'

wb.save(Filename)        

elapsed_time = time.time() - start
print ("elapsed_time:{0}".format(elapsed_time) + "[sec]")
    
