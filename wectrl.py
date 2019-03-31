#微信简单控制电脑
# coding=utf-8
import itchat
import os
import cv2
from PIL import ImageGrab

usageMsg = u"使用方法：\n1.运行CMD命令：cmd xxx (xxx为命令)\n" \
           u"例如关机命令:\ncmd shutdown -s -t 0 \n" \
           u"2.获取摄像头并拍照：cap\n" \
           u"2.获取屏幕截屏：pc\n" \

@itchat.msg_register('Text')
def handler_receive_msg(msg):  # 处理收到的消息
    message = msg['Text']
    toName = msg['ToUserName']
    path = r'C:\Users\22129\mytool'  # 临时保存截屏图片地址
    if toName == "filehelper":
        if message == "cap":  # 拍照
            #  要使用摄像头，需要使用cv2.VideoCapture(0)创建VideoCapture对象，
            # 参数：0指的是摄像头的编号。如果你电脑上有两个摄像头的话，访问第2个摄像头就可以传入1
            cap = cv2.VideoCapture(0)
            ret, img = cap.read()  # 获取一帧
            cv2.imwrite("temp.jpg", img)
            itchat.send('@img@%s' % u'temp.jpg', 'filehelper')
            cap.release()  # 释放资源
        if message[0:3] == "cmd":  # 处理cmd命令
            os.system(message.strip(message[0:4]))
        if message == "pc":  # 截图
            im = ImageGrab.grab()  # 实现截屏功能
            im.save(path, 'JPEG')  # 设置保存路径和图片格式
            itchat.send_image(path, 'filehelper')


if __name__ == '__main__':
    itchat.auto_login()
    itchat.send(usageMsg, "filehelper")
    itchat.run()
