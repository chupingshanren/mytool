#-*- coding=utf-8 -*-
import requests
from multiprocessing import Process
import gevent
from gevent import monkey
import sys
from selenium import webdriver
import csv
import time
import os
import re
monkey.patch_all()

 
def process_start(i_list):
    tasks = []
    for i in i_list:
        tasks.append(gevent.spawn(listd,i))
        #listd(i)
    gevent.joinall(tasks)#使用协程来执行
 
def task_start(lists):#每10W条url启动一个进程
    i_list = []
    for i in range(36,73):
        i_list.append(lists[i])
        if (i+1)%1 == 0 or i == 72:
            p = Process(target=process_start,args=(i_list,))
            i_list = []
            p.start()
            p.join()

            #process_start(i_list)
            



def get_list():
#网易云音乐歌单首页的url
    base = 'https://music.163.com/discover/playlist/?order=hot'

#用PhantomJS接口创建一个Selenium的Webdriver 此方案失败driver = webdriver.PhantomJS()
    #option=webdriver.ChromeOptions()
    #option.add_argument('headless') # 设置
    driver = webdriver.Chrome()
#创建储存歌单的文件
#解析每一页，直到下一页为空
    driver.get(base)
    # 切换到内容的iframe
    driver.switch_to.default_content()
    iframe = None
    iframe = driver.find_element_by_xpath("//iframe[@id='g_iframe']")
    driver.switch_to.frame(iframe)
    #截屏查看driver.save_screenshot('screenshot.png')
    #driver.switch_to.frame("g_iframe")
    #data = driver.find_element_by_xpath("//*[@id="cateListBox"]/div[2]").find_elements_by_tag_name("a")
    data = driver.find_elements_by_xpath("//a[contains(@class,'s-fc1')]")  
    lists = []
    for i in range(len(data)):
        url = data[i].get_attribute('href')  #,
        name = data[i].get_attribute('data-cat')
        list = []
        list.append(name)
        list.append(url)
    # 全部歌曲信息放在lists列表中
        lists.append(list)
    driver.quit()
    return lists
    
def listd(i):
# 使用代理
    #options = webdriver.ChromeOptions()
 
    #options.add_argument("--proxy-server=http://119.102.133.6:9999")
    driver = webdriver.Chrome()

    name = i[0]
    url = i[1]
    name = re.sub(r'[^\u4e00-\u9fa5a-zA-Z0-9]','', name)
    csv_file = open('list/'+name+".csv","w",encoding='utf-8',newline='')
    writer = csv.writer(csv_file)
    writer.writerow(['标题','播放数','链接'])
#解析每一页，直到下一页为空
    while url != 'javascript:void(0)':
        #print(url)
        driver.get(url)
    # 切换到内容的iframe
        driver.switch_to.default_content()
        iframe = None
        iframe = driver.find_element_by_xpath("//iframe[@id='g_iframe']")
        driver.switch_to.frame(iframe)
    #截屏查看driver.save_screenshot('screenshot.png')
    #driver.switch_to.frame("g_iframe")
    # 定位歌单标签
        data = driver.find_element_by_xpath("//ul[@id='m-pl-container']").find_elements_by_tag_name("li")
    #解析每一页的所有歌单
        for i in range(len(data)):
        #获取播放数
            nb = data[i].find_element_by_class_name("nb").text
            if '万' in nb and int(nb.split("万")[0]) > 1000:
            #获取播放数大于1000万的歌单封面
                msk = data[i].find_element_by_css_selector("a.msk")
                tit=msk.get_attribute('title').replace(u'\xa0', u' ')
                ltit = re.sub(r'[^\u4e00-\u9fa5a-zA-Z0-9]','', tit)
            #把封面标题，连接，播放数写到文件
                writer.writerow([tit,nb,msk.get_attribute('href')])
    #定位下一页的url#m-pl-pager > div > a.zbtn.znxt
        #url = driver.find_element_by_css_selector("url#m-pl-pager > div > a.zbtn.znxt").get_attribute('href')
        #url = None
        #try:
        url = driver.find_element_by_link_text('下一页').get_attribute('href')
        #except:
        #    url = None
        #print(driver.find_element_by_link_text('下一页'))
    #try:
    #    next_page = self.driver.find_element_by_link_text('下一页')
    #except:
    #    next_page = None
    csv_file.close()
    driver.quit()

#73
if __name__ == '__main__':
    lists = get_list()  
    #os.mkdir('list')    

    task_start(lists)


