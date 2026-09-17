import os
import time
from images.file_check import check
import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.action_chains import ActionChains
from bs4 import BeautifulSoup

img_name = '雙帶小丑'
url = 'https://www.flickr.com/photos/65547243@N00/4148939271/in/photolist-7jCp6H-88SLJY-6deffX-bT5MgK-8CRovL-SH4e3q-77Y7KY-21Q7FXb-S9GjsA-88j4HV-cEsifW-2qeXNQR-2jCFKjR-6XRSzj-6T4wmC-dpR12z-88j5z4-8CRovE-6q2bgM-arbRWR-dBCmcC-2nRwpvn-Ds5za-gBmopq-RtFVKr-25Dn2Ag-4J5Z6M-npqk83-7jCu7a-7jCrjT-2ozqUv9-9TtxBf-dBxRpH-ZiqdLu-43ZeZ1-5jnJQb-kgbj7K-2k2E8wS-LfcYCD-siUrcn-6defaF-2owL7X5-5jirCg-a7wMC3-dBCmhU-25DqiKe-2joXXUS-7zht2-dGpgRb-67Wbdn'

local_path = './images/小丑魚/Amphiprion clarkii 雙帶小丑'  # 圖片儲存路徑
checkfile = check(local_path)  
used_numbers, max_number, missing_numbers = checkfile.analyze_files(img_name)

resp = requests.get(url)
soup = BeautifulSoup(resp.text, 'lxml')
with open('a.html', 'w', encoding='utf-8') as f:   # w 寫入, a 附加, r 讀取
    f.write(soup.prettify())   # 解析網頁內容

# 啟動chrome瀏覽器
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
driver.get(url)  

# 目標元素的xpath
#xpath = '//div[contains(@class,"lZNFLShGN1hv5ECLYH1E")]/article/a/figure/picture/img'
#button_xpath = '//a[contains(@data-testid,"pagination-button-next")]'
xpath = '//div[contains(@class,"view photo-well-media-scrappy-view")]/img'
button_xpath = '//a[contains(@class,"navigate-next")]/span'

# 紀錄下載過的圖片網址，避免重複下載  
img_url_dic = {}  
  

for i in range(1000):
    elements = driver.find_elements(By.XPATH, xpath)
    #print(f"找到 {len(elements)} 个元素")
    for element in elements:
        try:
            img_url = element.get_attribute('src')
            # 保存圖片到指定路徑
            if img_url and img_url not in img_url_dic:
                img_url_dic[img_url] = ''
                
                # 取得下一個可用的檔名和編號
                filename, file_num = checkfile.get_next_filename(used_numbers, missing_numbers, img_name)
                filepath = os.path.join(local_path, filename)
                
                print(f"下載圖片: {img_url}")
                print(f"儲存在: {filepath}")
                print(f"存為: {filename}")
                
                if checkfile.download_image(img_url, filepath):
                    print(f"✓ 成功下載: {filename}")
                else:
                    print(f"✗ 下載失敗: {filename}")
                    # 如果下載失敗，將編號放回缺失列表
                    file_num = int(file_num) if isinstance(file_num, str) else file_num
                    used_numbers.remove(file_num)
                    missing_numbers.append(file_num)
                    missing_numbers.sort()
                
        except Exception as e:
            print(f"处理元素时出错: {e}")

    next_button = driver.find_element(By.XPATH, button_xpath)
    actions = ActionChains(driver)
    actions.click(next_button).perform()
    time.sleep(2)

print("url:, ", driver.current_url)
driver.close()
print('下載完畢!')
