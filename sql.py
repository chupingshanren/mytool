# -*- coding:utf-8 -*-
from bs4 import BeautifulSoup
import requests
import re
import pandas as pd
import pymysql
from multiprocessing import Pool
import time
import os



def mksql():
    print('连接到mysql服务器...')
    conn = pymysql.Connect(host='127.0.0.1', port=3306,user='root', passwd='1234', db='save',charset='utf8')
    print('连接上了!')
    cur = conn.cursor()
    #判断表是否存在，若存在则删除此表
    cur.execute("DROP TABLE IF EXISTS wyyslist")
#创建表
    sql = """CREATE TABLE wyyslist(
                 class  CHAR(20),
                 list  CHAR(80),
                 num   CHAR(20),
                 listlink   CHAR(120),
                 music   CHAR(120),
                 musiclink   CHAR(120))"""
    cur.execute(sql)
    conn.commit()
    
def editsql(i):
    #print('连接到mysql服务器...')
    conn = pymysql.Connect(host='127.0.0.1', port=3306,user='root', passwd='1234', db='save',charset='utf8')
    #print('连接上了!')
    cur = conn.cursor()
    data = pd.read_csv(i) 
    list=data.values.tolist()
    for name,list,num,listlink,music,musiclink in list:
        sql = "INSERT INTO wyyslist(class,list,num,listlink,music,musiclink) VALUES ( '%s', '%s', '%s','%s','%s','%s' )"  #插入数据 sql = "UPDATE money SET saving = %.2f WHERE account = '%s' "修改数据
        llist = re.sub(r'[^\u4e00-\u9fa5a-zA-Z0-9]','', list)
        cur.execute(sql % (name,llist,num,listlink,music,musiclink))
    conn.commit()
    #print('成功插入', cur.rowcount, '条数据')
    conn.close()

def selsql():
    print('连接到mysql服务器...')
    conn = pymysql.Connect(host='127.0.0.1', port=3306,user='root', passwd='1234', db='save',charset='utf8')
    print('连接上了!')
    cur = conn.cursor()
    sql = "SELECT music,musiclink FROM wyylist WHERE class = '%s' "#查询 sql = "DELETE FROM money  WHERE account = '%s' LIMIT %d"
    data = ('影视原声')
    cur.execute(sql % data)
    for row in cur.fetchall():
        print("music:%s\tmusiclink:%s" % row)
    print('共查找出', cur.rowcount, '条数据')
    cur.close()
    conn.close()



def mycallback(x):
    with open('123.txt', 'a+') as f:
        f.writelines(str(x))


def sayHi(num):
    return num




if __name__ == '__main__':
    filedir = r"C:\Users\22129\mytool\lis\list"
    mksql()
    #获取目标文件夹的路径
    #获取当前文件夹中的文件名称列表  

    filenames=os.listdir(filedir)
    lists = []
    for filename in filenames:
        filepath = filedir+'\\'+filename
        lists.append(filepath)
        
    pool = Pool()        
    for i in lists:
        #pool.apply_async(sayHi, (i,), callback=editsql)

    #pool.close()
    #pool.join()
        editsql(i)



    


    #os.mkdir(r'C:\Users\22129\mytool\lis\list' )


    #task_start(lists) 
    #print('finish')  
#mksql()
#selsql()

