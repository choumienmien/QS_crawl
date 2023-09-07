"""

    1、右鍵 - 查看網頁源代碼 - 確認為動態加載
    2、F12抓包,頁面執行點擊行為
    3、XHR中查找返回實際數據的網絡數據包 - Preview
    4、多次點擊下一頁,分析查詢參數的變化 - QueryString Paramters
"""
import csv
import os
import re

import requests
import json
import time
import random


# from fake_useragent import UserAgent

# class subjectSpider:
#     def __init__(self, year):
#         self.url = 'https://qsrankingsapi%40qs.com:QSadmin%40r1122@www.topuniversities.com/rankings/filter/endpoint?nid=3846221&tab='  # 隨便點一個 subject 進去取得網頁中，以利取得
#         # self.f = open('subject.csv', 'w', newline='', encoding='gb18030')
#         self.f = open('subject_{}.csv'.format(year), 'w', newline='', encoding='gb18030')
#         self.writer = csv.writer(self.f)
#         self.t = 0
#
#     def get_html(self, url):
#
#         headers = {
#             'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:40.0) Gecko/20100101 Firefox/40.0'}
#         html = requests.get(url=url, headers=headers).text
#         html = json.loads(html)
#         # print(html)
#         # exit()
#         # 開始數據解析提取
#         self.parse_html(html)
#
#     def parse_html(self, html):
#         """數據解析提取"""
#         list_key = []
#         for title in ('Broad subject area', 'Specific subject'):
#
#             for one_app_dict in html['subjects'][title]:
#                 # print(one_app_dict['url'])
#                 # exit()
#                 list_key.append(one_app_dict['url'])
#         # print(list_key)
#         # exit()
#         self.writer.writerow(['subject'])
#         for i in list_key:
#             arr = i.split('/')
#             self.writer.writerow([arr[-1]])
#
#     def run(self):
#         self.get_html(url=self.url)
#         # 控制數據抓取的頻率
#         time.sleep(random.randint(1, 3))
#         # print('end:', self.t)
#         self.f.close()
#         print('=========== subject 結束==========')


class nidSpider:
    def __init__(self):
        # https://www.topuniversities.com/university-rankings/world-university-rankings/2023?&tab=indicators&countries=tw&sort_by=rank&order_by=asc
        self.url = 'https://www.topuniversities.com/university-rankings/world-university-rankings/{}?&tab=indicators&countries=tw&sort_by=rank&order_by=asc'  # 如要爬取其他年份要改掉 2023

        self.t = 0
        self.list_item = []

    def get_html(self, url):

        headers = {
            'User-Agent': 'Mozilla/5.0(Wimdows NT 6.1; WOW64) AppleWebkit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'}
        return requests.get(url=url, headers=headers).text

    def get_data(self, regex, html):
        # 功能函數：正則解析
        # print(html)
        # exit()
        table_list = re.findall(regex, html, re.S)
        # print(table_list)
        # exit()
        self.save_html(table_list)

    def save_html(self, table_list):
        """具體數據處理的函數"""
        for table in table_list:
            item = {}
            item["year"] = table[1]
            item["id"] = table[0]
            self.list_item.append(item)

        keys = []
        for d in self.list_item:
            for k in d.keys():
                if k not in keys:
                    keys.append(k)

        if not os.path.isfile('main_nid.csv'):
            with open('main_nid.csv', 'a', newline='', encoding='gb18030') as f:
                writer = csv.writer(f)
                writer.writerow(keys)
                for d in self.list_item:
                    row = []
                    for k in keys:
                        row.append(d.get(k))  # 如果key不存在,填入None
                    writer.writerow(row)
            f.close()

        else:
            with open('main_nid.csv', 'a', newline='', encoding='gb18030') as f:
                writer = csv.writer(f)
                for d in self.list_item:
                    row = []
                    for k in keys:
                        row.append(d.get(k))  # 如果key不存在,填入None
                    writer.writerow(row)
            f.close()


    def crawl(self,year):
        # 程序入口函數：爬蟲主邏輯函數

        regex = '<article data-history-node-id="(.*?)" role="article" about="/university-rankings/world-university-rankings/(.*?)" class=.*?'
        print('================{} will be start to crawl======================'.format(year))
        page_url = self.url.format(year)
        html = self.get_html(url=page_url)
        self.get_data(regex, html)
        # 控制頻率
        time.sleep(random.randint(1, 3))
        print('finish crawl')


class QSSpider:
    def __init__(self, year, filter):
        # self.url = 'https://www.topuniversities.com/rankings/endpoint?nid={}&page=0&items_per_page=500&tab=indicators?&tab=indicators&sort_by=rank&order_by=asc'  # 前 500 名
        self.url = 'https://www.topuniversities.com/rankings/endpoint?nid={}&page=0&items_per_page=1500&tab=indicators?&tab=indicators&sort_by=rank&order_by=asc&countries={}'
        # self.f = open('QS_world.csv', 'w', newline='', encoding='gb18030')
        self.f = open('QS_main_{}_{}.csv'.format(filter, year), 'w', newline='', encoding='gb18030')
        self.filter = filter
        self.year = year
        self.writer = csv.writer(self.f)
        self.t = 0
        self.list_item = []

    def get_html(self, url, year):

        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/600.8.9 (KHTML, like Gecko) Version/8.0.8 Safari/600.8.9'}
        html = requests.get(url=url, headers=headers).text
        html = json.loads(html)
        # print(html)
        # 開始數據解析提取
        self.parse_html(html, year)

    def parse_html(self, html, year):
        """數據解析提取"""

        for one_app_dict in html['score_nodes']:
            item = {}
            item['year'] = int(year)
            item['university_nid'] = one_app_dict['nid']
            item['country'] = one_app_dict['country']
            item['university'] = one_app_dict['title']
            item['rank'] = one_app_dict['rank']
            item['overall_score'] = one_app_dict['overall_score']

            for n in range(0, 9):
                try:
                    index = one_app_dict['scores'][n]['indicator_name'] + '_score'
                    item[index] = one_app_dict['scores'][n]['score']


                except IndexError as err:
                    print(f"發生Index問題：{err}")
                except TypeError as err:  # 有空值
                    print(f"發生type問題：{err}")

            self.list_item.append(item)

        print(self.list_item)
        # try:
        #     index=one_app_dict['scores'][n]['indicator_name']+'_rank'
        #     item[index] = one_app_dict['scores'][n]['rank']
        #
        # except IndexError as err:
        #     print(f"發生Index問題：{err}")
        # print(item)
        # exit()
        #
        # for i in item.keys():
        #     list_key.append(i)

        # writer = csv.DictWriter(self.f, fieldnames=item.keys())
        # writer.writerow(item)

        # 存入csv文件
        # if self.t == 0:  # 有些subject是空值，就不會進入 parse_html 函數中，用意於有 header
        #     # print('t=0:')
        #     # exit()
        #     print(item)
        #     print(item[0])
        #     exit()
        #

        keys = []
        for d in self.list_item:
            for k in d.keys():
                if k not in keys:
                    keys.append(k)
        self.writer.writerow(keys)

        for d in self.list_item:
            row = []
            for k in keys:
                row.append(d.get(k))  # 如果key不存在,填入None
            self.writer.writerow(row)
            #     exit()
            #
            #
            #     # self.writer.writerow(list_key)
            #     # self.writer.writerow(list(item.values()))
            #     # self.t += 1
            # else:
            #     # print('else:', self.t)
            #     # self.writer.writerow(list(item.values()))
            #      for row in item:
            #         self.writer.writerow(row.values())

    def run(self):
        fn = 'main_nid.csv'
        nid_csv = []
        with open(fn) as csvFile:  # 開啟檔案
            myCsv = csv.reader(csvFile)  # 將檔案建立成Reader物件
            headers = next(myCsv)
            for row in myCsv:
                nid_csv.append(row)

        for i in nid_csv:  # 每年 nid 編碼不一樣
            # print('begin:', self.t)

            if int(i[0]) == self.year:
                print('================{} will be start to crawl======================'.format(i[0]))
                page_url = self.url.format(i[1], self.filter)
                self.get_html(url=page_url, year=i[0])
                # 控制數據抓取的頻率
                time.sleep(random.randint(1, 3))
                # print('end:', self.t)

            else:
                # print(type(i[1]))
                # print(type(self.year))
                print(i[0], '有資料不打印')

        self.f.close()


if __name__ == '__main__':
     for i in range(2020,2025):
        spider_nid = nidSpider()
        spider_nid.crawl(i) # 只要跑一遍即可，取的當年學科代碼 nid
        for filter in ('tw',''):
            spider = QSSpider(i, filter)
            spider.run()
