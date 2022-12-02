import requests
from bs4 import BeautifulSoup

import notify
import datetime
import sqlite3

conn = sqlite3.connect('flight.db')

'''
'''

def init_db():
    # 连仓库
    # 建表
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS NOTIFY
           (ID INTEGER PRIMARY KEY   AUTOINCREMENT  NOT NULL,
           COMPANY         VARCHAR(200)  NOT NULL,
           TITLE                VARCHAR(2000)     NOT NULL
           );''')


def check_db_exist(company,title):
    c = conn.cursor()
    c.execute('select count(1) from NOTIFY WHERE COMPANY = ? AND TITLE = ?',[company,title])
    count = c.fetchone()[0]
    if count > 0:
        return True
    else:
        c.execute('INSERT INTO NOTIFY (COMPANY,TITLE) VALUES (?,?)',[company,title])
    conn.commit()

def check_ca():
    ca_url = "http://www.airchina.com.cn/cn/info/new-service/service_announcement.shtml"
    response = requests.get(ca_url)
    soup = BeautifulSoup(response.text, 'html.parser')
    links = soup.select("div.serviceMsg a")
    today = datetime.date.today().strftime("%Y-%m-%d")
    notify_message = ""
    for link in links:
        title = link.text
        create_date = link.nextSibling.text[1:-1]
        if today == create_date:
            if not check_db_exist('CA',title):
                notify_message += title + ":" + create_date + '\n'

    if notify_message:
        notify.send("国航今日通知", notify_message)


def check_mu():
    mu_url = "https://www.ceair.com/global/static/Announcement/AnnouncementMessage/notices/"
    response = requests.get(mu_url)
    soup = BeautifulSoup(response.content, 'html.parser')
    links = soup.select("div.uw_chntent_right_text span.right_span")
    today = datetime.date.today().strftime("%Y-%m-%d")
    notify_message = ""
    for link in links:
        title = link.text
        create_date = link.nextSibling.nextSibling.text.strip()
        if today == create_date:
            if not check_db_exist('MU', title):
                notify_message += title + ":" + create_date + '\n'
    if notify_message:
        notify.send("东航今日通知", notify_message)


def check_cz():
    cz_url = "https://www.csair.com/cn/about/news/notice/2022/"
    response = requests.get(cz_url)
    soup = BeautifulSoup(response.content, 'html.parser')
    links = soup.select("div.tabContent>ul>li>a")
    today = datetime.date.today().strftime("%Y-%m-%d")
    notify_message = ""
    for link in links:
        title = link.text
        if link.nextSibling:
            create_date = link.nextSibling.text[1:-1]
        else:
            create_date = ""
        if today == create_date:
            if not check_db_exist('CZ', title):
                notify_message += title + ":" + create_date + '\n'
    if notify_message:
        notify.send("南航今日通知", notify_message)


if __name__ == '__main__':
    init_db()
    check_ca()
    check_mu()
    check_cz()

