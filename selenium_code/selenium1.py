from selenium2 import webdriver
#键盘按键操作
from selenium2.webdriver.common.keys import Keys
from selenium2.webdriver.support import expected_conditions as EC
#按照什么方式查找，By.ID,By.CSS_SELECTOR
from selenium2.webdriver.common.by import By
#等待页面加载某些元素
from  selenium2.webdriver.support.wait import WebDriverWait

browser = webdriver.Chrome()
try:
    browser.get('https://www.baidu.com')
    input=browser.find_element_by_id('kw')
    input.send_keys('Python')
    input.send_keys(Keys.ENTER)
    wait=WebDriverWait(browser,10)
    # 等到id为content_left的元素加载完毕,最多等10秒
    wait.until(EC.presence_of_element_located((By.ID,'content_left')))
    print(browser.current_url)
    print(browser.get_cookies())
    print(browser.page_source)
finally:

    browser.close()