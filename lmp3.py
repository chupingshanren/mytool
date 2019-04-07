import csv
import pandas as pd
import os
import re
from subprocess import call

i = r"C:\Users\22129\mytool\lis\list\(14360万)欧美网易云热歌热评10w持续更新.csv"
lists =[]
data = pd.read_csv(i) 
path = 'C:\\Users\\22129\\mytool\\Music\\'
nnum = 'q'
llist = ''
list=data.values.tolist()
for name,list,num,listlink,music,musiclink in list:
            llist = re.sub(r'[^\u4e00-\u9fa5a-zA-Z0-9]','', list)
            list = []
            nnum = num
            list.append(musiclink)
            list.append(music)
            lists.append(list)
path = path+'('+num+')'+llist
os.mkdir(path)
IDM = r'C:\Program Files (x86)\Internet Download Manager\IDMan.exe'
DownPath = r'C:\Users\22129\mytool\Music\周杰伦'
for list in lists:
    call([IDM, '/d',list[0], '/p',path, '/f', list[1]+'.mp3', '/n', '/a'])
    print('add'+list[1])
print('开始')
call([IDM, '/s'])

    
