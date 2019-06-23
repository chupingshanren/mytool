import requests
from lxml import etree
from urllib import parse
import httplib2
import smtplib
from email.mime.text import MIMEText
#from twilio.rest import Client

def get_text():
    url = "http://www.tianqi.com/wuhan/life.html"
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'}
    response = requests.get(url=url,headers=headers)
 
    html = response.text
    html_xpath = etree.HTML(html)
 
 
    rain = html_xpath.xpath('/html/body/div[4]/div[1]/ul/li[1]/p/text()')[0]
    clothes = html_xpath.xpath('/html/body/div[4]/div[1]/ul/li[6]/p/text()')[0]
    ziwaixian = html_xpath.xpath('/html/body/div[4]/div[1]/ul/li[3]/p/text()')[0]
    travel = html_xpath.xpath('/html/body/div[4]/div[1]/ul/li[7]/p/text()')[0]
    shaiyifu = html_xpath.xpath('/html/body/div[4]/div[1]/ul/li[8]/p/text()')[0]
 
    url2 = "http://www.tianqi.com/wuhan/"
    response2 = requests.get(url=url2,headers=headers)
    html2 = response2.text
    html_xpath2 = etree.HTML(html2)
    wendu = html_xpath2.xpath('/html/body/div[5]/div/div[1]/dl/dd[3]/p/b/text()')[0]
    shidu = html_xpath2.xpath('/html/body/div[5]/div/div[1]/dl/dd[4]/b[1]/text()')[0]
    fengxiang = html_xpath2.xpath('/html/body/div[5]/div/div[1]/dl/dd[4]/b[2]/text()')[0]
    tianqi = html_xpath2.xpath('/html/body/div[5]/div/div[1]/dl/dd[3]/span/b/text()')[0]
    wen = html_xpath2.xpath('/html/body/div[5]/div/div[1]/dl/dd[3]/span/text()')[0]
    text = '\n' + "今日天气：" + tianqi +'\n' + '今日温度：' + wen +'\n' + '当前温度：' + wendu +'℃' + '\n' + shidu +'\n' + fengxiang +'\n' + rain +'\n' + clothes + '\n' + ziwaixian + '\n' + travel + '\n' + shaiyifu
    return text

def send_pas(mobile,info):
    # Your Account SID from twilio.com/console
    account_sid = "ACaac74d942a0084979a3d8c22d1b84ed4"
    # Your Auth Token from twilio.com/console
    auth_token  = "b2f84f0d5b15be25bc4f44841782c4d6"
    client = Client(account_sid, auth_token)
    mobile = "+86"+str(mobile)
    message = client.messages.create(
        to=mobile, 
        from_="+12028318916",
        body=info)


def send_sms(mobile, sms_info):
        """发送手机通知短信，用的是-互亿无线-的测试短信"""
        host = "106.ihuyi.com"
        sms_send_uri = "/webservice/sms.php?method=Submit"
        account = "C59782899"
        pass_word = "19d4d9c0796532c7328e8b82e2812655"
        params = parse.urlencode(
            {'account': account, 'password': pass_word, 'content': sms_info, 'mobile': mobile, 'format': 'json'}
        )
        headers = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain"}
        conn = httplib2.HTTPConnectionWithTimeout(host, port=80, timeout=30)
        conn.request("POST", sms_send_uri, params, headers)
        response = conn.getresponse()
        response_str = response.read()
        conn.close()
        return response_str    

def send_mail(receiver_address, content):
        """发送邮件通知"""
        # 连接邮箱服务器信息
        host = 'smtp.163.com'
        port = 25
        sender = 'tazhe4213@163.com'  # 你的发件邮箱号码
        pwd = 'zixu19980510'  # 不是登陆密码，是客户端授权密码
        # 发件信息
        receiver = receiver_address
        body = '<h2>温馨提醒：</h2><p>' + content + '</p>'
        msg = MIMEText(body, 'html', _charset="utf-8")
        msg['subject'] = '抢票成功通知！'
        msg['from'] = sender
        msg['to'] = receiver
        s = smtplib.SMTP(host, port)
        # 开始登陆邮箱，并发送邮件
        s.login(sender, pwd)
        s.sendmail(sender, receiver, msg.as_string())
        
text = get_text()        
#send_pas(18872999731,'lllll您的验证码是：8888。请不要把验证码泄露给其他人。')        
send_mail('2212920550@qq.com', text)        
#send_sms(18872999731, '您的验证码是：8888。请不要把验证码泄露给其他人。')     