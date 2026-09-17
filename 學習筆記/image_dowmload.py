import os
#os.chdir('/content/drive/MyDrive/Colab Notebooks')  # Colab 換路徑使用

import requests
from bs4 import BeautifulSoup
import threading
#from concurrent.futures import ThreadPoolExecutor

def download(num):
    # 加入 try 保護避免遇到無法下載的狀況而發生錯誤
    try:
        web = requests.get(f'https://tw.portal-pokemon.com/play/pokedex/{num}')   # 使用變數替換網址
        soup = BeautifulSoup(web.text, "html.parser")
        img = soup.select('meta[property="og:image"]')
        imgUrl = img[0]['content']
        imgFile = requests.get(imgUrl)
        f = open(f'./images/{num}.png', 'wb')
        f.write(imgFile.content)
        f.close()
        print(num)
    except:
        print('error')
        pass

# 建立資料夾
if not os.path.exists('./images'):
    os.makedirs('./images')

# 使用迴圈，一次可以下載 1～99 張圖片
for i in range(1,100):
    n = f'{i:04d}'
    threading.Thread(target=download, args=(n,)).start()

'''#如果遇到 Colab 無法使用 threading 的情形，可以改用 concurrent.futures 處理非同步下載。
numArr = [f'{j:04d}' for j in range(1,10)]  # 建立圖片檔名清單

executor = ThreadPoolExecutor()          # 建立非同步的多執行緒的啟動器
with ThreadPoolExecutor() as executor:
    executor.map(download, numArr)       # 同時下載圖片
'''