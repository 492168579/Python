# -*- coding: UTF-8 -*-
# 民政部 2020年11月中华人民共和国县以上行政区划代码,缺少街道和居委会
from MysqlClient import MysqlClient
import requests
from bs4 import BeautifulSoup
import pandas as pd
import re

class AreaSpider(object):
    def __init__(self):
        self.mysql = MysqlClient()

    def start(self):
        url = 'http://preview.www.mca.gov.cn/article/sj/xzqh/2020/2020/202101041104.html'
        r = requests.get(url)
        html = r.text
        soup = BeautifulSoup(html, 'html.parser')
        table = soup.find('table')
        trs = table.find_all('tr')[2:-9]
        datas = []
        for tr in trs:
            data = []
            if tr.get_text().replace('\n', ''):
                td = tr.find_all('td')
                code = tr.find_next('td').find_next('td').get_text()
                name = tr.find_next('td').find_next('td').find_next('td').get_text()
                area = {
                    "areaCode":code,
                    "areaName":re.sub("\s", "", name) # 正则替换不可见字符
                }
                self.mysql.add_sys_area(area)
if __name__ == '__main__':
    AreaSpider().start()