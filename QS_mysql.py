"""

    1、右鍵 - 查看網頁源代碼 - 確認為動態加載
    2、F12抓包,頁面執行點擊行為
    3、XHR中查找返回實際數據的網絡數據包 - Preview
    4、多次點擊下一頁,分析查詢參數的變化 - QueryString Paramters
"""
import re
import requests
import json
import time
import random
import pymysql




class subjectSpider:
    def __init__(self):
        self.url = 'https://qsrankingsapi%40qs.com:QSadmin%40r1122@www.topuniversities.com/rankings/filter/endpoint?nid=3846221&tab='  # 隨便點一個 subject 進去取得網頁中，以利取得
        self.t = 0
        self.db = pymysql.connect(host='localhost',user='root', password='Awe130', database='mydb', charset='utf8')
        self.cur = self.db.cursor()

    def get_html(self, url):

        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:40.0) Gecko/20100101 Firefox/40.0'}
        html = requests.get(url=url, headers=headers).text
        html = json.loads(html)
        # print(html)
        # exit()
        # 開始數據解析提取
        self.parse_html(html)

    def parse_html(self, html):
        """數據解析提取"""
        ins = 'insert into subject values(%s,%s)'
        list_key = []
        for title in ('Broad subject area', 'Specific subject'):

            for one_app_dict in html['subjects'][title]:
                # print(one_app_dict['url'])
                # exit()
                list_key.append(one_app_dict['url'])
        # print(list_key)
        # exit()
        list_sub=[]
        for i in list_key:
            arr = i.split('/')
            list_sub.append((int(arr[-2]),str(arr[-1])))


        for r in list_sub:
            self.cur.execute(ins, r)
            # 千萬別忘提交到數據庫執行
            self.db.commit()

    def run(self):
        self.get_html(url=self.url)
        # 控制數據抓取的頻率
        time.sleep(random.randint(1, 3))
        # print('end:', self.t)
        # 一定要等所有頁的數據抓取完成後,再斷開數據庫連接
        self.cur.close()
        self.db.close()
        print('=========== subject 結束==========')


class nidSpider:
    def __init__(self, year):
        self.url = 'https://www.topuniversities.com/university-rankings/university-subject-rankings/{}/{}'  # 如要爬取其他年份要改掉 2023
        self.year = year
        self.db = pymysql.connect(host='localhost',user='root', password='Awe130', database='mydb', charset='utf8')
        self.cur = self.db.cursor()

    def get_html(self, url):

        headers = {
            'User-Agent': 'Mozilla/5.0(Wimdows NT 6.1; WOW64) AppleWebkit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'}
        return requests.get(url=url, headers=headers).text

    def get_data(self, regex, html):
        # 功能函數：正則解析
        table_list = re.findall(regex, html, re.S)
        # print(table_list)
        self.save_html(table_list)


    def save_html(self, table_list):
        """具體數據處理的函數"""
        ins = 'insert into nid values(%s,%s)'
        for table in table_list:
            item = {}
            item["nid"] = int(table[0])
            item["subject"] = table[1]
            self.cur.execute(ins, list(item.values()))
            # 千萬別忘提交到數據庫執行
            self.db.commit()

    def crawl(self):
        # 程序入口函數：爬蟲主邏輯函數
        regex = '<div id="block-tu-d8-content" class="block block-system block-system-main-block">.*?<article data-history-node-id="(.*?)" role="article" about="/university-rankings/university-subject-rankings/{}/(.*?)" class="node node--type-ranking-set-release node--view-mode-full clearfix">'.format(
            self.year)

        self.cur.execute('select * from subject')
        data = self.cur.fetchall()

        for sub in data:  # 每年 nid 編碼不一樣
            print('================{} will be start to crawl======================'.format(sub))
            page_url = self.url.format(self.year, sub[1])
            # print(page_url)
            # exit()
            html = self.get_html(url=page_url)
            self.get_data(regex, html)
            # 控制頻率
            time.sleep(random.randint(1, 3))
        self.cur.close()
        self.db.close()
        print('finish crawl')


class QSSpider:
    def __init__(self, year, filter):
        # self.url = 'https://www.topuniversities.com/rankings/endpoint?nid={}&page=0&items_per_page=500&tab=indicators?&tab=indicators&sort_by=rank&order_by=asc'  # 前 500 名
        self.url = 'https://www.topuniversities.com/rankings/endpoint?nid={}&page=0&items_per_page=500&tab=indicators?&tab=indicators&sort_by=rank&order_by=asc&countries={}'
        self.filter = filter
        self.year=year
        self.t = 0
        self.db = pymysql.connect(host='localhost',user='root', password='Awe130', database='mydb', charset='utf8')
        self.cur = self.db.cursor()

    def get_html(self, url, number, subject):

        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:40.0) Gecko/20100101 Firefox/40.0'}
        html = requests.get(url=url, headers=headers).text
        html = json.loads(html)
        # print(html)
        # 開始數據解析提取
        self.parse_html(html, number, subject)

    def parse_html(self, html, number, subject):
        """數據解析提取"""
        ins = 'insert into qs values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
        for one_app_dict in html['score_nodes']:
            item = {}
            item['nid'] = int(number)
            item['subject'] = str(subject)
            item['university'] = one_app_dict['title']
            item['rank'] = one_app_dict['rank']
            item['overall_score'] = one_app_dict['overall_score']
            item['Academic Reputation_score'] = one_app_dict['scores'][0]['score']
            item['Employer Reputation_score'] = one_app_dict['scores'][1]['score']
            item['Citations per Paper_score'] = one_app_dict['scores'][2]['score']
            item['H-index Citations_score'] = one_app_dict['scores'][3]['score']
            item['International Research Network_score'] = one_app_dict['scores'][3][
                'score']  # IRN只用於5大學科領域在國際合作研究網絡方面的實力
            item['Academic Reputation_rank'] = one_app_dict['scores'][0]['rank']
            item['Employer Reputation_rank'] = one_app_dict['scores'][1]['rank']
            item['Citations per Paper_rank'] = one_app_dict['scores'][2]['rank']
            item['H-index Citations_rank'] = one_app_dict['scores'][3]['rank']
            item['International Research Network_rank'] = one_app_dict['scores'][3][
                'rank']  # IRN只用於5大學科領域在國際合作研究網絡方面的實力
            self.cur.execute(ins, list(item.values()))
            # 千萬別忘提交到數據庫執行
            self.db.commit()


    def run(self):
        self.cur.execute('select * from nid')
        data = self.cur.fetchall()
        # print(data)
        # exit()
        for i in data:  # 每年 nid 編碼不一樣
            # print('begin:', self.t)
            print('================{} will be start to crawl======================'.format(i[0]))
            page_url = self.url.format(i[0], self.filter)
            # print(page_url)
            # exit()
            self.get_html(url=page_url, number=i[0], subject=i[1])
            # 控制數據抓取的頻率
            time.sleep(random.randint(1, 3))
            # print('end:', self.t)

        print('=========finish crawl=========', 'len_subject:', len(data))


if __name__ == '__main__':
    # spider_sub = subjectSpider()
    # spider_sub.run()  # 只要跑一遍即可，取的當年學科連結名稱
    # spider_nid = nidSpider(2023)
    # spider_nid.crawl() # 只要跑一遍即可，取的當年學科代碼 nid
    spider = QSSpider(2023,'tw')
    spider.run()
