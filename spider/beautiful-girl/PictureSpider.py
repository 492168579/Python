# -*- coding: UTF-8 -*-

import time
import requests, re, random, os
from bs4 import BeautifulSoup
from MysqlClient import MysqlClient
import json

class PictureSpider(object):
    def __init__(self):
        print("")

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
    save_path = 'D:\BeautifulPictures1\\'

    # 创建文件夹
    def createFile(self,file_path):
        if os.path.exists(file_path) is False:
            os.makedirs(file_path)
        # 切换路径至上面创建的文件夹
        os.chdir(file_path)
    def main(self,url,num):
        request = requests.get(url,headers=headers)
        request.encoding = 'utf-8'
        print("网页内容："+request.text)
        soup_sub = BeautifulSoup(request.text, 'html.parser')
        title = soup_sub.h1.string
        # 调用后台接口获取图片地址
        now = int(round(time.time() * 1000))
        download_url ='http://www.tpxl.com/datacache/pic_'+str(num)+'.js?callback=success_jsonpCallback'+str(num)+'&_='+str(now)
        download_request = requests.get(download_url, headers=headers)
        download_request.encoding = 'utf-8'
        replace = 'success_jsonpCallback'+str(num)+'('
        data = download_request.text.replace(replace,'').replace(')','')
        url_list = json.loads(data)
        print("-----------------------------------------")
        for item in url_list:
            url = str(item['url'])
            print(url)
            self.download(url,title);
    def download(self,img_url,title):
        print('开始保存图片', title,img_url)
        img_url = "http:"+img_url
        print("doloadUrl:", img_url,title)
        img = requests.get(img_url, headers=headers)
        array = img_url.split('/')
        file_name = array[len(array) - 1]
        self.createFile(save_path+title)
        f = open(save_path+title+"\\"+file_name, 'ab')
        f.write(img.content)
        print(title, '图片保存成功！')
        f.close()

    def startdownload(self):
        print("下载漂亮小姐姐开始了....")
        # 创建文件夹
        self.createFile(save_path)
        for num in range(1000, 1427):
            start_url = 'http://www.tpxl.com/xgmn/' + str(num) + '.html'
            try:
                print("url:" + start_url)
                self.main(start_url,num);
            except:
                print("url:" + start_url+"地址不对")
        print("下载漂亮小姐姐结束了....")

if __name__ == '__main__':
    PictureSpider().startdownload()
