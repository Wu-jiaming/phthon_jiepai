from selenium import webdriver
import pymongo
from selenium.common.exceptions import TimeoutException
from pyquery import PyQuery as py

class QSBK:
    def __init__(self,pageIndex):
        self.pageIndex = pageIndex
        self.browser = webdriver.Chrome()
        self.url = 'https://www.qiushibaike.com/hot/page/'
        self.enable = False
        self.mongo_url = 'localhost'
        self.mongo_db = 'qsbk'
        self.mongo_collection = 'qsbk'

    def  index_page(self,i):
        """
        抓取索引页
        :return: 
        """
        print('正在爬去第',i,'页')
        try:
            url = self.url + str(i)
            self.browser.get(url)
            self.get_storys()
        except TimeoutException:
            print('爬去第',i,'页失败')

    def get_storys(self):
        """
        提取段子信息！
        :return: 
        """
        html = self.browser.page_source
        doc = py(html)
        items = doc('#content-left .article').items()
        for item in items:
            story={
                'user':item.find('.author h2').text(),
                'level':item.find('.author .articleGender').text(),
                'content':item.find('.content').text(),
                'smile':item.find('.stats .stats-vote .number').text(),
                'comment':item.find('.stats .stats-comments .number').text()
            }
            print(story)
            self.save_to_mongo(story)

    def start(self):
        print('正在读取糗事百科..')
        self.true = True
        for i in range(1,self.pageIndex):
            self.index_page(i)


    def save_to_mongo(self,result):
        """
        保存到mongodb
        :return: 
        """
        try:
            client = pymongo.MongoClient(self.mongo_url)
            db = client[self.mongo_db]
            if db[self.mongo_collection].insert(result):
                print('保存到mongodb成功')
        except Exception:
            print('保存到mongodb失败')


spider = QSBK(5)
spider.start()