###ЕСЛИ НЕ РАБОТАЕТ ПРОГА, ОБРАТИСЬ К БОГДАНУ. У ТЕБЯ СКОРЕЕ ВСЕГО НЕ УСТАНОВЛЕНЫ БИБЛИОТЕКИ
# P.S. Да, requirements.txt я не сделал))

import email
import imaplib
import smtplib
import ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# from email.header import decode_header
# import base64
# from bs4 import BeautifulSoup
# import re


def mail_send(IncID, message, receiver_email):
    port = 465
    smtp_server = "smtp.yandex.com"
    email_login = "dronbrother@yandex.ru"
    email_password = "12323212t"
    # receiver_email = "andreykae28@gmail.com" #УКАЗЫВАТЬ СВОЙ АДРЕС ДЛЯ ДЕМОНСТРАЦИИ. СООБЩЕНИЕ МОЖЕТ (А СКОРЕЕ ВСЕГО И ТАК И БУДЕТ) ПОПАСТЬ В СПАМ
    #
    # message = """
    #     #WAF_003
    #     ☢️ Инцидент: Срабатывание критичной сигнатуры WAF в User-Agent
    #
    #     Описание Инцидента:
    #     Nemesida WAF зафиксировал атаку в User-agent на ресурс example.com/cgi-mod/finger.pl, распознанную как Scanner с хоста 200.200.200.20. User-Agent: Mozilla/5.00 (Nikto/2.1.6) (Evasions:None) (Test:000027)
    #
    #     KeyFields:
    #     Nemesida|200.200.200.20|example.com|Scanner
    #
    #     ID инцидента: WAF-003
    # """

    msg = MIMEMultipart()
    msg["From"] = email_login
    msg["To"] = receiver_email
    msg["Subject"] = IncID
    msg.attach(MIMEText(message, "plain"))

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
        server.login(email_login, email_password)
        server.sendmail(email_login, receiver_email, msg.as_string())


def mail_read(IncID):
    # imap conntect
    imap_server = "imap.yandex.com"
    email_login = "dronbrother@yandex.ru"
    email_password = "12323212t"
    imap = imaplib.IMAP4_SSL(imap_server)
    imap.login(email_login, email_password)

    imap.select("INBOX")
    typ, data = imap.search(None, "ALL")
    data = data[0].split()

    IncID_response = False

    for i in data:
        status, data = imap.fetch(i, "(RFC822)")
        data = data[0][1]
        msg = email.message_from_bytes(data)

        if IncID in msg["Subject"]:
            IncID_response = True

    imap.close()
    return IncID_response


# mail_send("WAF-004")
# print(mail_read("WAF-004"))
