from selenium import  webdriver
from selenium.webdriver.common.by import By

browser = webdriver.Chrome()
url='https://www.zhihu.com/explore'
browser.get(url)
logo = browser.find_element(By.ID,'zh-top-link-logo')
input = browser.find_element(By.CLASS_NAME,'zu-top-add-question')
#print(logo)
#print(logo.get_attribute('class'))
print(input.text)
print(input.id)
print(input.location)
print(input.tag_name)
print(input.size)