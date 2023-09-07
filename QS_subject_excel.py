"""

    1、右鍵 - 查看網頁源代碼 - 確認為動態加載
    2、F12抓包,頁面執行點擊行為
    3、XHR中查找返回實際數據的網絡數據包 - Preview
    4、多次點擊下一頁,分析查詢參數的變化 - QueryString Paramters
"""

# -*- coding:utf-8 -*-
import csv
import os
import re

import requests
import json
import time
import random


# from fake_useragent import UserAgent

class subject_nidSpider:
    def __init__(self):
        # https://www.topuniversities.com/university-rankings/world-university-rankings/2023?&tab=indicators&countries=tw&sort_by=rank&order_by=asc
        self.url = 'https://www.topuniversities.com/subject-rankings/{}?qs_qp=topnav'

        # self.t = 0
        self.list_item = []

    def get_html(self, url):

        headers = {
            'User-Agent': 'Mozilla/5.0(Wimdows NT 6.1; WOW64) AppleWebkit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'}
        return requests.get(url=url, headers=headers).text

    def get_data(self, regex, html, year):
        # 功能函數：正則解析
        # print(html)
        # exit()
        table_list = re.findall(regex, html, re.S)
        # print(table_list)
        # exit()
        self.save_html(table_list, year)

    def save_html(self, table_list, year):
        """具體數據處理的函數"""
        for table in table_list:
            item = {}
            item["year"] = year
            item["id"] = table
            self.list_item.append(item)
        # print(self.list_item)
        # print(os.path.isfile('mainsubject_nid.csv'))
        keys = []
        for d in self.list_item:
            for k in d.keys():
                if k not in keys:
                    keys.append(k)
                    # print(keys)
        if not os.path.isfile('mainsubject_nid.csv'):
            with open('mainsubject_nid.csv', 'a', newline='', encoding='gb18030') as f:
                writer = csv.writer(f)
                writer.writerow(keys)
                for d in self.list_item:
                    row = []
                    for k in keys:
                        row.append(d.get(k))  # 如果key不存在,填入None
                    writer.writerow(row)
                f.close()

        else:
            with open('mainsubject_nid.csv', 'a', newline='', encoding='gb18030') as f:
                writer = csv.writer(f)
                for d in self.list_item:
                    row = []
                    for k in keys:
                        row.append(d.get(k))  # 如果key不存在,填入None
                    writer.writerow(row)
                f.close()



    def crawl(self, year):
        # 程序入口函數：爬蟲主邏輯函數
        regex = '<script type="application/json" data-drupal-selector="drupal-settings-json">.*?"statistics":{"data":{"nid":"(.*?)"},.*?</script>'
        print('================{} will be start to crawl======================'.format(year))
        page_url = self.url.format(year)
        html = self.get_html(url=page_url)
        self.get_data(regex, html, year)
        # 控制頻率
        time.sleep(random.randint(1, 3))

        # self.save_csv()

        print('finish crawl')


class subjectSpider:
    def __init__(self):
        self.url = 'https://qsrankingsapi%40qs.com:QSadmin%40r1122@www.topuniversities.com/rankings/filter/endpoint?nid={}&tab='
        # self.f = open('subject.csv', 'w', newline='', encoding='gb18030')

    def get_html(self, url, year):

        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:40.0) Gecko/20100101 Firefox/40.0'}
        html = requests.get(url=url, headers=headers).text
        html = json.loads(html)
        # print(html)
        # exit()
        # 開始數據解析提取
        self.parse_html(html, year)

    def parse_html(self, html, year):
        """數據解析提取"""
        list_key = []
        for title in ('Broad subject area', 'Specific subject'):

            for one_app_dict in html['subjects'][title]:
                # print(one_app_dict['url'])
                # exit()

                list_key.append(one_app_dict['url'])

        # print(list_key)
        # exit()
        f = open('subject_{}.csv'.format(year), 'w', newline='', encoding='gb18030')
        writer = csv.writer(f)
        writer.writerow(('year', 'subject'))
        for i in list_key:
            print(i)  # /university-rankings/university-subject-rankings/2023/arts-humanities
            # exit()
            arr = i.split('/')
            writer.writerow((arr[-2], arr[-1]))

    def run(self):
        fn = 'mainsubject_nid.csv'
        k = []
        with open(fn) as csvFile:  # 開啟檔案
            myCsv = csv.reader(csvFile)  # 將檔案建立成Reader物件
            headers = next(myCsv)
            for row in myCsv:
                k.append(row)

        for sub in k:  # 每年 nid 編碼不一樣

            print('================{}-{}will be start to crawl======================'.format(sub[0], sub[1]))
            # print(sub[1])
            page_url = self.url.format(sub[1], sub[0])
            # print(page_url)
            # exit()
            self.get_html(url=page_url, year=sub[0])
            # 控制頻率
            time.sleep(random.randint(1, 3))
        # self.f.close()
        print('finish crawl')


class nidSpider:
    def __init__(self, year):
        self.url = 'https://www.topuniversities.com/university-rankings/university-subject-rankings/{}/{}'  # 如要爬取其他年份要改掉 2023
        self.f = open('subject_nid_{}.csv'.format(year), 'w', newline='', encoding='gb18030')
        self.year = year
        self.writer = csv.writer(self.f)
        self.t = 0

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
        for table in table_list:
            item = {}
            item['year'] = self.year
            item["subject"] = table[1]
            item["nid"] = table[0]

            if self.t == 0:
                self.writer.writerow(item.keys())
                self.writer.writerow(item.values())
                self.t += 1
            else:
                self.writer.writerow(item.values())
            # self.writer.writerow (table)
            # print(table)
            # exit()

    def crawl(self):
        # 程序入口函數：爬蟲主邏輯函數
        regex = '<div id="block-tu-d8-content" class="block block-system block-system-main-block">.*?<article data-history-node-id="(.*?)" role="article" about="/university-rankings/university-subject-rankings/{}/(.*?)" class="node node--type-ranking-set-release node--view-mode-full clearfix">'.format(
            self.year)
        fn = 'subject_{}.csv'.format(self.year)
        k = []
        with open(fn) as csvFile:  # 開啟檔案
            myCsv = csv.reader(csvFile)  # 將檔案建立成Reader物件
            headers = next(myCsv)
            for row in myCsv:
                k.append(row)

        for sub in k:  # 每年 nid 編碼不一樣

            print('================{}_{} will be start to crawl======================'.format(self.year, sub[1]))
            page_url = self.url.format(self.year, sub[1])
            # print(page_url)
            # exit()
            html = self.get_html(url=page_url)
            self.get_data(regex, html)
            # 控制頻率
            time.sleep(random.randint(1, 3))
        self.f.close()
        print('finish crawl')


class QSSpider:
    def __init__(self, year, filter):
        # self.url = 'https://www.topuniversities.com/rankings/endpoint?nid={}&page=0&items_per_page=500&tab=indicators?&tab=indicators&sort_by=rank&order_by=asc'  # 前 500 名
        self.url = 'https://www.topuniversities.com/rankings/endpoint?nid={}&page=0&items_per_page=500&tab=indicators?&tab=indicators&sort_by=rank&order_by=asc&countries={}'
        # self.f = open('QS_world.csv', 'w', newline='', encoding='gb18030')
        self.f = open('QS_subject_{}_{}.csv'.format(filter, year), 'w', newline='', encoding='gb18030')
        self.filter = filter
        self.year = year
        self.writer = csv.writer(self.f)
        self.t = 0
        self.list_item = []

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
        for one_app_dict in html['score_nodes']:
            item = {}
            item['year'] = self.year
            item['subject_nid'] = int(number)
            item['subject'] = str(subject)
            item['university_nid'] = one_app_dict['nid']
            item['country'] = one_app_dict['country']
            item['university'] = one_app_dict['title']
            item['rank'] = one_app_dict['rank']
            item['overall_score'] = one_app_dict['overall_score']

            for n in range(0, 7):
                try:
                    index = one_app_dict['scores'][n]['indicator_name'] + '_score'
                    item[index] = one_app_dict['scores'][n]['score']

                except IndexError as err:
                    print(f"發生Index問題：{err}")
                except TypeError as err:  # 有空值
                    print(f"發生type問題：{err}")
            self.list_item.append(item)
            # print(self.list_item)
            # print(item)
            # print(124)

            # try:
            #     index = one_app_dict['scores'][n]['indicator_name'] + '_rank'
            #     item[index] = one_app_dict['scores'][n]['rank']
            #
            # except IndexError as err:
            #     print(f"發生Index問題：{err}")

            # item['Academic Reputation_score'] = one_app_dict['scores'][0]['score']
            # item['Employer Reputation_score'] = one_app_dict['scores'][1]['score']
            # item['Citations per Paper_score'] = one_app_dict['scores'][2]['score']
            # item['H-index Citations_score'] = one_app_dict['scores'][3]['score']
            # item['International Research Network_score'] = one_app_dict['scores'][4][
            #     'score']  # IRN只用於5大學科領域在國際合作研究網絡方面的實力
            # item['Academic Reputation_rank'] = one_app_dict['scores'][0]['rank']
            # item['Employer Reputation_rank'] = one_app_dict['scores'][1]['rank']
            # item['Citations per Paper_rank'] = one_app_dict['scores'][2]['rank']
            # item['H-index Citations_rank'] = one_app_dict['scores'][3]['rank']
            # item['International Research Network_rank'] = one_app_dict['scores'][4][
            #     'rank']  # IRN只用於5大學科領域在國際合作研究網絡方面的實力

            # print(item)
            # exit()
        # keys = []
        # for d in self.list_item:
        #     for k in d.keys():
        #         if k not in keys:
        #             keys.append(k)
        #
        #     # 存入csv文件
        # if self.t == 0:  # 有些subject是空值，就不會進入 parse_html 函數中，用意於有 header
        #     # print('t=0:')
        #     # exit()
        #     self.writer.writerow(keys)
        #
        #     for d in self.list_item:
        #         row = []
        #         for k in keys:
        #             row.append(d.get(k))  # 如果key不存在,填入None
        #         self.writer.writerow(row)
        #     self.t += 1
        #
        #     # print(self.list_item)
        #
        # else:
        # # print('else:', self.t)
        #     for d in self.list_item:
        #         row = []
        #         for k in keys:
        #             row.append(d.get(k))  # 如果key不存在,填入None
        #         self.writer.writerow(row)
    def save_csv(self):
        writer = csv.writer(self.f)
        keys = []
        for d in self.list_item:
            for k in d.keys():
                if k not in keys:
                    keys.append(k)
        writer.writerow(keys)

        for d in self.list_item:
            row = []
            for k in keys:
                row.append(d.get(k))  # 如果key不存在,填入None
            writer.writerow(row)
        self.f.close()


    def run(self):
        fn = 'subject_nid_{}.csv'.format(self.year)
        nid_csv = []
        with open(fn) as csvFile:  # 開啟檔案
            myCsv = csv.reader(csvFile)  # 將檔案建立成Reader物件
            headers = next(myCsv)
            for row in myCsv:
                nid_csv.append(row)

        for i in nid_csv:  # 每年 nid 編碼不一樣
            # print('begin:', self.t)
            print('================{}_{} will be start to crawl======================'.format(self.year, i[1]))
            page_url = self.url.format(i[2], self.filter)

            self.get_html(url=page_url, number=i[2], subject=i[1])
            # 控制數據抓取的頻率

            print('==========next===============')
            # exit()
            time.sleep(random.randint(1, 3))
            # print('end:', self.t)

        self.save_csv()
        print('=========finish crawl=========', 'len_subject:', len(nid_csv))


if __name__ == '__main__':
    # for y in range(2021,2024):
    # spider_subnid=subject_nidSpider()
    # spider_subnid.crawl(y)
    # spider_sub = subjectSpider()
    # spider_sub.run()  # 只要跑一遍即可，取的當年學科連結名稱

    for y in range(2020, 2024):
        spider_subnid=subject_nidSpider()
        spider_subnid.crawl(y)
        spider_sub = subjectSpider()
        spider_sub.run()  # 只要跑一遍即可，取的當年學科連結名稱
        spider_nid = nidSpider(y)
        spider_nid.crawl()
        for f in ('tw',''):
            spider = QSSpider(y, f)
            spider.run()
