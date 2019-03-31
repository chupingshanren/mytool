#由于ajax异步加载爬取空数据bs失败 爬取网易云数据
from selenium import webdriver
import csv
import time
#网易云音乐歌单首页的url
#base = 'http://music.163.com/#/discover/playlist?order=hot&cat=%E5%85%A8%E9%83%A8&limit=35&offset='
base = 'https://music.163.com/#/discover/playlist/?order=hot&cat=%E5%8D%8E%E8%AF%AD&limit=35&offset='
#用PhantomJS接口创建一个Selenium的Webdriver 此方案失败driver = webdriver.PhantomJS()
driver = webdriver.Chrome()
#创建储存歌单的文件
csv_file = open("huaplaylist.csv","w",encoding='utf-8',newline='')
writer = csv.writer(csv_file)
writer.writerow(['标题','播放数','链接'])
url = base + '0'
count = 0
#解析每一页，直到下一页为空
while url != 'javascript:void(0)':
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
            #把封面标题，连接，播放数写到文件
            writer.writerow([tit,nb,msk.get_attribute('href')])
    #定位下一页的url
    #url = driver.find_element_by_css_selector("a.zbtn.znxt").get_attribute('href')
    count+=35
    url = base + str(count)
    #try:
    #    next_page = self.driver.find_element_by_link_text('下一页')
    #except:
    #    next_page = None
csv_file.close()