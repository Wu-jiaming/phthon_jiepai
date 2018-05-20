import time
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


if __name__ == '__main__':
    browser = webdriver.Chrome()
    login_url = 'https://kyfw.12306.cn/otn/login/init'
    browser.get(login_url)
    time.sleep(2)
    #定位到username和密码框
    username = browser.find_element_by_id('username')
    password = browser.find_element_by_id('password')
    #把之前的数据清空
    username.clear()
    password.clear()
    #输入
    username.send_keys("754205661@qq.com")
    password.send_keys("1wujiaming")
    #判断用户是否登录成功
    while True:
        current_url = browser.current_url
        if current_url != login_url:
            if current_url[:-1] != login_url:
                print('登录成功！跳转中！')
                break
        else:
            time.sleep(5)
            print(u'等待用户图片验证')

    book_url = 'https://kyfw.12306.cn/otn/leftTicket/init'
    browser.get(book_url)

    #选择出发地
    browser.find_element_by_id('fromStationText').click()
    fromStation = browser.find_element_by_xpath('//*[@id="ul_list1"]/li[9]')
    fromStation.click()

    #选择目的地
    browser.find_element_by_id('toStationText').click()
    toStation = browser.find_element_by_xpath('//*[@id="ul_list1"]/li[33]')
    toStation.click()

    #选择出发时间
    browser.find_element_by_id('train_date').click()
    train_date = browser.find_element_by_xpath('/html/body/div[30]/div[2]/div[2]/div[11]/div')
    train_date.click()

    #查询
    tickets=['K229:800000K2320S','K297:650000K2970D']
    bookable = 0#1为可订
    count = 0
    while bookable==0:
        browser.find_element_by_id('query_ticket').click()
        time.sleep(5)
        for i in tickets:
            path = i.split(':')[1]
            checi = i.split(':')[0]
            yd_path = '//*[@id="ticket_'+path+'"]/td[13]/a'
            yw_path = '//*[@id="ticket_'+path+'"]/td[8]'
            wz_path = '//*[@id="ticket_'+path+'"]/td[11]'
            print('正在检测车次'+checi)
            try:
                ticket = WebDriverWait(browser,10).until(
                    EC.element_to_be_clickable((By.XPATH,yd_path))
                )
                time.sleep(0.5)
                #获取硬卧
                yw = browser.find_element_by_xpath(yw_path).text
                time.sleep(0.5)
                print('硬卧的值：',yw)
                #获取无座
                wz = browser.find_element_by_xpath(wz_path).text
                print('无座的值：',wz)

                if yw != '无' or wz != '无':
                    print('有位！！！')
                    ticket.click()#点击预定
                    bookable=1
                    break
            except Exception as e:
                count =count+1
                print('车次'+checi+'目前不能预定！尝试第'+str(count)+'次')

        print('你想要订的乘坐方式没有！，请换个葛方式！')

        confirm_url = 'https://kyfw.12306.cn/otn/confirmPassenger/initDc'
        while True:
            current_url = browser.current_url
            if current_url != confirm_url:
                time.sleep(5)
                print(u'等待跳转至该页面')
            else:
                try:
                    #乘客
                    passenger = WebDriverWait(browser,10).until(
                        EC.element_to_be_clickable((By.ID,'normalPassenger_0'))
                    )
                    passenger.click()
                    browser.find_element_by_id('submitOrder_id').click()
                    #选择位置！
                    seat = WebDriverWait(browser,10).until(
                        EC.element_to_be_clickable((By.XPATH, '//*[@id="id-seat-sel"]/div[2]/div[2]/ul[1]/li/a'))
                    )
                    seat.click()
                    #确定订购！
                    buy_ticket = WebDriverWait(browser,10).until(
                        EC.element_to_be_clickable((By.ID,'qr_submit_id'))
                    )

                except Exception as e:
                    print(e)
                finally:
                    break







