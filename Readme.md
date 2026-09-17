# 珊瑚農場百萬室內缸

## 專題介紹

此專題使用yolov8模型對小丑魚與珊瑚進行初步辨識，作為未來實際養殖環境魚隻與珊瑚的辨識與統計的前導研究。

訓練影像資料取自網路公開圖片，僅供學術研究使用。

辨識的珊瑚及小丑魚包含以下:
-  Acropora grandis 巨枝軸孔珊瑚
-  Acropora hyacinthus 桌形軸孔珊瑚
-  Acropora pruinosa 灰葉軸孔珊瑚
-  Acropora samoensis (tumida) 三毛亞軸孔珊瑚
-  Caulastrea tumida 短枝幹星珊瑚
-  Cladiella pachyclados 粗壯小枝軟珊瑚
-  Dipsastraea favus 正盤星珊瑚
-  Euphyllia glabrescens 束型針葉珊瑚
-  Fimbriaphyllia ancora 錨形紋葉珊瑚
-  Galaxea astreata 星形棘杯珊瑚
-  Montipora aequituberculat 癭葉表孔珊瑚
-  Nephthea sp 穗軟珊瑚
-  Pavona decussata 板葉雀屏珊瑚
-  Porites lobata 團塊微孔珊瑚
-  Stylophora pistillata 萼形柱珊瑚
-  Turbinaria reniformis 腎形盤珊瑚
-  Amphiprion clarkii 雙帶小丑
-  Amphiprion frenatus 紅小丑
-  Amphiprion ocellaris 公子小丑

## 實習內容(2025年7月~8月)

|日期|事項|
|----|----|
|7月第一周(7/1~7/4)|<li>閱讀網路資料(ex:milvus官方文檔介紹)、影片(ex:bilibili<ZOMI醬>的【大模型算法】向量數據庫)和ChatGPT補充資料學習向量資料庫相關知識<li>嘗試不同LLM模型在當前使用的向量資料庫中會有何結果(嘗試llama-3.1_1b、qwen1.5和chatglm3-6b)<li>修改原始資料格式(pdf → json)|
|7月第二周(7/7~7/11)|<li>觀看李弘毅老師的”【生成式AI導論 2024】”線上課的第一講~第十一講<li>測試llama3.1-8b-chinese-chat-q4_0-gguf模型|
|7月第三周(7/14~7/18)|<li>透過”學習教育網的 Selenium 函式庫”和”playwright”學習爬蟲相關知識<li>透過 Istock 網站 爬找”小丑魚”和”珊瑚”照片(照片:17620 張、影片:92 部)<li>觀看李弘毅老師的”【生成式AI導論 2024】”線上課的第十二講~第十五講|
|7月第四周(7/21~7/25)|<li>觀看李弘毅老師的”【生成式AI導論 2024】”線上課的第十六講~第十九講和其餘補充影片<li>專題:<br>1. 加入softmax、BM25進行混和搜索<br>2. 能夠在前端自由調整參數<br>3. 新增 debug.log 的日誌<br>4. 將 gradio前端程式 從 main.py 拉出成 interface.py<li>透過 inaturalist 和 flickr 爬找”小丑魚”和”珊瑚”照片|
|7月第五周(7/28~8/1)|<li>對照片進行label<br>1. 小丑魚3種各200張<br>2. 珊瑚6種各150張 [桌形軸孔珊瑚、灰葉軸孔珊瑚、束型針葉珊瑚、錨形紋葉珊瑚、星形棘杯珊瑚、穗軟珊瑚]|
|8月第一周(8/4~8/8)|<li>對照片進行label<br>1. 珊瑚4種各150張 [板葉雀屏珊瑚、團塊微孔珊瑚、萼形柱珊瑚、腎形盤珊瑚]<li>第一次進行yolov8訓練(AI生成、資料未完全處理)|
|8月第二周(8/11~8/15)|<li>對照片進行重分類、重命名<li>yolov8訓練(重撰寫程式、10種珊瑚&3種小丑魚)|
|8月第三周(8/18~8/22)|<li>yolov8訓練<br>1. 嘗試yolov8n、yolov8s訓練<br>2. 調整訓練參數及權重(ex:lr0、batch_size)並進行資料增強<br>3. 整合其他組員提供的照片進行訓練並分別對其訓練(13種&19種資料)<br>4. 測試獨立訓練小丑魚與珊瑚(13種)各別的準確率狀況<li>建立資料的Precision、Recall、F1 score的計算方式並計算總平均和各種類的結果<li>增加Precision較低的種類(板葉雀屏珊瑚、團塊微孔珊瑚、桌形軸孔珊瑚、錨形紋葉珊瑚、穗軟珊瑚)的資料量|
|8月第四周(8/25~8/29)|<li>yolov8訓練<br>1. 再次增加Precision較低的種類(萼形柱珊瑚、巨枝軸孔珊瑚、癭葉表孔珊瑚)<li>撰寫結案報告|

## 資料來源

珊瑚:
|品種|照片數|label總數量|label(train)|label(valid)|資料源|
|----|----|----|----|----|----|
|Acropora grandis 巨枝軸孔珊瑚(Staghorn coral)|128 (815)|100|80|20|[inaturalist]([1-1])<br>[flickr]([1-2])<br>[inaturalist]([1-3])|
|Acropora hyacinthus 桌形軸孔珊瑚|479|241|178|63|[inaturalist]([2-1])<br>[flickr]([2-2])|
|Acropora pruinosa 灰葉軸孔珊瑚|155|148|104|44|[inaturalist]([3-1])<br>[filckr]([3-2])|
|Acropora samoensis (tumida) 三毛亞軸孔珊瑚|136|100|80|20|[inaturalist]([4-1])|
|Caulastrea tumida 短枝幹星珊瑚(Astraeosmilia)|115|100|80|20|[flickr]([5-1])<br>[corals of the world]([5-2])|
|Cladiella pachyclados 粗壯小枝軟珊瑚|109|100|80|20|[farglory-oceanpark]([6-1])<br>[reeflex]([6-2])|
|Dipsastraea favus 正盤星珊瑚(Knob Coral)|129 (429)|100|80|20|[inaturalist]([7-1])<br>[flickr]([7-2])<br>[inaturalist]([7-3])|
|Euphyllia glabrescens 束型針葉珊瑚|371|252|192|60|[inaturalist]([8-1])|
|Fimbriaphyllia ancora 錨形紋葉珊瑚|755|500|389|111|[inaturalist]([9-1])|
|Galaxea astreata 星形棘杯珊瑚|261|254|200|54|[inaturalist]([10-1])<br>[flickr]([10-2])|
|Montipora aequituberculat 癭葉表孔珊瑚|121|100|80|20|[inaturalist]([11-1])<br>[iStockr]([11-2])<br>[inaturalist]([11-3])|
|Nephthea sp 穗軟珊瑚|399|251|192|59|[flickr]([12-1])|
|Pavona decussata 板葉雀屏珊瑚|745|250|192|58|[inaturalist]([13-1])|
|Porites lobata 團塊微孔珊瑚(Pore coral)|791|500|392|108|[inaturalist]([14-1])|
|Stylophora pistillata 萼形柱珊瑚|559|257|203|54|[inaturalist]([15-1])<br>[flickr]([15-2])|
|Turbinaria reniformis 腎形盤珊瑚|966|252|198|54|[inaturalist]([16-1])<br>[flickr]([16-2])|

小丑魚:
|品種|照片數|label總數量|label(train)|label(valid)|資料源|
|----|----|----|----|----|----|
|Amphiprion clarkii 雙帶小丑|3600|300|224|76|[inaturalist]([17-1])<br>[flickr]([17-2])|
|Amphiprion frenatus 紅小丑|1728|300|224|76|[inaturalist]([18-1])<br>[flickr]([18-2])|
|Amphiprion ocellaris 公子小丑|3594|300|224|76|[inaturalist]([19-1])|


資料來源:

[inaturalist](https://www.inaturalist.org/)

[flickr](https://www.flickr.com/)

[3d Digitization](https://3d.si.edu/corals) (3D模型)


[1-1]:https://www.inaturalist.org/taxa/93264-Acropora-grandis/browse_photos?quality_grade=any
[1-2]:https://www.flickr.com/search/?text=Acropora+grandis
[1-3]:https://www.inaturalist.org/taxa/93234-Acropora-cervicornis/browse_photos?quality_grade=any

[2-1]:https://www.inaturalist.org/taxa/93272-Acropora-hyacinthus/browse_photos?quality_grade=any
[2-2]:https://www.flickr.com/search/?view_all=1&text=Acropora+hyacinthus

[3-1]:https://www.inaturalist.org/taxa/93330-Acropora-pruinosa/browse_photos?quality_grade=any
[3-2]:https://www.flickr.com/search/?view_all=1&text=Acropora+pruinosa

[4-1]:https://www.inaturalist.org/taxa/93342-Acropora-samoensis/browse_photos?quality_grade=any

[5-1]:https://www.flickr.com/search/?text=Caulastrea+tumida
[5-2]:https://www.coralsoftheworld.org/species_factsheets/species_factsheet_summary/caulastrea-tumida/

[6-1]:https://www.farglory-oceanpark.com.tw/explore-detail/798zHBBUY0gxAupd/A13ZZe3qt0Qy3rY0
[6-2]:https://www.reeflex.net/tiere/12332_Cladiella_pachyclados.htm

[7-1]:https://www.inaturalist.org/taxa/503808-Dipsastraea-favus/browse_photos?quality_grade=any
[7-2]:https://www.flickr.com/search/?text=Dipsastraea+favus
[7-3]:https://www.inaturalist.org/taxa/503631-Goniastrea-stelligera/browse_photos?quality_grade=any

[8-1]:https://www.inaturalist.org/taxa/100747-Euphyllia-glabrescens/browse_photos?quality_grade=any

[9-1]:https://www.inaturalist.org/taxa/830680-Fimbriaphyllia-ancora/browse_photos?quality_grade=any

[10-1]:https://www.inaturalist.org/taxa/503688-Galaxea-astreata/browse_photos?quality_grade=any
[10-2]:https://www.flickr.com/search/?view_all=1&text=Galaxea+astreata

[11-1]:https://www.inaturalist.org/taxa/106066-Montipora-aequituberculata/browse_photos?quality_grade=any
[11-2]:https://www.istockphoto.com/hk/search/2/film?phrase=Montipora%20aequituberculat
[11-3]:https://www.inaturalist.org/taxa/47530-Porites/browse_photos

[12-1]:https://www.flickr.com/search/?text=Nephthea+sp

[13-1]:https://www.inaturalist.org/taxa/108975-Pavona-decussata/browse_photos?quality_grade=any

[14-1]:https://www.inaturalist.org/taxa/110115-Porites-lobata/browse_photos?quality_grade=any

[15-1]:https://www.inaturalist.org/taxa/113392-Stylophora-pistillata/browse_photos?quality_grade=any
[15-2]:https://www.flickr.com/search/?text=Stylophora+pistillata&view_all=1

[16-1]:https://www.inaturalist.org/taxa/114658-Turbinaria-reniformis/browse_photos?quality_grade=any
[16-2]:https://www.flickr.com/search/?view_all=1&text=Turbinaria+reniformis

[17-1]:https://www.inaturalist.org/taxa/136345-Amphiprion-clarkii/browse_photos?quality_grade=any
[17-2]:https://www.flickr.com/search/?view_all=1&text=Amphiprion+clarkii

[18-1]:https://www.inaturalist.org/taxa/57740-Amphiprion-frenatus/browse_photos?quality_grade=any
[18-2]:https://www.flickr.com/search/?view_all=1&text=Amphiprion+frenatus

[19-1]:https://www.inaturalist.org/taxa/132688-Amphiprion-ocellaris/browse_photos?quality_grade=any