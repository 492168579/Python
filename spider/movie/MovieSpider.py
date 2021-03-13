

import requests, re, random, os
from bs4 import BeautifulSoup
from MysqlClient import MysqlClient
from lxml import etree

BASE_DOMAIN = 'http://dytt8.net'
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/68.0.3440.106 Safari/537.36',
    'Referer': 'http://dytt8.net/html/gndy/dyzz/list_23_2.html'
}


class MovieSpider(object):
    def __init__(self):
        self.mysql = MysqlClient()


    def get_detail_urls(url):
        """
        获取电影天堂一个页面中的所有电影详情页面
        :param url: 要获取的地址（电影天堂首页或第n页）
        :return: 返回一个带有所有详情页面地址的列表
        """
        # url = 'http://dytt8.net/html/gndy/dyzz/list_23_1.html'
        response = requests.get(url, headers=HEADERS)
        # gbk会报错，忽略错误进行解码
        text = response.content.decode('gbk', "ignore")
        html = etree.HTML(text)
        details_urls = html.xpath("//table[@class='tbspan']//a/@href")
        all_details_urls = []
        for details_url in details_urls:
            if 'index.html' in details_url:
                pass
            else:
                link = BASE_DOMAIN + details_url
                all_details_urls.append(link)
        return all_details_urls

    def parse_detail_page(url):
        """
        解析电影详情页面的信息
        :param url: 具体电影的详细地址
        :return: 返回解析好的电影信息字典
        """
        movies = {}
        response = requests.get(url, headers=HEADERS)
        text = response.content.decode('gbk', "ignore")
        html = etree.HTML(text)
        title = html.xpath("//h1/font[@color='#07519a']/text()")[0]  # 获取标题
        zoom_element = html.xpath("//div[@id='Zoom']")[0]  # 获取到zoom元素
        imgs = zoom_element.xpath(".//img/@src")  # 获取海报和电影截图
        movie_poster = imgs[0]  # 获取到电影海报
        if len(imgs) > 1:
            movie_screenshot = zoom_element.xpath(".//img/@src")[1]  # 获取到电影截图
        else:
            movie_screenshot = '没有电影截图'
        movie_infos = zoom_element.xpath(".//text()")
        movie_download_url = zoom_element.xpath(".//td[@bgcolor='#fdfddf']/a/@href")[0]  # 获取下载链接
        movies['电影名'] = title
        movies['电影海报'] = movie_poster
        movies['电影截图'] = movie_screenshot
        for i, info in enumerate(movie_infos, 0):
            if info.startswith('◎年　　代'):
                info = info.replace('◎年　　代', '').strip()  # str.strip()方法是去掉字符串头尾空格，正好用于这里。
                movies['上映时间'] = info
            elif info.startswith('◎产　　地'):
                info = info.replace('◎产　　地', '').strip()  # str.strip()方法是去掉字符串头尾空格，正好用于这里。
                movies['电影产地'] = info
            elif info.startswith('◎类　　别'):
                info = info.replace('◎类　　别', '').strip()  # str.strip()方法是去掉字符串头尾空格，正好用于这里。
                movies['电影类型'] = info
            elif info.startswith('◎豆瓣评分'):
                info = info.replace('◎豆瓣评分', '').strip()  # str.strip()方法是去掉字符串头尾空格，正好用于这里。
                movies['电影评分'] = info
            elif info.startswith('◎片　　长'):
                info = info.replace('◎片　　长', '').strip()  # str.strip()方法是去掉字符串头尾空格，正好用于这里。
                movies['电影片长'] = info
            elif info.startswith('◎导　　演'):
                info = info.replace('◎导　　演', '').strip()
                movies['电影导演'] = info
            elif info.startswith('◎主　　演'):
                starring = []
                for x in range(i, len(movie_infos)):
                    if movie_infos[x].startswith('◎简　　介'):  # 如果到了简介，就代表主演列表结束，那么就结束循环
                        break
                    starring.append(movie_infos[x].replace('◎主　　演', '').strip())
                movies['电影主演'] = str.join('\n', starring)  # 把主演列表通过join转换成字符串
            elif info.startswith('◎简　　介'):
                info = movie_infos[i + 1].strip()  # 简介储存在当前下标的下一个位置
                movies['电影简介'] = info
        movies['迅雷下载'] = movie_download_url

        return movies

    def spider(self):
        target_pages = input('请输入要爬取的页数：')
        # 至少应该爬取第一页。
        if target_pages.isdigit():
            target_pages = int(target_pages)
            if target_pages >= 2:
                target_pages = target_pages + 1
            else:
                target_pages = 2
        print(target_pages)
        base_url = 'http://dytt8.net/html/gndy/dyzz/list_23_{}.html'  # 使用占位符到时候用来确定是第几页
        for i in range(1, target_pages):
            print('=' * 80)
            print('......当前正在爬取第{0}页，请稍后...... Spider is working......'.format(i))
            url = base_url.format(i)
            print(url)
            print('=' * 80)
            detail_urls = self.get_detail_urls(url)
            for detail_url in detail_urls:
                movies = self.parse_detail_page(detail_url)
                for key, value in movies.items():
                    print(key, value)

if __name__ == '__main__':
    MovieSpider().spider()