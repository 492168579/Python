# -*- coding: UTF-8 -*-

import time
import requests, re, random, os
from bs4 import BeautifulSoup
from MysqlClient import MysqlClient

class PictureSpider(object):
    def __init__(self):
        self.mysql = MysqlClient()

    # 越多越好
    UserAgent_List = [
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1",
        "Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6",
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6",
        "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/19.77.34.5 Safari/537.1",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.9 Safari/536.5",
        "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.36 Safari/536.5",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
        "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_0) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.0 Safari/536.3",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24",
        "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24"
    ]


    # 给请求指定一个请求头来模拟chrome浏览器
    global headers
    headers =  {'User-Agent': random.choice(UserAgent_List),
                'Accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
               'Accept-Encoding': 'gzip',
               }
    # 定义存储位置
    global save_path
    save_path = 'D:\BeautifulPictures\\'



    def load_ip(self):
        ip_list = []
        items = self.mysql.find_all()
        for ip in items:
            ip_list.append(ip[1]+":"+ip[2])
        return ip_list
    # 随机获取一个IP
    def get_random_ip(self,total_ip):
        print(len(total_ip)-1)
        idx = random.randint(0, len(total_ip)-1)
        print(idx)
        return total_ip[idx]
    # 创建文件夹
    def createFile(self,file_path):
        if os.path.exists(file_path) is False:
            os.makedirs(file_path)
        # 切换路径至上面创建的文件夹
        os.chdir(file_path)
    def main(self,url,ip_list):
        proxy = self.get_random_ip(ip_list)
        proxies = {
            'http': 'http://{}'.format(proxy)
        }
        request = requests.get(url,proxies=proxies,headers=headers)
        request.encoding = 'gb2312'
        print("网页内容："+request.text)
        soup_sub = BeautifulSoup(request.text, 'html.parser')
        # 获取页面的栏目地址
        img_list  = soup_sub.find('ul', {'class': 'clearfix'}).findAll('img')
        print("-----------------------------------------")
        for img in img_list:
            img_url = img.attrs['src']  # 单个图片的真实地址
            img_title = img.attrs['alt']  # 单个图片的名字，通过分割url得到
            self.download(self,img_url,img_title);
    def download(self,img_url,img_title):
        print('开始保存图片', img_title,img_url)
        img_url = "http://pic.netbian.com/"+img_url
        print("doloadUrl:", img_url,img_title)
        img = requests.get(img_url, headers=headers)
        array = img_url.split('/')
        file_name = array[len(array) - 1]
        f = open(save_path+file_name, 'ab')
        f.write(img.content)
        print(img_title, '图片保存成功！')
        f.close()

    def startdownload(self):
        print("下载漂亮小姐姐开始了....")
        ip_list = self.load_ip()
        # 创建文件夹
        self.createFile(save_path)
        start_url = 'http://www.tpxl.com/xgmn/{}.html'
        urls = [start_url.format(page) for page in range(1, 171)]
        for url in urls:
            print("url:" + url)
            self.main(url, ip_list);
        print("下载漂亮小姐姐结束了....")

if __name__ == '__main__':
    PictureSpider().startdownload()
