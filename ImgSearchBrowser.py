#https://www.amazon.co.jp/gp/top-sellers/hobby/ref=crw_ratp_ts_hobby
#####
#HeadlessChromeを使用し、アマゾンランキングを取得し、
#ASINのみを出力する
#####


from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.chrome.options import Options
import time
import re


options = Options()
options.add_argument("--disable-extentions")
options.add_argument("--ignore-certificate-errors")
#options.add_argument("--headless")

'''
driver = webdriver.Chrome(chrome_options=options)

driver.get("https://www.google.co.jp/imghp?hl=ja")
#driver.get("https://www.google.co.jp/")
time.sleep(2)  # 2秒まってみる

imgaddress = 'https://images-na.ssl-images-amazon.com/images/I/61Z0fYmetYL._SX425_.jpg'

#カメラマーククリック
driver.find_element_by_id("qbi").click()
time.sleep(1)
#検索ワード入力
driver.find_element_by_id("qbui").send_keys(imgaddress)
time.sleep(1)
#検索実行
driver.find_element_by_id("qbbtc").click()
time.sleep(3)
#検索結果を表示させる
driver.find_element_by_id("Z6bGOb").click()
time.sleep(5)


data = driver.page_source
soup = BeautifulSoup(data,"lxml")
prettify = soup.prettify()
'''
data = open(r'X:\Users\0003221\Desktop\testtest.txt','rb')
soup = BeautifulSoup(data,"lxml")
#print(soup.prettify())

#result = soup.find_all("div",attr={'jsname':'ik8THc'})
result = soup.find_all("div", attrs={"jsname": "ik8THc"})




print('###########')
for res in result:
    pattern = "https://www.amazon.com/.+/dp/[a-zA-Z0-9_]{10}"
    text = res.string
    matchOB = re.search(pattern , text)
    if matchOB:
        print(matchOB.group(0))
        break


#テキストへHTML情報書き込み
#f = open(r'X:\Users\0003221\Desktop\testtest.txt','wb')
#f.write(soup.prettify().encode('utf-8'))
#f.close()
#driver.quit()
