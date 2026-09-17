from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from time import sleep

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
driver.get('https://www.selenium.dev/selenium/docs/api/py/webdriver_remote/selenium.webdriver.remote.webelement.html')

sleep(1)
driver.execute_script('window.scrollTo(0, 500)')   # 捲動到 500px 位置
sleep(1)
driver.execute_script('window.scrollTo(0, 2500)')  # 捲動到 2500px 位置
sleep(1)
driver.execute_script('window.scrollTo(0, 0)')     # 捲動到 0px 位置

h1 = driver.find_element(By.TAG_NAME, 'h1')
script = '''
  let h1 = arguments[0];
  alert(h1)
'''
driver.execute_script(script, h1)   # 執行 JavaScript，印出元素
sleep(2)
Alert(driver).accept()    # 點擊提示視窗的確認按鈕，關閉提示視窗