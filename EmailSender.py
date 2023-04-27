# 设置服务器所需信息
# 163邮箱服务器地址
import smtplib
from email.mime.text import MIMEText


def Send(content: str, text: str):
    mail_host = 'smtp.qq.com'
    # qq邮箱用户名
    mail_user = ''
    # 密码(部分邮箱为授权码)
    mail_pass = ''
    # 邮件发送方邮箱地址
    sender = ''
    # 邮件接受方邮箱地址，注意需要[]包裹，这意味着你可以写多个邮件地址群发
    receivers = ['']

    # 设置email信息
    # 邮件内容设置
    message = MIMEText(text, 'plain', 'utf-8')
    # 邮件主题
    message['Subject'] = content
    # 发送方信息
    message['From'] = sender
    # 接受方信息
    message['To'] = receivers[0]
    # 邮件正文
    # message = MIMEText(text, 'plain', 'utf-8')

    # 登录并发送邮件
    try:
        #连接到服务器
        smtpObj = smtplib.SMTP_SSL(mail_host, 465)
         #登录到服务器
        smtpObj.login(mail_user,mail_pass)
        #发送
        smtpObj.sendmail(sender,receivers,message.as_string())
        #退出
        smtpObj.quit()
        print('success')
    except smtplib.SMTPException as e:
        print('error', e)  # 打印错误
