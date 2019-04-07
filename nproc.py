#-*- coding=utf-8 -*-
import requests
from multiprocessing import Process
import gevent
from gevent import monkey
import sys
import pandas as pd
from selenium import webdriver
import csv
import time
import os
from bs4 import BeautifulSoup
import urllib.request
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
    for i in range(len(lists)):
        i_list.append(lists[i])
        if (i+1)%1 == 0 or i == len(lists)-1:
            p = Process(target=process_start,args=(i_list,))
            p.start()
            i_list = []
            #p.join()
            
            #process_start(i_list)
            
def listd(i):
    MAX_RETRIES = 20
    headers = {
    'Referer':'http://music.163.com/',
    'Host':'music.163.com',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.75 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    }
 
# 歌单的url地址 
    path = r'C:\Users\22129\mytool\lis\list'      
    data = pd.read_csv(i[1]) 
    list=data.values.tolist()
    listname = i[0]
    listname = listname[:-4]
    #os.mkdir(path)
    for name,num,url in list:
        lname = re.sub(r'[^\u4e00-\u9fa5a-zA-Z0-9]','', name)
 # 获取页面内容
        with requests.session() as session:
            adapter = requests.adapters.HTTPAdapter(max_retries=MAX_RETRIES)
            session.mount('https://', adapter)
            session.mount('http://', adapter)
            response=session.get(url,headers = headers).content
 
#使用bs4匹配出对应的歌曲名称和地址
            s = BeautifulSoup(response,'lxml')
            main = s.find('ul',{'class':'f-hide'}) 
            lists=[]
            csv_file = open(path+'\\('+num+')'+listname+lname+".csv","w",encoding='utf-8',newline='')
            writer = csv.writer(csv_file)
            writer.writerow(['class','list','num','listlink','music','musiclink'])
            for music in main.find_all('a'):
    # print('{} : {}'.format(music.text, music['href']))
                musicUrl='http://music.163.com/song/media/outer/url'+music['href'][5:]+'.mp3'
                musicName=music.text
                musicName = re.sub(r'[^\u4e00-\u9fa5a-zA-Z0-9]','', musicName)
    # 单首歌曲的名字和地址放在list列表中
                writer.writerow([listname,name,num,url,musicName,musicUrl])
            csv_file.close()

    
if __name__ == '__main__':
    filedir = r"C:\Users\22129\mytool\list"
    #获取目标文件夹的路径
    #获取当前文件夹中的文件名称列表  
    filenames=os.listdir(filedir)
    lists = []
    for filename in filenames:
        filepath = filedir+'\\'+filename
        list = []
        list.append(filename)
        list.append(filepath)
        lists.append(list)
    #os.mkdir(r'C:\Users\22129\mytool\lis\list' )


    task_start(lists) 
    print('finish')    