import os
import requests
import urllib
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import time
import threading

img_name = 'Clownfish Coral'
url = 'https://www.google.com.tw/search?q='+img_name+'&tbm=isch'

resp = requests.get(url)
soup = BeautifulSoup(resp.text, 'lxml')
with open('a.html', 'w', encoding='utf-8') as f:   # w 寫入, a 附加, r 讀取
    f.write(soup.prettify())   # 解析網頁內容

local_path = './images'  # 圖片儲存路徑
if not os.path.exists(local_path):
    os.makedirs(local_path)  # 建立資料夾

# 目標元素的xpath
xpath = '//div[@jsname="qQjpJ"]/h3/a/div/div/div/g-img/img' #隨時需要更新
# 啟動chrome瀏覽器
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
  
# 最大化窗口，因為每一次爬取只能看到視窗内的圖片  
driver.maximize_window()  
  
# 紀錄下載過的圖片網址，避免重複下載  
img_url_dic = {}  
  
# 瀏覽器打開爬取頁面
driver.get(url)  
  
# 模擬滾動視窗瀏覽更多圖片
pos = 0  
m = 0 # 圖片編號 
for i in range(100):  
    pos += i*500 # 每次下滾500  
    js = "document.documentElement.scrollTop=%d" % pos  
    driver.execute_script(js)  
    time.sleep(3)
    for element in driver.find_elements(By.XPATH, xpath):
        try:
            img_url = element.get_attribute('src')
            
            # 保存圖片到指定路徑
            if img_url != None and not img_url in img_url_dic:
                img_url_dic[img_url] = ''  
                m += 1
                # print(img_url)
                ext = img_url.split('/')[-1]
                # print(ext)
                filename = str(m) + 'Clownfish&Coral'+'.jpg'
                print(filename)
                stop = m
                while(os.path.exists(local_path + '/' + filename)):
                    if stop + 1000 < m:
                        break
                    m += 1
                # 保存圖片
                urllib.request.urlretrieve(img_url, os.path.join(local_path , filename))
                
        except OSError:
            print('發生OSError!')
            print(pos)
            break
            
driver.close()