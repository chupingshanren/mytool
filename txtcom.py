#优书网查找小说 未知bug只能爬三页
# 环境python3.5
import requests
from bs4 import BeautifulSoup
import urllib.request
import re
 
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.75 Safari/537.36'
    }
 
# url地址
li_url = 'http://www.yousuu.com'
base_url = 'http://www.yousuu.com/booklist?'
 
# 获取页面内容
url = base_url
while url != None:
    s = requests.session()
    response=s.get(url,headers=headers).content
    #使用bs4匹配出对应的信息
    s = BeautifulSoup(response,'lxml')
    lists=[]
    for main in s.find_all('h4',{'style':'line-height:30px;'}):
        for music in main.find_all('a',{'target':'_blank'}):
            for la in main.find_all('i',{'title':'该书单是精品书单'}):
                list=[]
	        # print('{} : {}'.format(music.text, music['href']))
                listUrl=li_url+music.attrs.get('href')
                listName=music.text
			# 单首歌曲的名字和地址放在list列表中
                list.append(listName)
                list.append(listUrl)
			# 全部歌曲信息放在lists列表中
                lists.append(list)
    #print(lists)
	# 下载列表中的全部歌曲，并以歌曲名命名下载后的文件，文件位置为当前文件夹
	#for i in lists:
	#    url=i[1]
	#	name=i[0]
    with open('list.txt', "a+",encoding='utf-8') as f:
        for i in lists:           
            f.write(i[0]+i[1]+'\n')
            
    try:
	    new = s.find('a',text="下一页")
	    pat2=r"\d+" #进行下一页筛选的正则表达式
	    next = re.compile(pat2).findall(str(new))   #获取下一页地址
	    url = base_url+'t='+next[0]
    except:
        url = None
        print('完')
