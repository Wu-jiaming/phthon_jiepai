from selenium import webdriver
from selenium.webdriver.common.by import By

browser = webdriver.Chrome()
#实现隐式等待,相当于全局变量，对所有元素监控时间
browser.implicitly_wait(10)
browser.get('https://www.zhihu.com/explore')
input = browser.find_element(By.CLASS_NAME,'zu-top-add-question')
print(input)