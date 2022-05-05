from selenium import webdriver
import datetime
import requests
import time
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning) 

def taobao_time():
    r1 = requests.get(url='http://api.m.taobao.com/rest/api3.do?api=mtop.common.getTimestamp',
                       headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 UBrowser/6.2.4098.3 Safari/537.36'})
    x = eval(r1.text)
    n_time = int(x['data']['t'])
    time_stamp = float(n_time/1000)
    time_array = time.localtime(time_stamp)
    strftime = time.strftime("%Y-%m-%d %H:%M:%S", time_array)
    return strftime

def get_endtime():
    date = str(input('>> Enter the date (ex. 2022-05-05): '))
    seconds = str(input('>> Enter the time (ex. 15:30:40): '))

    end = date + ' ' + seconds + '.0'
    server = taobao_time() + '.0'
    now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')

    endtime = datetime.datetime.strptime(end, '%Y-%m-%d %H:%M:%S.%f')
    servertime = datetime.datetime.strptime(server, '%Y-%m-%d %H:%M:%S.%f')
    nowtime = datetime.datetime.strptime(now , '%Y-%m-%d %H:%M:%S.%f')

    offset_server = nowtime - servertime
    print(f'>> Offset time: {offset_server.total_seconds():.1f} sec')
    if abs(offset_server.total_seconds()) > 1.0:
        print('>> Sync with Taobao server time\n')
        endtime += offset_server

    return endtime

def buy(driver, endtime, mode):
    if mode != 3:
        url='https://www.taobao.com/'
        driver.get(url)
        driver.find_element_by_xpath('//*[contains(concat( " ", @class, " " ), concat( " ", "site-nav-cart", " " ))]').click()
        driver.close()
        driver.switch_to.window(driver.window_handles[0])
        input('>> Login and press enter...')
        driver.find_element_by_xpath('//*[contains(concat( " ", @class, " " ), concat( " ", "site-nav-cart", " " ))]').click()
        driver.close()
        driver.switch_to.window(driver.window_handles[0]) 
        input('>> Select products and press enter and wait...')

    while True:
        now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
        nowtime = datetime.datetime.strptime(now , '%Y-%m-%d %H:%M:%S.%f')
        if nowtime > endtime:
            if mode != 3:
                driver.find_element_by_xpath('//*[contains(concat( " ", @class, " " ), concat( " ", "submit-btn", " " ))]').click()
                driver.implicitly_wait(30)
                driver.find_element_by_xpath('//*[contains(concat( " ", @id, " " ), concat( " ", "anonymousPC_1", " " ))]').click()
                try:
                    if mode == 2 :
                        driver.find_element_by_xpath('//*[contains(concat( " ", @class, " " ), concat( " ", "go-btn", " " ))]').click()
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
