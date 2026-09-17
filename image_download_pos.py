import os
import re
import time
from images.file_check import check
import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup

img_name = 'Pore coral(孔珊瑚屬 屬 Porites)_'
url = 'https://www.inaturalist.org/taxa/47530-Porites/browse_photos'

local_path = './images/珊瑚(俗名)/Pore coral'  # 圖片儲存路徑
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
xpath = '//div[contains(@class,"TaxonPhoto")]/div[contains(@class,"CoverImage")]'

# 紀錄下載過的圖片網址，避免重複下載  
img_url_dic = {}  
pos = 0

for i in range(1000):
    elements = driver.find_elements(By.XPATH, xpath)
    print(f"找到 {len(elements)} 个元素")

    for element in elements:
        try:
            # 获取style属性
            style = element.get_attribute('style')
            
            # 从style中提取URL
            if style and 'background-image' in style:
                # 使用正则表达式提取URL
                match = re.search(r'url\("([^"]+)"\)', style)
                if match:
                    img_url = match.group(1)
                    
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

    pos += i*1000 
    js = "document.documentElement.scrollTop=%d" % pos  
    driver.execute_script(js)  
    time.sleep(3)

print("url:, ", driver.current_url)
driver.close()
print('下載完畢!')
