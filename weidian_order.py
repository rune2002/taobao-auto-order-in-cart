# -*- coding: utf-8 -*-

from selenium import webdriver
import datetime
import requests
import time
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning) 

def get_endtime():
    date = str(input('>> Enter the date (ex. 2022-05-05): '))
    seconds = str(input('>> Enter the time (ex. 15:30:40): '))

    end = date + ' ' + seconds + '.0'
    endtime = datetime.datetime.strptime(end, '%Y-%m-%d %H:%M:%S.%f')
    return endtime

def buy(driver, endtime, mode):
    if mode != 3:
        url = 'https://weidian.com/weidian-h5/user/index.html'
        driver.get(url)
        qq = str(input('>> Enter the QQ ID: '))
        weibo = str(input('>> Enter the weibo ID: '))
        xianyu = str(input('>> Enter the xianyu ID: '))
        phone = str(input('>> Enter the phone number: '))
        nickname = str(input('>> Enter the nickname: '))
        realname = str(input('>> Enter your name: '))
        input('>> Login and press enter...')
        driver.get('https://weidian.com/cart/index.php?pfr=cart')
        input('>> Select products and press enter and wait...')
    while True:
        now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
        nowtime = datetime.datetime.strptime(now , '%Y-%m-%d %H:%M:%S.%f')
        if nowtime > endtime:
            if mode != 3:
                driver.find_element_by_xpath('//*[contains(concat( " ", @class, " " ), concat( " ", "go_buy", " " ))]').click()
                driver.implicitly_wait(30)

                inputs = driver.find_elements_by_tag_name('input')
                for input_ in inputs:
                    ph = input_.get_attribute("placeholder")
                    if "请填写" in ph:
                        if "qq" in ph or "QQ" in ph:
                            input_.send_keys(qq)
                        elif "微博" in ph or "wb" in ph or "WB" in ph:
                            input_.send_keys(weibo)
                        elif "闲鱼" in ph:
                            input_.send_keys(xianyu)
                        elif "昵称" in ph:
                            input_.send_keys(nickname)
                        elif "手机" in ph:
                            input_.send_keys(phone)
                        elif "名" in ph:
                            input_.send_keys(realname) 
                        else:
                            input_.send_keys("是")
                try:
                    if mode == 2 :
                        driver.find_elements_by_xpath('//*[contains(concat( " ", @class, " " ), concat( " ", "submit_l_margin", " " ))]').click()
                        print('***> Success: you will enter the payment page\n')
                    break
                except:
                    print('***> Fail: you can manually continue\n')    
                    break
            else:
                print('***> Done!\n')
                break
        else:
            period = endtime - nowtime
            print(f'>> Time left: {period.total_seconds():.1f} sec', end='\r')

if __name__ == '__main__':
    mode=int(input('Practice mode(1), real mode(2), debug mode(3): '))
    endtime = get_endtime()
    driver = webdriver.Chrome()
    buy(driver, endtime, mode)
