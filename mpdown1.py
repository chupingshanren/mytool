# 导入驱动包
import json
import os
import pickle
import platform
import time
import urllib
from _sha1 import sha1

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver import DesiredCapabilities, ActionChains

import requests
from bs4 import BeautifulSoup
import urllib.request

def driver_set():
    # 浏览器请求头
    headers = {'Accept': '*/*',
               'Accept-Language': 'en-US,en;q=0.8',
               'Cache-Control': 'max-age=0',
               'User-Agent': 'Mozilla/5.0 (Linux; U; Android 2.3.6; zh-cn; GT-S5660 Build/GINGERBREAD) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1 MicroMessenger/4.5.255',
               'Connection': 'keep-alive', }
    desired_capabilities = DesiredCapabilities.PHANTOMJS.copy()
    for key, value in headers.items():
        desired_capabilities['phantomjs.page.customHeaders.{}'.format(key)] = value
    # 禁止加载图片
    desired_capabilities["phantomjs.page.settings.loadImages"] = False
    driver = webdriver.PhantomJS(desired_capabilities=desired_capabilities)
    # 设置屏幕大小
    driver.set_window_size(1366, 631)
    # 开始请求qzone
    driver.get('http://music.wandhi.com/')
    return driver

def download(driver,name,num):

    mname = name
    num = num
    input = driver.find_element_by_xpath('//*[@id="j-input"]')
    name = driver.find_element_by_xpath('//*[@id="j-nav"]/li[1]/a')
    id = driver.find_element_by_xpath('//*[@id="j-nav"]/li[2]/a')
    add = driver.find_element_by_xpath('//*[@id="j-nav"]/li[3]/a')
    get = driver.find_element_by_xpath('//*[@id="j-submit"]')

    # 移动
    action = ActionChains(driver)
    if num != None:
        vau = driver.find_element_by_xpath('//*[@id="j-type"]/label['+str(num)+']')
        action.move_to_element(vau)
        action.click(vau)
        action.perform()
    action.move_to_element(input)
    action.click(input)
    # 模仿键盘输入
    action.send_keys(mname)

    # 点击
    action.move_by_offset(get.location['x'], get.location['y'])
    action.click(get)

    # 执行
    action.perform()
    time.sleep(3)
    for i in range(3):
        try :
            down_url = driver.find_element_by_xpath('//*[@id="j-src-btn"]')
            url = down_url.get_attribute('href')
        except:
		    # 休息5秒保证能执行
            time.sleep(5)
    driver.get('http://music.wandhi.com/')
    return url


def ask():
    yn = input('是否选择音乐平台?y or n')
    if yn == 'y':
        print('1.网易\n2.qq\n3.酷狗\n4.酷我\n5.虾米\n6.百度\n7.一听\n8.咪咕\n9.荔枝\n10.蜻蜓\n11.喜马拉雅\n12.全民k歌\n13.5sing原创\n14.5sing翻唱\n')
        inp = input('输入')
        try:
            if int(inp)<15 and int(inp)>0:
                num = inp
            else:
                num = None 
        except:
            print('error')
    else:
        num = None
    return num
    

num = ask()
name = input("输入exit结束\n输入s截屏\n输入歌名：")	
driver = driver_set()
while(1):
    if name == 'exit':
        driver.quit()
        try:
            os.remove('screenshot.png')
        except:
            print('结束')
        exit()
    elif name == 's':
        driver.save_screenshot('screenshot.png')
    else:
        url = download(driver,name,num)
        try:
            print('正在下载',name)
            urllib.request.urlretrieve(url,'./'+name+'.mp3')
            print('下载成功')
        except:
            print('下载失败')
    num = ask()
    name = input("输入exit结束\n输入s截屏\n输入歌名：")
    
