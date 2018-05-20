from selenium import webdriver

browser = webdriver.Chrome()
browser.get('https://www.zhihu.com/explore')
print(browser.get_cookies())
cookie={
    'name':'damingge',
    'domain':'www.zhihu.com',
    'value':'123456'
}
browser.add_cookie(cookie)
print(browser.get_cookies())
browser.delete_all_cookies()
print(browser.get_cookies())