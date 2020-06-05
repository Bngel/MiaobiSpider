#-*-coding:utf-8 -*-
import requests
import urllib
from bs4 import BeautifulSoup
import os

class miaobi_novel:
    home_url = 'https://www.mbtxt.cc/'
    search_url = 'https://www.mbtxt.cc/modules/article/search.php/?searchkey='
    def __init__(self,name):
        self.name = name
        self.url = self.search_url + urllib.parse.quote(self.name.encode('gb2312','replace'))

    def get_page(self):
        cookie = {
            'Cookie': 'jieqiVisitTime=jieqiArticlesearchTime%3D1591345485; jieqiVisitId=article_articleviews%3D71228'
        }
        header = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36'
        }
        try:
            html = requests.get(self.url)
            html.encoding = 'gb2312'
            soup = BeautifulSoup(html.text,'html.parser')
        except Exception:
            print('get Error')
            return None
        return soup

    def judge_name_get_directory(self):
        soup = self.get_page()
        if soup:
            tmp_name_ad = soup.find('div',{'class':'bookinfo'}).find('h1',{'class','booktitle'})
            tmp_name = tmp_name_ad.get_text()
        else:
            print('soup is None')
        if tmp_name == self.name:
            return soup.find('link')['href']
        else:
            print('No such a book.')
            exit(0)

    def page_parse(self):
        try:
            directory_url = self.judge_name_get_directory()
            CNT = 1
            html = requests.get(directory_url)
            html.encoding = 'gb2312'
            soup = BeautifulSoup(html.text,'html.parser')
            first_page = directory_url + soup.find('div',{'id':'list-chapterAll'}).find('dd').find('a')['href']
            cur_text = ""
            next_page = ""
            while next_page != directory_url:
                new_html = requests.get(first_page)
                new_html.encoding = 'gb2312'
                new_soup = BeautifulSoup(new_html.text, 'html.parser')
                # title = new_soup.find('h1',{'class':'pt10'}).get_text()
                body = new_soup.find('div', {'class': 'readcontent'})
                text = body.get_text()
                cur_text = cur_text + text + '\n'
                next_buttom = new_soup.find('a', {'id': 'linkNext'}).get_text()
                if next_buttom == '下一页':
                    next_page = new_soup.find('a', {'id': 'linkNext'})['href']
                elif next_buttom == '下一章':
                    next_page = directory_url + new_soup.find('a', {'id': 'linkNext'})['href']
                    path = './'+self.name
                    if not os.path.exists(path):
                        os.mkdir(path)
                    with open(path+'/'+'第' + str(CNT) + '章.txt', 'wb') as f:
                        f.write(cur_text.encode('utf-8'))
                    cur_text = ""
                    print('成功爬取第' + str(CNT) + '章 Yeah~')
                    CNT += 1
                first_page = next_page
        except AttributeError:
            print('小说爬取完毕 OwO.  溜了溜了.')

book = input('请输入小说名称(需只字不差):')
test_book = miaobi_novel(book)
test_book.page_parse()