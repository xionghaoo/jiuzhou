import json
import time

import login
import requests as req
import static_value as g
import schedule
import js2py
from datetime import datetime

ZOOM = 1.5
URL_BET = "http://9757928.com/api/bet"
URL_OPEN_INFO = "http://9757928.com/v/lottery/openInfo"

context = js2py.EvalJs()


# 号码赔率映射关系
odd_map = {
    '3': '42',
    '4': '42',
    '5': '21',
    '6': '21',
    '7': '14',
    '8': '14',
    '9': '10.5',
    '10': '10.5',
    '11': '8.4',
    '12': '10.5',
    '13': '10.5',
    '14': '14',
    '15': '14',
    '16': '21',
    '17': '21',
    '18': '42',
    '19': '42',
}


def parse_date(s):
    # 2021-08-03 10:55:02
    date_s, time_s = s.split(' ')
    year_s, mon_s, day_s = date_s.split('-')
    hour_s, minute_s, second_s = time_s.split(':')
    return datetime(int(year_s), int(mon_s), int(day_s), int(hour_s), int(minute_s), int(second_s))


def get_bet_data(money, data_odds):
    f = open("js/my_bet.js", "r", encoding='utf-8')
    context.execute(f.read())
    return context.getBetOdds(money, data_odds)


# 获取当前下注期数
def open_info():
    params = {
        'gameId': 82
    }
    response = req.get(URL_OPEN_INFO, params=params, cookies={'token': g.bet_token})
    if response.status_code == 200:
        r = json.loads(response.text)
        turn_num = r['cur']['turnNum']
        print("投注期数：{0}".format(turn_num))
        return turn_num
    else:
        print("登录失败: {0}".format(response.status_code))


# test_data = {
#     "gameId": "82",
#     "turnNum": turn_num,
#     "content": [
#         {
#             "code": "82101101",
#             "betInfo": "7",
#             "odds": "0.14",
#             "money": 0.01,
#             "betModel": 2,
#             "rebate": 0,
#             "multiple": "1",
#             "totalMoney": "0.01",
#             "totalNums": 1,
#             "cateName": "冠亚军和"
#         }
#     ]
# }
def bet(turn_num, cate_list):
    data = {
        "gameId": 82,
        "turnNum": turn_num,
        "content": cate_list,
    }
    headers = {
        "DNT": "1",
        "Content-Type": "application/json; charset=UTF-8",
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "Accept-Encoding": "gzip, deflate",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36"
    }
    bet_res = req.post(URL_BET, json=data, headers=headers, cookies={'token': g.bet_token})
    if bet_res.status_code == 200:
        print("投注成功: {0}\n".format(bet_res.text))
    else:
        print("投注失败: {0}, {1}\n".format(bet_res.status_code, bet_res.text))


def get_unopen_list():
    # 获取未开奖列表
    params = {
        'page': 1,
        'rows': 10,
        "gameId": "",
        "status": 0
    }
    res = req.get(login.URL_TODAY_LIST, params=params, cookies={'token': g.main_token})
    if res.status_code == 200:
        r = json.loads(res.text)
        # addTime 投注时间
        # betStartTime 每期开始时间
        # betEndTime 每期结束时间
        # orderNo 订单号
        # totalMoney 投注金额
        # reward 奖金
        # openNum 开彩号码
        # betInfo, oddsName 下注号码
        # oddsName 赔率
        # 投注
        log_data = []
        cate_list = []
        for item in r['data']:
            start_time = parse_date(item['betStartTime'])
            now_time = datetime.now()
            # 当天期数开始时间在四分钟内，正常应该是两分钟左右，确保是本期的投注
            if (now_time - start_time).seconds < 4 * 60:
                bet_money = round(item['totalMoney'] * ZOOM, 2)
                bet_number = item['betInfo']
                bet_data = get_bet_data(bet_money, odd_map[bet_number])
                cate_list.append({
                    "code": item['cateCode'],
                    "betInfo": bet_number,
                    "odds": bet_data['odds'],  # 赔率金额 可能会修改
                    "money": float(bet_data['money']),  # 金额最小单位
                    "betModel": int(bet_data['betModel']),  # 金额小数点 可能会修改
                    "rebate": item['rebate'],
                    "multiple": bet_data['multiple'],  # 修改
                    "totalMoney": str(bet_money),  # 修改
                    "totalNums": item['totalNums'],
                    "cateName": item['cateName'],
                })
                log_data.append({'betInfo': item['betInfo'], 'money': bet_money})
        print("本期投注：{}".format(log_data))
        return cate_list
    else:
        print("get_unopen_list：{0}".format(res.status_code))


# 自动根据主账号投注
def bet_start():
    print("---------------------------bet task run at {}---------------------------".format(
        time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())))
    # 登录投注账号
    login.login(username="night123", pwd="night123")
    # 获取本期投注期数
    turn_num = open_info()
    # 登录主账号
    login.login(username="rabbit", pwd="rabbit")
    # 获取主账号投注单
    cate_list = get_unopen_list()
    if len(cate_list) > 0:
        # 投注账号下单
        bet(turn_num, cate_list)
    else:
        print("主账号未投注\n")


def auto_task():
    for hour in range(11, 15):
        for minute in range(0, 6):
            schedule.every().day.at("{0}:{1}2".format(hour, minute)).do(bet_start)
            schedule.every().day.at("{0}:{1}7".format(hour, minute)).do(bet_start)
    print("start bet task...")
    while True:
        schedule.run_pending()
        time.sleep(1)


def test():
    print(round(0.02*2.5, 2))


auto_task()
# bet_start()
# test()
