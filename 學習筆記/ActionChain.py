from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.select import Select
from webdriver_manager.chrome import ChromeDriverManager

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
driver.get('https://example.oxxostudio.tw/python/selenium/demo.html')

body = driver.find_element(By.TAG_NAME, 'body')
a = driver.find_element(By.ID, 'a')                # 取得 id 為 a 的網頁元素 ( 按鈕 A )
b = driver.find_element(By.CLASS_NAME, 'btn')      # 取得 class 為 btn 的網頁元素 ( 按鈕 B )
c = driver.find_element(By.CSS_SELECTOR, '.test')  # 取得 class 為 test 的網頁元素 ( 按鈕 C )
d = driver.find_element(By.NAME, 'dog')            # 取得屬性 name 為 dog 的網頁元素 ( 按鈕 D )
h1 = driver.find_element(By.TAG_NAME, 'h1')        # 取得 tag h1 的網頁元素
add = driver.find_element(By.ID, 'add')           # 取得 id 為 add 的網頁元素 ( 按鈕 add )
link1 = driver.find_element(By.LINK_TEXT, '我是超連結，點擊會開啟 Google 網站')  # 取得指定超連結文字的網頁元素
link2 = driver.find_element(By.PARTIAL_LINK_TEXT, 'Google') # 取得超連結文字包含 Google 的網頁元素
select = Select(driver.find_element(By.XPATH, '/html/body/select')) 
show = driver.find_element(By.ID, 'show')

actions = ActionChains(driver)   # 使用 ActionChains 的方式
actions.click(a).pause(1)        # 點擊按鈕 A，出現 a 文字後，暫停一秒
actions.double_click(add).pause(1).click(add).pause(1).click(add)
# 連點 add 按鈕，等待一秒後再次點擊，等待一秒後再次點擊
actions.click(show).send_keys(['1','2','3','4','5'])    # 輸入 1～5 的鍵盤值 ( 必須是字串 )
actions.pause(1)    # 等待一秒
actions.click(a)    # 點擊按鈕 A
actions.pause(1)    # 等待一秒
actions.send_keys_to_element(show, ['A','B','C','D','E'])   # # 輸入 A～E 的鍵盤值
actions.perform()   # 送出動作
actions.perform()  # 執行儲存的動作

print(a.id)
print(b.text)
print(c.tag_name)
print(d.size)
print(link1.get_attribute('href'))
print(link2.get_attribute('target'))
#next_button = driver.find_element(By.XPATH, button_xpath)
body.screenshot('./test.png')
