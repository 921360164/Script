#!/usr/bin/env python
# -*- coding: utf-8 -*-

from appium import webdriver
from time import sleep
import json
import requests
import rsa
import base64
import time

global lists
lists = []

'''
登录操作
'''
def login(driver):
    if driver is None:
        return
    try:
        loginNode = driver.find_element_by_xpath(
            "//android.widget.ScrollView/android.view.ViewGroup/android.view.ViewGroup[1]/android.widget.EditText")
        loginNode.send_keys("127188")
    except:
        println(u"没有找到登录界面")

'''
主界面操作
'''
def homePage(driver):
    if driver is None:
        return
    try:
        homeNode = driver.find_element_by_xpath("(//android.widget.ImageView[@content-desc=\"iconNoti\"])[2]")
        homeNode.click()
    except:
        println(u"没有找到主界面")

'''
读取详情数据
'''
def readDetail(driver):
    if driver is None:
        return
    titleTxt = None
    try:
        title = driver.find_element_by_xpath("//android.widget.TextView[@content-desc=\"Title\"]")
        titleTxt = title.text.encode('utf-8')
    except:
        println(u"没有找到详情标题")
    if titleTxt is None or "Chi tiết giao dịch" != titleTxt:
        return False
    codeTitle = None
    try:
        codeTitleNode = driver.find_element_by_xpath("//android.widget.ScrollView/android.view.ViewGroup/android.widget.TextView[2]")
        codeTitle = codeTitleNode.text.encode('utf-8')
    except:
        println(u"没有找到code标志")
        return
    if codeTitle is None or "LỜI NHẮN ĐÃ NHẬN" != codeTitle:
        return
    code = None
    try:
        codeNode = driver.find_element_by_xpath(
            "//android.widget.ScrollView/android.view.ViewGroup/android.view.ViewGroup[4]/android.widget.TextView")
        code = codeNode.text.encode('utf-8')
        if len(code) != 8:
            println(u"code长度不对")
            return
    except:
        println(u"没有codeNode")
        return
    money = None
    try:
        moneyNode = driver.find_element_by_xpath(
            "//android.widget.ScrollView/android.view.ViewGroup/android.view.ViewGroup[3]/android.widget.TextView[6]")
        money = moneyNode.text.encode('utf-8')
    except:
        println(u"没有moneyNode")
        return
    order = None
    try:
        orderNode = driver.find_element_by_xpath(
            "//android.widget.ScrollView/android.view.ViewGroup/android.view.ViewGroup[2]/android.widget.TextView[6]")
        order = orderNode.text.encode('utf-8')
    except:
        println(u"没有orderNode")
        return
    println(code + "," + money + "," + order)
    if code is None or money is None or order is None:
        return
    map = {}
    map['amount'] = money[:-2]
    map['code'] = code
    map['orderId'] = order
    if isExists(order) is False:
        lists.append(map)

'''
判断是否存在同样的订单号
'''
def isExists(order = None):
    if order is None:
        return True
    for each in lists:
        if each["orderId"] == order:
            return True
    return False

'''
读取列表数据
'''
def readList(driver):
    if driver is None:
        return
    sleep(1)
    swipeDown(driver)
    k = 1
    m = 1
    while True:
        sleep(2)
        try:
            item = driver.find_element_by_xpath(
                "//android.widget.ScrollView/android.view.ViewGroup/android.view.ViewGroup[" + str(
                    k) + "]/android.view.ViewGroup/android.view.ViewGroup")
            txt = item.find_element_by_xpath("//android.widget.TextView[1]").text
            k += 3
            if "Nhận tiền thành công" != txt.encode('utf-8'):
                println(u"不相等")
                continue
            item.click()
            sleep(1)
            try:
                driver.hide_keyboard()
            except:
                println(u"没有键盘")

            #读取详情数据
            readDetail(driver)

            sleep(1)
            driver.press_keycode(4)
        except:
            m += 1
            k = 1
            println(u"找不到节点")
            if m > 2:
                break
            swipeUp(driver, 2000, 2)
    sleep(2)
    try:
        driver.press_keycode(4)
    except:
        println(u"找不到press_keycode")

'''
向上滑动屏幕
'''
def swipeUp(driver, t = 500, n = 1):
    if driver is None:
        return
    try:
        h = driver.get_window_size()
        x = h['width'] * 0.5
        y1 = h['height'] * 0.6
        y2 = h['height'] * 0.3
        for i in range(n):
            driver.swipe(x, y1, x, y2, t)
    except:
        println(u"找不到driver")

'''
向下滑动屏幕
'''
def swipeDown(driver, t = 500, n = 1):
    if driver is None:
        return
    try:
        h = driver.get_window_size()
        x = h['width'] * 0.5
        y1 = h['height'] * 0.25
        y2 = h['height'] * 0.65
        for i in range(n):
            driver.swipe(x, y1, x, y2, t)
    except:
        println(u"找不到driver")

'''
特殊处理操作
'''
def specialAction(driver):
    if driver is None:
        return
    try:
        validLogin = driver.find_element_by_xpath(
            "//android.widget.FrameLayout/android.view.ViewGroup/android.view.ViewGroup[1]/android.view.ViewGroup[2]" +
                     "/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup/android.widget.TextView")
        txt = validLogin.text
        if "ĐỒNG Ý" == txt.encode('utf-8'):
            println(u"正在处理失效会话")
            validLogin.click()
    except:
        println(u"登录会话没有失效")

'''
开启应用
'''
def startApp():
    desired_caps = {}
    desired_caps['platformName'] = 'Android'  # Android系统 or IOS系统
    # desired_caps['deviceName'] = 'HUAWEI Mate 20 Pro (UD)'  # 真机或模块器名
    desired_caps['deviceName'] = 'HONOR 9X'  # 真机或模块器名
    desired_caps['platformVersion'] = '9'  # Android系统版本
    desired_caps['appPackage'] = 'com.mservice.momotransfer'  # APP包名
    desired_caps['appActivity'] = 'com.mservice.MainActivity'  # APP启动Activity
    desired_caps['automationName'] = 'UIAutomator2'
    desired_caps['noReset'] = True  # 每次打开APP不开启重置，否则每次都进入四个欢迎页
    desired_caps['resetKeyboard'] = True  # 隐藏键盘
    desired_caps['newCommandTimeout'] = 60 * 30
    lists = []
    driver = webdriver.Remote('http://127.0.0.1:4723/wd/hub', desired_caps)
    driver.implicitly_wait(8)
    return driver

'''
核心流程
'''
def core():
    while True:
        # 重启App
        driver = None
        try:
            driver = startApp()
        except:
            println(u"创建driver失败")

        sleep(1)
		
        #登录
        login(driver)

        sleep(10)

        #首页点击操作
        homePage(driver)

        sleep(1)

        # 读取列表
        readList(driver)

        try:
            #网络请求
            httpRequest()
        except:
            println(u"网络请求发生异常")

        sleep(1)
        driver.close()
        driver.quit()
        println(u"====延时等待中====")
        sleep(5)

        lists = []

    sleep(2)

    println(u"退出应用程序")
    try:
        driver.quit()
    except:
        println(u"找不到quit")

''''
网络请求
'''
def httpRequest():
    if len(lists) is False:
        println(u"本次请求没有爬取到数据")
    println(u"本次请求爬取到的数据：" + str(lists))
    with open('private_key.pem', 'r') as f:
        privateKey = rsa.PrivateKey.load_pkcs1(f.read().encode())
    # url = 'http://10.45.0.12:9114/recharge/momo/autoConfirm'
    url = 'http://service.skinsnb.com/recharge/momo/autoConfirm'
    body = {}
    data = json.dumps(lists)
    secret = base64.b64encode(rsa.sign(data, privateKey, 'SHA-256'))
    body['sign'] = secret
    body['data'] = data
    headers = {'content-type' : 'application/json'}
    response = requests.post(url, data=json.dumps(body), headers=headers)
    println(u"接口请求结果：" + response.text.encode('utf-8'))

'''
获取当前时间
'''
def getTime():
    now = int(time.time())
    return time.strftime("%Y%m%d %H:%M:%S", time.localtime(now))

'''
打印日志
'''
def println(dataString):
    print (getTime() + dataString)

if __name__ == "__main__":
    core()