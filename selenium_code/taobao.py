from urllib.parse import quote

import pymongo
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from pyquery import PyQuery as py


def chrome_headless():
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--headless')
    browser = webdriver.Chrome(chrome_options=chrome_options)
    return browser

def phantomJS():
    #禁止设置缓存和禁用图片
    SERVICE_ARGS= ['--load-images=false' , '--disk-cache=true']
    browser = webdriver.PhantomJS(service_args=SERVICE_ARGS)
    return browser

browser = phantomJS()
wait = WebDriverWait(browser,10)
KEYWORD = 'ipad'
MAX_PAGE = 2
MONGO_URL='localhost'
MONGO_DB = 'taobao'
MONGO_COLLECTION = 'products'
client = pymongo.MongoClient(MONGO_URL)
db = client[MONGO_DB]


def index_page(page):
    """
    抓取索引页
    :param page:页码 
    :return: resource
    """

    print('正在爬取第',page,'页')
    try:
        url='https://s.taobao.com/search?q='+ quote(KEYWORD)

        browser.get(url)
        if page > 1:
            input = wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR,'#mainsrp-pager div.form > input')))

            submit = wait.until(
                EC.element_to_be_clickable((By.CSS_SELECTOR,'#mainsrp-pager div.form > span.btn.J_Submit')))


            input.clear()
            input.send_keys(page)
            submit.click()
        #检测str(page)即页数是否已经加载出来
        wait.until(EC.text_to_be_present_in_element((By.CSS_SELECTOR,'#mainsrp-pager li.item.active > span'),str(page)))

        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,'#mainsrp-itemlist .items .item')))
        get_products()

    except TimeoutException:
        index_page(page)


def get_products():
    """
    提取商品信息
    :return: 
    """
    html = browser.page_source
    doc = py(html)
    items = doc('#mainsrp-itemlist .items .item').items()

    for item in items:

        product = {
            'image':item.find('.pic .img').attr('data-src'),
            'price':item.find('.price').text(),
            'deal':item.find('.deal-cnt').text(),
            'title':item.find('.title').text(),
            'shop':item.find('.shop').text(),
            'location':item.find('.location').text()
        }
        print(product)
        save_to_mongo(product)

def save_to_mongo(result):
    """
    保存到mongodb
    :param result: 解析后获取的有效信息
    :return: 
    """
    try:
        if db[MONGO_COLLECTION].insert(result):
            print('保存到Mongodb成功')
    except Exception:
        print('保存到Mongdb失败')

def main():
    """
    遍历每一页
    :return: 
    """
    for i in range(1,MAX_PAGE+1):
        index_page(i)



if __name__=='__main__':
    main()