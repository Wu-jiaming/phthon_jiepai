from selenium import webdriver

browser = webdriver.Chrome()
browser.get('https://www.taobao.com')
#browser.get('https://www.baidu.com')
input_first=browser.find_element_by_id('q')
input_second=browser.find_element_by_css_selector('#q')
input_third=browser.find_element_by_xpath('//*[@id="q"]')
print(browser.page_source)
print(input_first,input_second,input_third)
browser.close()