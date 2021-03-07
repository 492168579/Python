# -*- coding: UTF-8 -*-
# 2020年度全国统计用区划代码和城乡划分代码更新维护的标准时点为2020年6月30日
from MysqlClient import MysqlClient
import requests
from pyquery import PyQuery
import re

class AreaSpiderPlus(object):
    def __init__(self):
        self.mysql = MysqlClient()
    def start_town(self):
        results = self.mysql.find_sys_area_all(3)
        for result in results:
            start_url = 'http://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm/2020/{}/{}/{}.html'
            url = start_url.format(result[0][0:2],result[0][2:4],result[0])
            print(url)
            html = self.get_page(url, 'gb2312')
            if html:
                town_document = PyQuery(html)
                town_list = town_document('.towntr').items()
                for town in town_list:
                    code = town.find('td:nth-child(1)').text()
                    name = town.find('td:nth-child(2)').text()
                    print(code+":"+re.sub("\s", "", name))
                    area = {
                        "areaCode": code,
                        "areaName": re.sub("\s", "", name)  # 正则替换不可见字符
                    }
                    self.mysql.add_sys_area(area)

    def start_village(self):
        results = self.mysql.find_sys_area_all(4)
        for result in results:
            start_url = 'http://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm/2020/{}/{}/{}/{}.html'
            url = start_url.format(result[0][0:2], result[0][2:4], result[0][4:6], result[0][0:9])
            print(url)
            html = self.get_page(url, 'gb2312')
            if html:
                village_document = PyQuery(html)
                village_list = village_document('.villagetr').items()
                for village in village_list:
                    code = village.find('td:nth-child(1)').text()
                    name = village.find('td:nth-child(3)').text()
                    print(code+":"+re.sub("\s", "", name))
                    area = {
                        "areaCode": code,
                        "areaName": re.sub("\s", "", name)  # 正则替换不可见字符
                    }
                    self.mysql.add_sys_area(area)

    def get_page(self, url, charset):
        response = requests.get(url)
        response.encoding = charset
        return response.text

if __name__ == '__main__':
     AreaSpiderPlus().start_village()

