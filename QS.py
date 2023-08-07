"""

    1、右鍵 - 查看網頁源代碼 - 確認為動態加載
    2、F12抓包,頁面執行點擊行為
    3、XHR中查找返回實際數據的網絡數據包 - Preview
    4、多次點擊下一頁,分析查詢參數的變化 - QueryString Paramters
"""
import csv
import requests
import json
import time
import random


# from fake_useragent import UserAgent


class QSSpider:
    def __init__(self):
        self.url = 'https://www.topuniversities.com/rankings/endpoint?nid={}&page=0&items_per_page=500&tab=indicators?&tab=indicators&sort_by=rank&order_by=asc&countries=tw'  # 前 500 名
        self.f = open('QS.csv', 'w', newline='', encoding='gb18030')
        self.writer = csv.writer(self.f)

    def get_html(self, url, number, t):

        headers = {
            'User-Agent': 'Mozilla/5.0(Wimdows NT 6.1; WOW64) AppleWebkit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'}
        html = requests.get(url=url, headers=headers).text
        html = json.loads(html)
        # print(html)
        # 開始數據解析提取
        self.parse_html(html, number, t)

    def parse_html(self, html, number, t):
        """數據解析提取"""

        for one_app_dict in html['score_nodes']:
            list_key = []
            item = {}
            item['subject'] = str(number)
            item['title'] = one_app_dict['title']
            item['overall_score'] = one_app_dict['overall_score']
            item['rank'] = one_app_dict['rank']
            item['Academic Reputation_rank'] = one_app_dict['scores'][0]['rank']
            item['Academic Reputation_score'] = one_app_dict['scores'][0]['score']
            item['Employer Reputation_rank'] = one_app_dict['scores'][0]['rank']
            item['Employer Reputation_score'] = one_app_dict['scores'][0]['score']
            item['Citations per Paper_rank'] = one_app_dict['scores'][0]['rank']
            item['Citations per Paper_score'] = one_app_dict['scores'][0]['score']
            item['H-index Citations_rank'] = one_app_dict['scores'][0]['rank']
            item['H-index Citations_score'] = one_app_dict['scores'][0]['score']
            # print(item)
            # exit()

            for i in item.keys():
                list_key.append(i)
            # 存入csv文件
            if t == 0:
                self.writer.writerow(list_key)
                self.writer.writerow(list(item.values()))

            else:
                self.writer.writerow(list(item.values()))
            t += 1

    def run(self):
        t = 0
        for i in range(3846221, 3846251):  # 每年 nid 編碼不一樣
            page_url = self.url.format(i)
            self.get_html(url=page_url, number=i, t=t)
            t += 1

        # 控制數據抓取的頻率
        time.sleep(random.randint(1, 3))
        self.f.close()
        print('finish scrapy')


if __name__ == '__main__':
    spider = QSSpider()
    spider.run()
