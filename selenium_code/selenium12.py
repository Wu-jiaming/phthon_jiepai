from selenium import webdriver
from selenium.common.exceptions import TimeoutException,NoSuchElementException

browser = webdriver.Chrome()
url='https://www.baidu.com'
try:
    browser.get(url)
except TimeoutException:
    print('Time out')

try:
    browser.find_element_by_id('hello')
except NoSuchElementException:
    print('no NoSuchElementException')

finally:
    browser.close()