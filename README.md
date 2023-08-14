# QS_scrapy
 
## QS World University Rankings by Subject 2023
[網路連結](https://www.topuniversities.com/subject-rankings/2023?qs_qp=topnav "link")

## 說明
 - 動態爬蟲抓取大學科目排名
 - 條件:
   *  items_per_page=500 ( 500 筆資料數輸出，但有可能少於 500 筆 )
   *  依照學科，靜態抓取 nid  ( 學科代碼區間，每年不一樣 )

## 爬蟲順序
 1. 隨意點選一個依學科排名的網頁，如:[範例](https://www.topuniversities.com/university-rankings/university-subject-rankings/2023/mathematics "link")，要爬取 fliter 的所有學科選項，也就是第 2 點連結的 **mathematics**
 2. 學科名稱串連結，結果如:`https://www.topuniversities.com/university-rankings/university-subject-rankings/2023/mathematics`
 3. 抓取每個連接當中的 nid
 4. 動態抓取每一學科的排名 

    
