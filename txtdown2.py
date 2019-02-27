# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
import urllib.request
from urllib import error
import sys

novel_url = "https://www.biqukan.com/53_53586/"  # 小说页面地址
base_url = "https://www.biqukan.com"  # 根地址，用于拼接

save_dir = "Novel/"  # 下载小说的存放路径
#    for txt in showtxt:
#        with open('a.txt', "a+",encoding='utf-8') as f:
#            for text in txt.stripped_strings:
#                f.write('\000\000\000\000\000\000\000'+text+'\ncuiweijuxing')



# 保存小说到本地
def save_chapter(txt, path,chapter_name):
    try:
        with open(path, "a+",encoding='utf-8') as f:
            f.wirte(chapter_name+'\n')
            f.write(txt.get_text(strip=True))
    except (error.HTTPError, OSError) as reason:
        print(str(reason))
    else:
        print("下载完成：" + path)


# 获得所有章节的url
def get_chapter_url():
    chapter_req = urllib.request.Request(novel_url)
    chapter_resp = urllib.request.urlopen(chapter_req, timeout=20)
    chapter_content = chapter_resp.read()
    chapter_soup = BeautifulSoup(chapter_content, 'html.parser')
    # 取出章节部分
    listmain = chapter_soup.find_all(attrs={'class': 'listmain'})                          #此处填写章节部分标签
    a_list = []  # 存放小说所有的a标签
    # 过滤掉不是a标签的数据
    for i in listmain:
        if 'a' not in str(i):
            continue
        for d in i.findAll('a'):
            a_list.append(d)
    #过滤掉前面"最新章节列表"部分
    #result_list = a_list
    result_list = a_list[12:]
    return result_list


# 获取章节内容并下载
def get_chapter_content(c):
    chapter_url = base_url + c.attrs.get('href')  # 获取url
    count = 0
#    chapter_url = c.attrs.get('href')
    chapter_name = c.string  # 获取章节名称
    print(c.string)
    chapter_req = urllib.request.Request(chapter_url)
    chapter_resp = urllib.request.urlopen(chapter_req, timeout=20)
    chapter_content = chapter_resp.read()
    chapter_soup = BeautifulSoup(chapter_content, 'html.parser')
    # 查找章节部分内容
    showtxt = chapter_soup.find_all(attrs={'class': 'showtxt'})                           #此处填写内容部分标签
    for txt in showtxt:
        try:
            with open(save_dir+'大医凌然.txt', "a+",encoding='utf-8') as f:               #此处填写书名
                f.write(chapter_name+'\n')
                for text in txt.stripped_strings:
                    f.write('\000\000\000\000\000\000\000'+text+'\n')
        except (error.HTTPError, OSError) as reason:
            print(str(reason))
    count+=1
    if count%10 == 0:
        proxy_list = []
        with open('availableIP.txt','r') as f:
            for line in f:
                proxy_list.append(list(line.strip('\n').split(',')))
        proxy_ip = random.choice(proxy_list) 
        proxy = {'http': proxy_ip} 
        handler = urllib.request.ProxyHandler(proxy)
        opener = urllib.request.build_opener(handler)
        urllib.request.install_opener(opener)


if __name__ == '__main__':
    novel_list = get_chapter_url()
    for chapter in novel_list:
        get_chapter_content(chapter)
    print("下载完成：" )


