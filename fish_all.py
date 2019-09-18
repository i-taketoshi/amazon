from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.chrome.options import Options
import time
import re

import pandas as pd
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import requests


path = r'D:\workspace\amazon\chromedriver.exe'

options = Options()
options.add_argument("--disable-extentions")
options.add_argument("--ignore-certificate-errors")
#options.add_argument("--headless")

driver = webdriver.Chrome(path, chrome_options=options)
driver.implicitly_wait(10) # seconds

def remove_whitespace(str):
    return ''.join(str.split())

condition_flag = 0
choka_flag = 0
timesleepsec = 10

#driver.get("https://ameblo.jp/tfa-fish/entry-12419724582.html")
#2014-10-18 07:21:19
driver.get("https://ameblo.jp/tfa-fish/entry-11940543060.html")

soup = BeautifulSoup(driver.page_source, "lxml")
previousPage = soup.find("a", class_="previousPage")

while previousPage is not None:

    soup = BeautifulSoup(driver.page_source, "lxml")
    previousPage = soup.find("a", class_="previousPage")
    
    ### 本文取得
    status_text = remove_whitespace(soup.find(id="entryBody").text)
    theme = soup.find("span", class_="theme").text


    pattern = '釣果速報'
    result = re.search(pattern, theme)
    if result: #none以外の場合
        choka_flag = 1
    else:
        pattern = 'コンディション'
        result = re.search(pattern, theme)
        if result: #none以外の場合
            condition_flag = 1

    
    if condition_flag == 1:
        lists = []#初期化、タイトル、日付、天気、水温等をを入れる

        title = soup.find("h3", class_="title").text.strip()
        yymmdd = soup.find(class_="date").text.strip()
        print(title)

        lists = [yymmdd,title]

        pattern = u'本日の営業時間[：:](.{1,12})天気'
        result = re.search(pattern, status_text)
        if result: #none以外の場合
            tmp = result.group(1)
        else:
            tmp = ""
        
        lists.append(tmp)

        pattern = '天気[：:](.{1,5})気温'
        result = re.search(pattern, status_text)
        if result: #none以外の場合
            tmp = result.group(1)
        else:
            tmp = ""
        lists.append(tmp)

        pattern = u'気温[：:](.{1,5})[度|℃]'
        result = re.search(pattern, status_text)
        if result: #none以外の場合
            tmp = result.group(1)
        else:
            tmp = ""
        lists.append(tmp)

        pattern = u'混雑度.*(\d{1,2})[名|人]'
        result = re.search(pattern, status_text)
        if result: #none以外の場合
            tmp = result.group(1)
        else:
            tmp = ""
        lists.append(tmp)

        pattern = u'アマゾンエリア.{1,5}(.{3,4})[度|℃]'
        result = re.search(pattern, status_text)
        if result: #none以外の場合
            tmp = result.group(1)
        else:
            tmp = ""
        lists.append(tmp)

        pattern = u'ナイアガラエリア.{1,5}(.{3,4})[度|℃]'
        result = re.search(pattern, status_text)
        if result: #none以外の場合
            tmp = result.group(1)
        else:
            tmp = ""
        lists.append(tmp)

        pattern = u'ミシガンエリア.{1,5}(.{3,4})[度|℃]'
        result = re.search(pattern, status_text)
        if result: #none以外の場合
            tmp = result.group(1)
        else:
            tmp = ""
        lists.append(tmp)

        pattern = u'左[:：](...)'
        if result: #none以外の場合
            tmp = result.group(1)
        else:
            tmp = ""
        lists.append(tmp)

        pattern = u'右[:：](...)'
        result = re.search(pattern, status_text)
        if result: #none以外の場合
            tmp = result.group(1)
        else:
            tmp = ""
        lists.append(tmp)

        pattern = u'本日は放流|本日放流|放流時間'
        result = re.search(pattern, status_text)
        if result: #none以外の場合
            tmp = "放流日"
        else:
            tmp = ""
        lists.append(tmp)

        condition_flag = 0


    if choka_flag == 1:

        #####   
        pattern = '(ヒットフライ|ヒットルアー|使用ルアー|使用フライ)+(は、|、|:|：)?(.*?)(でした|です)?(。|!|！)'
        result = re.findall(pattern, status_text)
        
        list_all = []
        if result:
            for r in result:
                list_tmp_add = []#初期化、使用ルアーを入れる
                list_tmp_add.extend(lists)
                list_tmp_add.append(r[0])
                list_tmp_add.append(r[2])

                list_all.append(list_tmp_add)
            
        
        # データフレームを作成
        df = pd.DataFrame(list_all)

        # CSV ファイル (employee.csv) として出力
        # df.to_csv("employee.csv", index=False, encoding="utf-8", mode='a')
        # CSV ファイル (employee.csv) に追記
        #df.to_csv(r'X:\Users\0003221\Desktop\choka.csv', index=False, encoding="utf-8", mode='a', header=False)
        df.to_csv(r'C:\Users\taketoshi\Desktop\choka.csv', index=False, encoding="utf-8", mode='a', header=False)
        print("書き込みOK")

        choka_flag = 0
        condition_flag = 0
        list_all = []

    #driver.find_element_by_xpath("//a[@class='previousPage _2-eNSDjM']").click()

    #aタグのリンク先の取得
    link = previousPage.attrs['href']
    print(link)
    time.sleep(timesleepsec)
    driver.get("https://ameblo.jp/" + link)
    
driver.quit()
print("end")