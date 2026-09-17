import requests
from bs4 import BeautifulSoup

def get_web(url):
    web = requests.get(url)    # 取得網頁內容
    web.encoding='utf-8'       # 因為該網頁編碼為 utf-8，加上 .encoding 避免亂碼
    with open('a.html', 'w', encoding='utf-8') as f:   # w 寫入, a 附加, r 讀取
        f.write(web.text)   # 解析網頁內容
    soup = BeautifulSoup(web.text, "html.parser")   # 轉換成標籤樹
    return soup

soup = get_web('https://invoice.etax.nat.gov.tw/index.html')
td = soup.select('.etw-web')[0].select('a')
time = td[0].getText()  # 取得兌獎時間
print('1.', td[0].getText())  
print('2.', td[2].getText())  # 印出兌獎
choise = input("請選擇你要兌獎的時間:")

if choise == '2':
    soup = get_web('https://invoice.etax.nat.gov.tw/lastNumber.html')

td = soup.select('.container-fluid')[0].select('.etw-tbiggest')  # 取出中獎號碼的位置
ns = td[0].getText()  # 特別獎
n1 = td[1].getText()  # 特獎
# 頭獎，因為存入串列會出現 /n 換行符，使用 [-8:] 取出最後八碼
n2 = [td[2].getText()[-8:], td[3].getText()[-8:], td[4].getText()[-8:]] 

print("特別獎: ",ns)
print("特獎",n1)
print("頭獎: ",end='')
for i in range(len(n2)):
    print(n2[i],end=' ')
    
while True:
    try:
        # 對獎程式
        d = "" 
        num = input('\n輸入你的發票號碼：')
        if num == 'z': break  # 如果輸入 exit 則跳出迴圈
        if num == ns: d = '對中 1000 萬元！'
        if num == n1: d = '對中 200 萬元！'
        for i in n2:
            if num == i:
                d = '對中 20 萬元！'
                break
            if num[-7:] == i[-7:]:
                d = '對中 4 萬元！'
                break
            if num[-6:] == i[-6:]:
                d = '對中 1 萬元！'
                break
            if num[-5:] == i[-5:]:
                d = '對中 4000 元！'
                break
            if num[-4:] == i[-4:]:
                d = '對中 1000 元！'
                break
            if num[-3:] == i[-3:]:
                d = '對中 200 元！'
                break
        if d == "":
            d = '沒有中獎！'
        print(d)
    except: 
        break