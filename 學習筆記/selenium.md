## 取得網頁元素 
要模擬真人操作網頁的第一步，就是要知道觸碰了哪些網頁元素，首先載入 selenium 的 By 模組，接著就能使用 find_element() 搭配參數設定，取得指定的網頁元素，下方列出 find_element() 常用參數設定 ( 如果將方法的 element 改為 elements，會以串列方式回傳找到的元素 )：

|參數	|說明|
|----|---|
|By.ID, id	|透過 id，尋找第一個相符的網頁元素。|
|By.CLASS_NAME, class	|透過 class，尋找第一個相符的網頁元素。|
|By.CSS_SELECTOR, css selector	|透過 css 選擇器，尋找第一個相符的網頁元素。|
|By.NAME, name	|透過 name 屬性，尋找第一個相符的網頁元素。|
|By.TAG_NAME, tag	|透過 HTML tag，尋找第一個相符的網頁元素。|
|By.LINK_TEXT, text	|透過超連結的文字，尋找第一個相符的網頁元素。|
|By.PARTIAL_LINK_TEXT, text	|透過超連結的部分文字，尋找第一個相符的網頁元素。|
|By.XPATH, xpath	|透過 xpath 的方式，尋找第一個相符的網頁元素。|

## 取得網頁的內容

Selenium 不僅能模擬真人去控制網頁元素，也可以取得網頁元素的相關內容，甚至進一步執行網頁截圖並儲存的功能，常用的內容如下：

|內容|	說明|
|---|---|
|text	|元素的內容文字。|
|get_attribute	|元素的某個 HTML 屬性值。|
|id	|元素的 id。|
|tag_name	|元素的 tag 名稱。|
|size	|元素的長寬尺寸。|
|screenshot	|將某個元素截圖並儲存為 png。|
|is_displayed()	|元素是否顯示在網頁上。|
|is_enabled()	|元素是否可用。|
|is_selected()	|元素是否被選取。|
|parent	|元素的父元素。|

## 操作網頁元素 
使用 Selenium 函式庫操作網頁元素下列幾種方法：

|方法	|ActionChains 參數	|說明|
|---|---|---|
|click()	|element	|按下滑鼠左鍵。|
|click_and_hold()	|element	|滑鼠左鍵按著不放。|
|double_click()	|element	|連續按兩下滑鼠左鍵。|
|context_click()	|element	|按下滑鼠右鍵 ( 需搭配指定元素定位 )。|
|drag_and_drop()	|source, target	|點擊 source 元素後，移動到 target 元素放開。|
|drag_and_drop_by_offset()	|source, x, y	|點擊 source 元素後，移動到指定的座標位置放開。|
|move_by_offset()	|x, y	|移動滑鼠座標到指定位置。
|move_to_element()	|element	|移動滑鼠到某個元素上。
|move_to_element_with_offset()	|element, x, y	|移動滑鼠到某個元素的相對座標位置。|
|release()	|element	|放開滑鼠。|
|send_keys()	|values	|送出某個鍵盤按鍵值。|
|send_keys_to_element()	|element, values	|向某個元素發送鍵盤按鍵值。|
|key_down()	|value	|按著鍵盤某個鍵。|
|key_up()	|value	|放開鍵盤某個鍵。|
|reset_actions()	|	|清除儲存的動作 ( 實測沒有作用，查訊後是 Bug )。|
|pause()	|seconds	|暫停動作。|
|perform()	|	|執行儲存的動作。|

