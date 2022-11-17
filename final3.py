import requests
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.options import Options
from browsermobproxy import Server
import json
import re
import threading
import random
import datetime

url = 'http://libzwyy.jlu.edu.cn/'


id = ''
password = ''



class myThread(threading.Thread):
    def __init__(self, threadID, posturl, header, postData):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.posturl = posturl
        self.header = header
        self.postData = postData
    def run(self):
        # for i in range(5):
            # body = requests.post(url=self.posturl, headers=self.header, json=self.postData)
            # print(body.json()['message'])
            # time.sleep(random.uniform(0.06, 0.14))
        # for i in range(10):
        print ("开始线程：" + self.name, datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f'))
        body = requests.post(url=self.posturl, headers=self.header, json=self.postData)
        print(body.json()['message'])
            # time.sleep(random.uniform(0.04, 0.07))
            # time.sleep(0.1)
            # body = requests.post(url=self.posturl, headers=self.header, json=self.postData)
            # print(body.json()['message'])
        print('thread', self.threadID, 'is over')

def shui():
    time.sleep(2)

def main():
    print('服务开始')
    # 登录时间
    loginhour = 20
    loginmin = 56
    loginsec = 0
    # 预约时间（发包）
    reservehour = 20
    reservemin = 59
    reservesec = 59
    # 预约日期（用于测试）
    # date = '2022-11-12'
    # start_time = '19:50:00'
    # end_time = '22:00:00'
    # seat = 39

    # 真正预约
    date = '2022-11-18'
    start_time = '14:00:00'
    end_time = '22:00:00'
    seat = 39



    while True:
        current_time = time.localtime(time.time())
        print('当前时间：', datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f'))
        # 到点登录
        if ((current_time.tm_hour == loginhour) and (current_time.tm_min == loginmin) and (current_time.tm_sec == loginsec)):
            break
        time.sleep(0.5)

    print('正在启动driver')
    server = Server(r"/home/ubuntu/get-sit/browsermob-proxy-2.1.4/bin/browsermob-proxy")
    server.start()
    proxy = server.create_proxy()
    edge_options = Options()
    edge_options.add_argument('--proxy-server={0}'.format(proxy.proxy))
    edge_options.add_argument('--headless')
    edge_options.add_argument('--no-sandbox')
    edge_options.add_argument('--disable-gpu')
    edge_options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Edge(options=edge_options)
    # driver.implicitly_wait(20)
    shui()
    print('driver已启动')

    proxy.new_har('library', options={'captureHeaders' : True, 'captureContent' : True})
    
    driver.get(url=url)
    # driver.implicitly_wait(20)
    shui()
    print(driver.title)
    print('正在输入账号密码')

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

    thread1 = myThread(1, posturl, header, postData)
    thread2 = myThread(2, posturl, header, postData)
    thread3 = myThread(3, posturl, header, postData)
    thread4 = myThread(4, posturl, header, postData)
    thread5 = myThread(5, posturl, header, postData)
    thread6 = myThread(6, posturl, header, postData)
    thread7 = myThread(7, posturl, header, postData)
    thread8 = myThread(8, posturl, header, postData)
    thread9 = myThread(9, posturl, header, postData)
    thread10 = myThread(10, posturl, header, postData)
    thread11 = myThread(11, posturl, header, postData)
    thread12 = myThread(12, posturl, header, postData)
    thread13 = myThread(13, posturl, header, postData)
    thread14 = myThread(14, posturl, header, postData)
    thread15 = myThread(15, posturl, header, postData)
    thread16 = myThread(16, posturl, header, postData)
    thread17 = myThread(17, posturl, header, postData)
    thread18 = myThread(18, posturl, header, postData)
    thread19 = myThread(19, posturl, header, postData)
    thread20 = myThread(20, posturl, header, postData)
    thread21 = myThread(21, posturl, header, postData)
    thread22 = myThread(22, posturl, header, postData)
    thread23 = myThread(23, posturl, header, postData)
    thread24 = myThread(24, posturl, header, postData)
    thread25 = myThread(25, posturl, header, postData)
    thread26 = myThread(26, posturl, header, postData)
    thread27 = myThread(27, posturl, header, postData)
    thread28 = myThread(28, posturl, header, postData)
    thread29 = myThread(29, posturl, header, postData)
    thread30 = myThread(30, posturl, header, postData)
    thread31 = myThread(31, posturl, header, postData)
    thread32 = myThread(32, posturl, header, postData)
    thread33 = myThread(33, posturl, header, postData)
    thread34 = myThread(34, posturl, header, postData)
    thread35 = myThread(35, posturl, header, postData)
    thread36 = myThread(36, posturl, header, postData)
    thread37 = myThread(37, posturl, header, postData)
    thread38 = myThread(38, posturl, header, postData)
    thread39 = myThread(39, posturl, header, postData)
    thread40 = myThread(40, posturl, header, postData)
    thread41 = myThread(41, posturl, header, postData)
    thread42 = myThread(42, posturl, header, postData)
    thread43 = myThread(43, posturl, header, postData)
    thread44 = myThread(44, posturl, header, postData)
    thread45 = myThread(45, posturl, header, postData)
    thread46 = myThread(46, posturl, header, postData)
    thread47 = myThread(47, posturl, header, postData)
    thread48 = myThread(48, posturl, header, postData)
    thread49 = myThread(49, posturl, header, postData)
    thread50 = myThread(50, posturl, header, postData)
    thread51 = myThread(51, posturl, header, postData)
    thread52 = myThread(52, posturl, header, postData)
    thread53 = myThread(53, posturl, header, postData)
    thread54 = myThread(54, posturl, header, postData)
    thread55 = myThread(55, posturl, header, postData)
    thread56 = myThread(56, posturl, header, postData)
    thread57 = myThread(57, posturl, header, postData)
    thread58 = myThread(58, posturl, header, postData)
    thread59 = myThread(59, posturl, header, postData)
    thread60 = myThread(60, posturl, header, postData)
    thread61 = myThread(61, posturl, header, postData)
    thread62 = myThread(62, posturl, header, postData)
    thread63 = myThread(63, posturl, header, postData)
    thread64 = myThread(64, posturl, header, postData)
    thread65 = myThread(65, posturl, header, postData)
    thread66 = myThread(66, posturl, header, postData)
    thread67 = myThread(67, posturl, header, postData)
    thread68 = myThread(68, posturl, header, postData)
    thread69 = myThread(69, posturl, header, postData)
    thread70 = myThread(70, posturl, header, postData)
    thread71 = myThread(71, posturl, header, postData)
    thread72 = myThread(72, posturl, header, postData)
    thread73 = myThread(73, posturl, header, postData)
    thread74 = myThread(74, posturl, header, postData)
    thread75 = myThread(75, posturl, header, postData)
    thread76 = myThread(76, posturl, header, postData)
    thread77 = myThread(77, posturl, header, postData)
    thread78 = myThread(78, posturl, header, postData)
    thread79 = myThread(79, posturl, header, postData)
    thread80 = myThread(80, posturl, header, postData)
    thread81 = myThread(81, posturl, header, postData)
    thread82 = myThread(82, posturl, header, postData)
    thread83 = myThread(83, posturl, header, postData)
    thread84 = myThread(84, posturl, header, postData)
    thread85 = myThread(85, posturl, header, postData)
    thread86 = myThread(86, posturl, header, postData)
    thread87 = myThread(87, posturl, header, postData)
    thread88 = myThread(88, posturl, header, postData)
    thread89 = myThread(89, posturl, header, postData)
    thread90 = myThread(90, posturl, header, postData)
    thread91 = myThread(91, posturl, header, postData)
    thread92 = myThread(92, posturl, header, postData)
    thread93 = myThread(93, posturl, header, postData)
    thread94 = myThread(94, posturl, header, postData)
    thread95 = myThread(95, posturl, header, postData)
    thread96 = myThread(96, posturl, header, postData)
    thread97 = myThread(97, posturl, header, postData)
    thread98 = myThread(98, posturl, header, postData)
    thread99 = myThread(99, posturl, header, postData)
    thread100 = myThread(100, posturl, header, postData)




    while True:

        current_time = time.localtime(time.time())
        print('当前时间：', datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f'))
        if ((current_time.tm_hour == reservehour) and (current_time.tm_min == reservemin) and (current_time.tm_sec == reservesec)):
            break
        time.sleep(0.05)

    # time.sleep(0.5)
    # thread1.start()
    # time.sleep(0.02)
    # thread2.start()
    # time.sleep(0.02)
    # thread3.start()
    # time.sleep(0.02)
    # thread4.start()
    # time.sleep(0.02)
    # thread5.start()
    # thread1.join()
    # thread2.join()
    # thread3.join()
    # thread4.join()
    # thread5.join()
    thread1.start()
    time.sleep(0.02)
    thread2.start()
    time.sleep(0.02)
    thread3.start()
    time.sleep(0.02)
    thread4.start()
    time.sleep(0.02)
    thread5.start()
    time.sleep(0.02)
    thread6.start()
    time.sleep(0.02)
    thread7.start()
    time.sleep(0.02)
    thread8.start()
    time.sleep(0.02)
    thread9.start()
    time.sleep(0.02)
    thread10.start()
    time.sleep(0.02)
    thread11.start()
    time.sleep(0.02)
    thread12.start()
    time.sleep(0.02)
    thread13.start()
    time.sleep(0.02)
    thread14.start()
    time.sleep(0.02)
    thread15.start()
    time.sleep(0.02)
    thread16.start()
    time.sleep(0.02)
    thread17.start()
    time.sleep(0.02)
    thread18.start()
    time.sleep(0.02)
    thread19.start()
    time.sleep(0.02)
    thread20.start()
    time.sleep(0.02)
    thread21.start()
    time.sleep(0.02)
    thread22.start()
    time.sleep(0.02)
    thread23.start()
    time.sleep(0.02)
    thread24.start()
    time.sleep(0.02)
    thread25.start()
    time.sleep(0.02)
    thread26.start()
    time.sleep(0.02)
    thread27.start()
    time.sleep(0.02)
    thread28.start()
    time.sleep(0.02)
    thread29.start()
    time.sleep(0.02)
    thread30.start()
    time.sleep(0.02)
    thread31.start()
    time.sleep(0.02)
    thread32.start()
    time.sleep(0.02)
    thread33.start()
    time.sleep(0.02)
    thread34.start()
    time.sleep(0.02)
    thread35.start()
    time.sleep(0.02)
    thread36.start()
    time.sleep(0.02)
    thread37.start()
    time.sleep(0.02)
    thread38.start()
    time.sleep(0.02)
    thread39.start()
    time.sleep(0.02)
    thread40.start()
    time.sleep(0.02)
    thread41.start()
    time.sleep(0.02)
    thread42.start()
    time.sleep(0.02)
    thread43.start()
    time.sleep(0.02)
    thread44.start()
    time.sleep(0.02)
    thread45.start()
    time.sleep(0.02)
    thread46.start()
    time.sleep(0.02)
    thread47.start()
    time.sleep(0.02)
    thread48.start()
    time.sleep(0.02)
    thread49.start()
    time.sleep(0.02)
    thread50.start()
    time.sleep(0.02)
    thread51.start()
    time.sleep(0.02)
    thread52.start()
    time.sleep(0.02)
    thread53.start()
    time.sleep(0.02)
    thread54.start()
    time.sleep(0.02)
    thread55.start()
    time.sleep(0.02)
    thread56.start()
    time.sleep(0.02)
    thread57.start()
    time.sleep(0.02)
    thread58.start()
    time.sleep(0.02)
    thread59.start()
    time.sleep(0.02)
    thread60.start()
    time.sleep(0.02)
    thread61.start()
    time.sleep(0.02)
    thread62.start()
    time.sleep(0.02)
    thread63.start()
    time.sleep(0.02)
    thread64.start()
    time.sleep(0.02)
    thread65.start()
    time.sleep(0.02)
    thread66.start()
    time.sleep(0.02)
    thread67.start()
    time.sleep(0.02)
    thread68.start()
    time.sleep(0.02)
    thread69.start()
    time.sleep(0.02)
    thread70.start()
    time.sleep(0.02)
    thread71.start()
    time.sleep(0.02)
    thread72.start()
    time.sleep(0.02)
    thread73.start()
    time.sleep(0.02)
    thread74.start()
    time.sleep(0.02)
    thread75.start()
    time.sleep(0.02)
    thread76.start()
    time.sleep(0.02)
    thread77.start()
    time.sleep(0.02)
    thread78.start()
    time.sleep(0.02)
    thread79.start()
    time.sleep(0.02)
    thread80.start()
    time.sleep(0.02)
    thread81.start()
    time.sleep(0.02)
    thread82.start()
    time.sleep(0.02)
    thread83.start()
    time.sleep(0.02)
    thread84.start()
    time.sleep(0.02)
    thread85.start()
    time.sleep(0.02)
    thread86.start()
    time.sleep(0.02)
    thread87.start()
    time.sleep(0.02)
    thread88.start()
    time.sleep(0.02)
    thread89.start()
    time.sleep(0.02)
    thread90.start()
    time.sleep(0.02)
    thread91.start()
    time.sleep(0.02)
    thread92.start()
    time.sleep(0.02)
    thread93.start()
    time.sleep(0.02)
    thread94.start()
    time.sleep(0.02)
    thread95.start()
    time.sleep(0.02)
    thread96.start()
    time.sleep(0.02)
    thread97.start()
    time.sleep(0.02)
    thread98.start()
    time.sleep(0.02)
    thread99.start()
    time.sleep(0.02)
    thread100.start()
    time.sleep(0.02)
    thread1.join()
    thread2.join()
    thread3.join()
    thread4.join()
    thread5.join()
    thread6.join()
    thread7.join()
    thread8.join()
    thread9.join()
    thread10.join()
    thread11.join()
    thread12.join()
    thread13.join()
    thread14.join()
    thread15.join()
    thread16.join()
    thread17.join()
    thread18.join()
    thread19.join()
    thread20.join()
    thread21.join()
    thread22.join()
    thread23.join()
    thread24.join()
    thread25.join()
    thread26.join()
    thread27.join()
    thread28.join()
    thread29.join()
    thread30.join()
    thread31.join()
    thread32.join()
    thread33.join()
    thread34.join()
    thread35.join()
    thread36.join()
    thread37.join()
    thread38.join()
    thread39.join()
    thread40.join()
    thread41.join()
    thread42.join()
    thread43.join()
    thread44.join()
    thread45.join()
    thread46.join()
    thread47.join()
    thread48.join()
    thread49.join()
    thread50.join()
    thread51.join()
    thread52.join()
    thread53.join()
    thread54.join()
    thread55.join()
    thread56.join()
    thread57.join()
    thread58.join()
    thread59.join()
    thread60.join()
    thread61.join()
    thread62.join()
    thread63.join()
    thread64.join()
    thread65.join()
    thread66.join()
    thread67.join()
    thread68.join()
    thread69.join()
    thread70.join()
    thread71.join()
    thread72.join()
    thread73.join()
    thread74.join()
    thread75.join()
    thread76.join()
    thread77.join()
    thread78.join()
    thread79.join()
    thread80.join()
    thread81.join()
    thread82.join()
    thread83.join()
    thread84.join()
    thread85.join()
    thread86.join()
    thread87.join()
    thread88.join()
    thread89.join()
    thread90.join()
    thread91.join()
    thread92.join()
    thread93.join()
    thread94.join()
    thread95.join()
    thread96.join()
    thread97.join()
    thread98.join()
    thread99.join()
    thread100.join()

    time.sleep(1)
    proxy.close()
    server.stop()
    
if __name__ == '__main__':
    main()
