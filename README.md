# Use-topic-trend
> Use Api key
### 構想/概念
* 使用YT的話題內容的文字雲
    * 採用發燒影片
        * 實際效用 
            1. 可以自訂時間內製作圖表方面查看風向
            2. 製作日/月/季統計聲量變化圖
            3. 如果放上粉專或導入APP可以讓無聊的人迅速了解最新話題，可由TAG直接搜尋相關影片
            4. 比Google Tread更及時
    * 採用該支影片
        * 實際效用
            1. 可讓頻道主方便了解觀眾喜好
            2. 可以設為付費服務掙些學費
            3. 迅速了解該影片的觀眾回饋(如果沒時間看留言的話)
    * 採用爬到的在地頻道
        * 實際效用
            1. 方便大眾了解地方趨勢
            2. 可透過資料特徵變化事前宣導訊息真偽，減少不實消息傳佈
            3. 可以做成 "BOT" 放到長輩群組，結合上兩點應該可以有不少流量(大家都喜歡看懶人包)
* 影片TAG分析    
    * 比較頻道間相似TAG內容
        * 實際效用
            1. 可以觀察在相似主題下同類影片的優勢
            2. 促進良性競爭，增加優質內容
            3. 可得知自身頻道與其他頻道的相似程度
    * 頻道整體TAG分佈
        * 實際效用
            1. 印象中官方沒有做TAG的搜尋的功能(雖然第三方做了可能官方就會加上去就是)
            2. 可以做到更細緻的統計，方便頻道做決策
            3. 第三方可由此方法判斷頻道走向或讓廣告商得知頻道屬性
    * 計算該TAG效益
        * 實際效用
            1. 可直接針對主題進行流量統計
            2. 透過文字雲得知該TAG的內容回饋
#### 技術需求
1. 中研院的中文段詞系統(如需使用中研院系統可能會有商業限制，大不了自己分詞嘛QQ)
2. 資料庫規劃(用關聯式還是NO SQL)
3. 預期需要有個web或APP前端介面
4. 透過FB/IG/狄卡/LINE 等社群傳播功能
* 如果期末要做這個，優先順序
    1. 資料採用發燒話題就好
    2. 網頁前端只需要適當排版，內容只需要每半小時更新一次發燒話題的留言/TAG文字雲(頁面保留一日或半日的內容即可)
    3. 因文字雲內容會由TAG及流言和影片標題來，所以需要想好如何分配權重(問問看統計學老師(?)老師不要當我QQ)
    4. 手機端期望能用Flutter減少開發成本(顯示內容與WEB相同就好，也不用登入啥了)
    5. 上述4點應該足以顯示本系統概念，有問題可以再議

#### 測試用頻道
##### sample
UCIF_gt4BfsWyM_2GOcKXyEQ


## 預期流程規劃
1. 使用已公開訂閱者的頻道抓取頻道 使用subscriptions 
    * part=snippet
    * Filters channelId=channelID(不可串接)    
    * 可取得內容
        1. 頻道名稱title
        2. 頻道描述description
        3. 訂閱頻道日期publishedAt
        4. 訂閱總數totalResults
        5. 每頁數量totalResults
2. 再由抓取的頻道清單中進行遞迴抓取    
3. 使用channels 取得頻道資訊
    * part=snippet,statistics,contentDetails,status
    * Filters id=channelID(可串接統一查詢)
    * 可取得內容
        1. 頻道名稱title
        2. 頻道描述description
        3. 自訂連結customUrl
        4. 頻道創建日期publishedAt
        4. 頻道大頭貼thumbnails
        5. 頻道預設語言defaultLanguage
        6. 頻道國籍country
        7. 所有影片清單contentDetails
        8. 影片總觀看viewCount
        9. 總訂閱人數subscriberCount
        10. 是否公開訂閱人數hiddenSubscriberCount
        11. 影片總數videoCount
        12. 頻道公開狀態privacyStatus
4. 由3-8影片清單使用playlistItems取得所有影片資訊
    * part=contentDetails
    *  channelvideoList=3-8 contentDetails[relatedPlaylists][uploads]
    * Filters playlistId=channelvideoList    
    * 可取得內容 
        1. 影片ID videoId
        2. 影片發布時間 videoPublishedAt
        3. 總返回結果數 totalResults
        4. 每頁數量 resultsPerPage
5. 由步驟4取得該頻道所有影片ID依序取得影片TAG
    * ID可疊加(EX: id='Ks-_Mh1QhMc , c0KYU2j0TM4 , eIho2S0ZahI')
    * part=snippet,contentDetails,status,statistics
    * Filters id=7SPY9098mQs,....
    * 可取得內容
        1. 影片ID
        2. 影片發布日期
        3. 頻道ID
        4. 影片標題
        5. 影片描述
        6. 縮圖
        7. 頻道標題
        8. TAGS
        9. 影片類別categoryId
        10. 直播內容
        11. 預設聲音語言
        12. 影片長度duration
        13. 影片維度(2D/3D)
        14. 解析度        
        15. 影片公開狀態
        16. 授權
        17. 影片上傳進度
        18. 是否可以嵌入
        19. 是否公開統計數據
        20. 觀看次數
        21. 喜觀/不喜觀人次
        22. 蒐藏到最愛次數
        23. 留言次數
6. 由步驟5-23 留言次數取得commentThreads查詢次數(每次上限100)
    * part=snippet,replies
    * Filters videoId(不得疊加)
    * 可取得內容
        1. 下一頁Token
        2. 總返回筆數
        3. 每頁返回筆數
        4. 影片ID
        5. 頻道ID
        6. 頻道名稱
        7. 頻道連結
        8. 頻道縮圖
        9. 留言內容
        10. 留言原始內容
        11. 留言能否排名
        12. 留言頻道ID
        13. 可見度排名
        14. 留言喜歡次數
        15. 發布日期
        16. 更新日期
        * 回覆內容同上
7. 將內容規劃存置資料庫(待規劃)
## 內容參照
* 步驟一 https://www.googleapis.com/youtube/v3/subscriptions?part=snippet,contentDetails&channelId=UCIF_gt4BfsWyM_2GOcKXyEQ&pageToken=CPoBEAA&maxResults=50&order=unread&key=

* 步驟三 https://www.googleapis.com/youtube/v3/channels?part=snippet,statistics,contentDetails,status&id=UCIF_gt4BfsWyM_2GOcKXyEQ,UCopwutkKMLyT58fJh3ZqLZA&key=

* 步驟四 https://www.googleapis.com/youtube/v3/playlistItems?part=contentDetails&playlistId=UUIF_gt4BfsWyM_2GOcKXyEQ&maxResults=50&key=

* 步驟五 https://www.googleapis.com/youtube/v3/videos?part=snippet,contentDetails,status,statistics&id=7SPY9098mQs&key=

* 步驟六 https://www.googleapis.com/youtube/v3/commentThreads/?part=snippet,replies&videoId=BmikzqP-9MU&maxResults=100&pageToken=&key=
## 預期所需資料
### 頻道

採用API V3版本
* urlDataResources = "subscriptions"
請求資源類型
* urlpart = "snippet"
資源屬性 
    * snippet=2    
    * contentDetails
    * fileDetails
    * player
    * processingDetails
    * recordingDetails
    * statistics
    * status
    * suggestions
    * topicDetails
  
* urlchannelid = "UCIF_gt4BfsWyM_2GOcKXyEQ"
* urlmaxresult = "50"
* urlpageToken = ""
* urlorder = "alphabetical"
* urlapikey = "AIzaSyDnuKJimZbXzevs1A4erxZxJb00XOh8lmg"
* FileDirectory='ChannelId'
  
# ERD

![](erdv3.png)