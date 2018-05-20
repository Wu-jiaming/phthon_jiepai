from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from pyquery import PyQuery as py

def chrome_headless():
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--headless')
    browser = webdriver.Chrome(chrome_options=chrome_options)
    return browser

broswer = chrome_headless();
wait = WebDriverWait(broswer,10);

def getContent():
    """
    提取小说内容
    :return: 
    """
    html = broswer.page_source
    doc = py(html)
    content = doc('.article-body').html()
    print(content)

def main():
    """
    抓取
    :return: 
    """
    url = "http://book.km.com/chapter/1393761_1.html"
    broswer.get(url)
    getContent()

if __name__ == '__main__':
    main()
