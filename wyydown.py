# 导入驱动包
import json
import os
import pickle
import platform
import time
import urllib
import pandas as pd
from _sha1 import sha1

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver import DesiredCapabilities, ActionChains

import requests
from bs4 import BeautifulSoup
import urllib.request

def driver_set(i):
    name = i[0]
    url = i[1]
    driver = webdriver.Chrome()
    driver.get('url')
    #return driver
    down_url = driver.find_element_by_xpath('/html/body/video/source')
    url = down_url.get_attribute('href')
    try:
        print('正在下载',name)
        urllib.request.urlretrieve(url,'./'+name+'.mp3')
        print('下载成功')
    except:
        print('下载失败')

if __name__ == '__main__':
    with pd.read_csv(i) as data:
        list=data.values.tolist()
    for i in list:
        driver_set(i)