import json

import requests as req
import random
import js2py
import static_value as g

URL_LOGIN = "http://9757928.com/v/user/login"
URL_TODAY_LIST = "http://9757928.com/api/cp/records/todayList"
URL_HOST_LIST = "http://9757928.com/api/cp/records/historyList"

context = js2py.EvalJs()


# 账号登录
def login(username, pwd):
    f = open("js/md5.js", "r")
    context.execute(f.read())
    password = context.hex_md5(pwd)
    data = {
        'r': random.random(),
        'account': username,
        'password': password
    }
    print("登录九州国际：{0}, {1}".format(username, pwd))
    response = req.post(URL_LOGIN, data=data)
    if username == "rabbit":
        g.main_token = response.cookies.get_dict()['token']
    else:
        g.bet_token = response.cookies.get_dict()['token']
    if response.status_code == 200:
        r = json.loads(response.text)
        print("登录成功，登录用户：{0}".format(r['account']))
    else:
        print("登录失败: {0}".format(response.status_code))


def load_today_records():
    global today_record_file
    today_record_file = open("today_order_records.txt", "w")
    for i in range(1, 24):
        print('load page {}'.format(i))
        # 今天投注记录
        today_list(g.main_token, i)


def load_history_records():
    global history_record_file
    history_record_file = open("history_order_records.txt", "w")
    dates = ["2021-07-28", "2021-07-29", "2021-07-30", "2021-07-31"]
    for date in dates:
        for i in range(1, 24):
            print('load page {}'.format(i))
            # 今天投注记录
            history_list(g.main_token, i, date)


def today_list(page, status):
    params = {
        'page': page,
        'rows': 10,
        "gameId": "",
        "status": status
    }
    response = req.get(URL_TODAY_LIST, params=params, cookies={'token': g.main_token})
    if response.status_code == 200:
        r = json.loads(response.text)
        # addTime 投注时间
        # betStartTime 每期开始时间
        # betEndTime 每期结束时间
        # orderNo 订单号
        # totalMoney 投注金额
        # reward 奖金
        # openNum 开彩号码
        # betInfo, oddsName 下注号码
        for item in r['data']:
            today_record_file.write(
                "{0}, {1}, {2}, {3}, {4}\n".format(item['turnNum'],
                                                        item['betInfo'], item['openNum'], item['totalMoney'],
                                                        item['reward'])
            )
    else:
        print("加载投注记录失败：{0}".format(response.status_code))


def history_list(page, date):
    # page=1&rows=10&gameId=&status=&date=2021-07-30
    params = {
        'page': page,
        'rows': 10,
        "gameId": "",
        "status": "",
        "date": date
    }
    response = req.get(URL_HOST_LIST, params=params, cookies={'token': g.main_token})
    if response.status_code == 200:
        r = json.loads(response.text)
        # addTime 投注时间
        # betStartTime 每期开始时间
        # betEndTime 每期结束时间
        # orderNo 订单号
        # totalMoney 投注金额
        # reward 奖金
        # openNum 开彩号码
        # betInfo, oddsName 下注号码
        # turnNum, 20210801158, 期号
        for item in r['data']:
            history_record_file.write(
                "{0}, {1}, {2}, {3}, {4}\n".format(item['turnNum'],
                                                        item['betInfo'], item['openNum'], item['totalMoney'],
                                                        item['reward'])
            )
    else:
        print("加载投注记录失败：{0}".format(response.status_code))


# def test():
#     f = open("js/md5.js", "r")
#     context.execute(f.read())
#     password = context.hex_md5("night123")
#     print(random.random())
#     print(password)
#
#
# test()
