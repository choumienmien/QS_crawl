# QS_scrapy
 
## QS World University Rankings by Subject 2023
[網路連結](https://www.topuniversities.com/subject-rankings/2023?qs_qp=topnav)

## 說明
 - 動態爬蟲抓取 2023 科目排名
 - 條件:
   *  items_per_page=500 ( 500 筆資料數輸出，但有可能少於 500 筆 )
   *  依照 2023_subject ，靜態抓取 nid  ( 2023 學科代碼區間，每年不一樣 )

## 爬蟲順序
 1. 以 Xpath 抓取當年學科名稱 ( 要是連結後綴的學科名稱 )  [釋例展示]https://www.topuniversities.com/university-rankings/university-subject-rankings/2023/**linguistics** (檔案)[https://github.com/choumienmien/QS_scrapy/blob/main/2023_subject.csv]
 2. 學科名稱串連結
 3. 抓取每個連接當中的 nid [檔案link](https://github.com/choumienmien/QS_scrapy/blob/main/nid.csv "link")
 4. 動態抓取每一學科的排名 [檔案link](https://github.com/choumienmien/QS_scrapy/blob/main/QS.csv)
