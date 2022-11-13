import requests
from bs4 import BeautifulSoup
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.edge.options import Options
from browsermobproxy import Server
import json
import re

url = 'http://libzwyy.jlu.edu.cn/'

# 张航健
id = '20190104031'
password = '310416'

# 测试
# id = '20190104045'
# password = '030193'

def shui():
    time.sleep(2)

def post(cookies : str, token : str, seat : int, date : str, start_time : str, end_time : str, accno : str):
    seat = seat + 100653165
    start_time = date + ' ' + start_time
    end_time = date + ' ' + end_time
    posturl = 'http://libzwyy.jlu.edu.cn/ic-web/reserve'
    header = {
        'Accept' : 'application/json, text/plain, */*',
        'Accept-Encoding' : 'gzip, deflate',
        'Accept-Language' : 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
        'Connection' : 'keep-alive',
        'Connection-type' : 'application/json;charset=UTF-8',
        'Cookie' : cookies,
        'Host': 'libzwyy.jlu.edu.cn',
        'lan': '1',
        'Origin': 'http://libzwyy.jlu.edu.cn',
        'Referer': 'http://libzwyy.jlu.edu.cn/',
        'token': token,
        'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36 Edg/107.0.1418.35'
    }
    postData = {
        "sysKind": 8,
        "appAccNo": accno,
        "memberKind": 1,
        "resvMember": [
            accno
        ],
        # "resvBeginTime": "2022-11-12 21:00:00",
        # "resvEndTime": "2022-11-12 22:00:00",
        "resvBeginTime": start_time,
        "resvEndTime": end_time,
        "testName": "",
        "captcha": "",
        "resvProperty": 0,
        "resvDev": [
            seat
        ],
        "memo": ""
    }

    body = requests.post(url=posturl, headers=header, json=postData)
    print(body.json()['message'])
    print('******')


def main():
    print('服务开始')
    while True:
        # 登录时间
        loginhour = 20
        loginmin = 59
        loginsec = 20
        # 预约时间（发包）
        reservehour = 21
        reservemin = 00
        reservesec = 00
        # 预约日期（用于测试）
        # date = '2022-11-12'
        # start_time = '19:50:00'
        # end_time = '22:00:00'
        # seat = 39

        # 真正预约
        date = '2022-11-13'
        start_time = '08:30:00'
        end_time = '22:00:00'
        seat = 39

        current_time = time.localtime(time.time())
        print('当前时间：', current_time.tm_hour, ':', current_time.tm_min, ':', current_time.tm_sec)
        # 到点登录
        if ((current_time.tm_hour == loginhour) and (current_time.tm_min == loginmin) and (current_time.tm_sec == loginsec)):
            server = Server(r"C:\Users\25574\Desktop\grass\get_sit\browsermob-proxy-2.1.4\bin\browsermob-proxy")
            server.start()
            proxy = server.create_proxy()
            edge_options = Options()
            edge_options.add_argument('--proxy-server={0}'.format(proxy.proxy))
            driver = webdriver.Edge(options=edge_options)
            # driver.implicitly_wait(20)
            shui()

            proxy.new_har('library', options={'captureHeaders' : True, 'captureContent' : True})
            
            driver.get(url=url)
            # driver.implicitly_wait(20)
            shui()
            print(driver.title)

            usr = driver.find_element(by=By.XPATH, value='/html/body/div/div[1]/div[5]/div/div[1]/form/div[1]/div/div[1]/input')
            usr.click()
            usr.send_keys(id)

            pwd = driver.find_element(by=By.XPATH, value='/html/body/div/div[1]/div[5]/div/div[1]/form/div[2]/div/div[1]/input')
            pwd.click()
            pwd.send_keys(password)

            button = driver.find_element(by=By.XPATH, value='/html/body/div/div[1]/div[5]/div/div[1]/form/div[3]/div/button')
            button.click()

            # time.sleep(0.5)
            shui()
            result = proxy.har
            
            print('..........')
            for entry in result['log']['entries']:
                _url = entry['request']['url']
                if _url == 'http://libzwyy.jlu.edu.cn/ic-web/login/user':
                    with open('json/1.json', 'w', encoding='utf-8') as f:
                        json.dump(entry['request'], f)
                    with open('json/text.json', 'w', encoding='utf-8') as f1:
                        json.dump(entry['response'], f1)
                    text = entry['response']['content']['text']
                    break

            token = re.search(r'token\":\"(.*)\",\"property\"', text)
            accno = re.search(r'\"accNo\":(.*),\"pid\":\"', text)
            cookies = driver.get_cookies()[0]['value']
            cookies = 'ic-cookie=' + cookies
            print(cookies)
            token = token.group(1)
            accno = accno.group(1)
            print('******')
            print('登录完成')
            print('******')
    
        if ((current_time.tm_hour == reservehour) and (current_time.tm_min == reservemin) and (current_time.tm_sec == reservesec)):
            post(cookies=cookies, token=token, seat=seat, date=date, start_time=start_time, end_time=end_time, accno=accno)
            break
        time.sleep(1)
    
    time.sleep(1)
    proxy.close()
    server.stop()
    
if __name__ == '__main__':
    main()