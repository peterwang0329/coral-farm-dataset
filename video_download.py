import os
import time
import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import NoSuchElementException
from bs4 import BeautifulSoup

video_name = 'Clownfish Coral'
url = 'https://www.pexels.com/zh-tw/search/videos/%E5%B0%8F%E4%B8%91%E9%AD%9A/'

resp = requests.get(url)
soup = BeautifulSoup(resp.text, 'lxml')
with open('a.html', 'w', encoding='utf-8') as f:   # w 寫入, a 附加, r 讀取
    f.write(soup.prettify())   # 解析網頁內容

local_path = './videos'  # 影片儲存路徑
if not os.path.exists(local_path):
    os.makedirs(local_path)

# 设置Chrome选项
options = webdriver.ChromeOptions()
options.add_argument('--disable-blink-features=AutomationControlled')
options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36')

# 啟動chrome瀏覽器
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
driver.get(url)  

# 目標元素的xpath
xpath = '//div[@class="BreakpointGrid_item__RSMyf"]/article/a/video'
  
# 紀錄下載過的影片網址，避免重複下載  
video_url_dic = {}  
m = 0 # 影片編號 

def download_video(url, filename):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36',
        'Referer': 'https://www.pexels.com/',
        'Accept': 'video/webm,video/mp4,video/*;q=0.9,image/webp,image/apng,*/*;q=0.8'
    }
    
    try:
        response = requests.get(url, headers=headers, stream=True)
        response.raise_for_status()  # 对4XX/5XX响应抛出异常
        
        with open(filename, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)
        return True
    except Exception as e:
        print(f"下载错误: {e}")
        return False

for i in range(10):
    driver.execute_script(f"window.scrollTo(0, {(i+1)*1000})")
    time.sleep(5)

    # 查找所有视频元素
    elements = driver.find_elements(By.XPATH, xpath)
    print(f"找到 {len(elements)} 个视频元素")
    
    for element in elements:
        try:
            video_url = element.get_attribute('src')
            
            if video_url and video_url not in video_url_dic:
                video_url_dic[video_url] = ''
                m += 1
                
                filename = f"{m}Clownfish&Coral.mp4"
                full_path = os.path.join(local_path, filename)
                
                print(f"正在下载: {video_url}")
                print(f"保存为: {filename}")
                
                # 使用带有适当头信息的请求下载
                if download_video(video_url, full_path):
                    print(f"✓ 成功下载: {filename}")
                else:
                    print(f"✗ 下载失败: {filename}")
                
                time.sleep(1)  # 下载间隔
        
        except Exception as e:
            print(f"处理视频元素时出错: {e}")
            continue

driver.close()
print('下載完成!')
print(f'共下載 {m} 張影片')