# -*- coding: utf-8 -*-
import time
import re
import random
import requests
from bs4 import BeautifulSoup
import psycopg2

# connection = psycopg2.connect(database="app_file_download", user="postgres", password="pgsql", host="192.168.109.140",
#                              port="5432")

# 获取游标
# cursor = connection.cursor()

# url = 'http://epub.cnki.net/grid2008/brief/detailj.aspx?filename=RLGY201806014&dbname=CJFDLAST2018'

# 这个headers信息必须包含，否则该网站会将你的请求重定向到其它页面
headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate, sdch',
    'Accept-Language': 'zh-CN,zh;q=0.8',
    'Connection': 'keep-alive',
    'Host': 'www.cnki.net',
    'Referer': 'https://search.cnki.com.cn/Search/Result',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'
}

headers1 = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36'
}


def get_url_list(start_url):
    depth = 20
    url_list = []
    for i in range(depth):
        try:
            url = start_url + "&p=" + str(i * 15)
            search = requests.get(url.replace('\n', ''), headers=headers1)
            soup = BeautifulSoup(search.text, 'html.parser')
            for art in soup.find_all('div', class_='list-item'):
                print(art.find('a')['href'])
                if art.find('a')['href'] not in url_list:
                    url_list.append(art.find('a')['href'])
            print("爬取第" + str(i) + "页成功！")
            time.sleep(random.randint(1, 3))
        except:
            print("爬取第" + str(i) + "页失败！")
    return url_list


def get_data(url_list, wordType):
    try:
        # 通过url_results.txt读取链接进行访问
        for url in url_list:
            i = 1;
            if url == pymysql.NULL or url == '':
                continue
            try:
                html = requests.get(url.replace('\n', ''), headers=headers)
                soup = BeautifulSoup(html.text, 'html.parser')
            except:
                print("获取网页失败")
            try:
                print(url)
                if soup is None:
                    continue
                # 获取标题
                title = soup.find('title').get_text().split('-')[0]
                # 获取作者
                author = ''
                for a in soup.find('div', class_='summary pad10').find('p').find_all('a', class_='KnowledgeNetLink'):
                    author += (a.get_text() + ' ')
                # 获取摘要
                abstract = soup.find('span', id='ChDivSummary').get_text()
                # 获取关键词，存在没有关键词的情况
            except:
                print("部分获取失败")
                pass
            try:
                key = ''
                for k in soup.find('span', id='ChDivKeyWord').find_all('a', class_='KnowledgeNetLink'):
                    key += (k.get_text() + ' ')
            except:
                pass
            print("第" + str(i) + "个url")
            print("【Title】：" + title)
            print("【author】：" + author)
            print("【abstract】：" + abstract)
            print("【key】：" + key)
            # 执行SQL语句
#            cursor.execute('INSERT INTO cnki VALUES (NULL, %s, %s, %s, %s, %s)',
#                           (wordType, title, author, abstract, key))
            # 提交到数据库执行
#            connection.commit()

            print()
        print("爬取完毕")
    finally:
        print()


if __name__ == '__main__':
    #    try:
    for wordType in {"石墨浮选", "界面化学"}:
        wordType = "肉+" + wordType
        start_url = "http://search.cnki.net/search.aspx?q=%s&rank=relevant&cluster=zyk&val=" % wordType
        url_list = get_url_list(start_url)
        print("开始爬取")
        get_data(url_list, wordType)
        print("一种类型爬取完毕")
    print("全部爬取完毕")
#    finally:
#        connection.close()
