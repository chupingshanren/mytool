# 导入驱动包下载周杰伦音乐
import json
import os
import pickle
import platform
import time
import urllib
from _sha1 import sha1
from subprocess import call

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver import DesiredCapabilities, ActionChains

import requests
from bs4 import BeautifulSoup
import urllib.request

def driver_set():
    driver = webdriver.Chrome()
    # 开始请求qzone
    driver.get('http://www.zhmdy.top/music/?name=%E5%91%A8%E6%9D%B0%E4%BC%A6&type=qq')
    time.sleep(5)
    action = ActionChains(driver)
    for i in range(13):
        for j in range(3):
            try:
                more = driver.find_element_by_xpath('//*[@id="j-player"]/div[4]')
                action.click(more).perform()
                time.sleep(5)
                break
            except:
		    # 休息5秒保证能执行
                time.sleep(5)
    return driver

def down(driver):
    lists = []
    action = ActionChains(driver)
    #driver.save_screenshot('screenshot1.png')
    #data = driver.find_element_by_xpath('//*[@id="j-player"]/div[3]/ol')//*[@id="j-player"]/div[3]/ol/li[49]/span[3]
    data = driver.find_elements_by_xpath("//span[contains(@class,'aplayer-list-title')]")  
    for i in range(len(data)):
        list = []
        i += 1
        music = driver.find_element_by_xpath("//*[@id='j-player']/div[3]/ol/li["+str(i)+"]/span[3]")
        name = music.text
        print(name)
        action.click(music).perform()
        #action.click(music)

        #driver.save_screenshot(name+'.png')
        time.sleep(2)
        down_url = driver.find_element_by_xpath('//*[@id="j-src-btn"]')
        url = down_url.get_attribute('href')
        list.append(url)
        list.append(name)
        lists.append(list)
    return lists

def download(driver,name,num):



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
    

	
driver = driver_set()
#driver.save_screenshot('screenshot.png')
lists = down(driver)
IDM = r'C:\Program Files (x86)\Internet Download Manager\IDMan.exe'
DownPath = r'C:\Users\22129\mytool\Music\周杰伦'
for list in lists:
    call([IDM, '/d',list[0], '/p',DownPath, '/f', list[1], '/n', '/a'])
    print('add'+list[1])
print('开始')
call([IDM, '/s'])

    
