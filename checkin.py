# coding=utf-8
import requests
import time
from bs4 import BeautifulSoup
import re

token = 'bot_token'
uid = 'telegram_uid'
user = 'username'
pw = 'password'
start_time = time.time()
login = requests.post('https://cccat.io/user/_login.php',
                      data={'email': user, 'passwd': pw, 'remember_me': 'week'})


def info():
    user_info = requests.get('https://cccat.io/user/index.php', cookies=login.cookies)
    parser = BeautifulSoup(user_info.text, 'html.parser')
    rule = re.compile('Remaining Transfer')
    transfer = str(parser.find('p', text=rule)).split()[3]
    return transfer


checkin = requests.get('https://cccat.io/user/_checkin.php', cookies=login.cookies)
results = checkin.json()
user_transfer = info()
if results.get('msg') == 'You have already checked in':
    requests.post('https://api.telegram.org/bot' + token + '/sendMessage',
                  data={'chat_id': uid, 'text': 'CCCAT: 今天已签过到\n剩余流量: ' + user_transfer})
else:
    prize = results.get('msg').split()
    requests.post('https://api.telegram.org/bot' + token + '/sendMessage',
                  data={'chat_id': uid, 'text': 'CCCAT: 获得了 ' + prize[1]
                        + ' 流量\n剩余流量: ' + user_transfer + '\n本次签到用时 ' +
                        str(time.time() - start_time) + ' 秒'})
