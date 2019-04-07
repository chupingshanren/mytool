import csv
import pandas as pd
import os
import re

if __name__ == '__main__':
    filedir = r"C:\Users\22129\mytool\lis\list"
    #获取目标文件夹的路径
    #获取当前文件夹中的文件名称列表  

    filenames=os.listdir(filedir)
    lists = []
    for filename in filenames:
        filepath = filedir+'\\'+filename
        lists.append(filepath)
    csv_file = open("all1.csv","w",encoding='utf-8',newline='')
    writer = csv.writer(csv_file)
    writer.writerow(['class','list','num','listlink','music','musiclink'])
    for i in lists:
        #print(i)
        data = pd.read_csv(i) 
        list=data.values.tolist()
        for name,list,num,listlink,music,musiclink in list:
            llist = re.sub(r'[^\u4e00-\u9fa5a-zA-Z0-9]','', list)
            writer.writerow([name,llist,num,listlink,music,musiclink])
    csv_file.close()