import json
import time

import login
import requests as req
import static_value as g
import schedule

URL_BET = "http://9757928.com/api/bet"
URL_OPEN_INFO = "http://9757928.com/v/lottery/openInfo"


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
        print("投注成功: {0}".format(bet_res.text))
    else:
        print("投注失败: {0}, {1}".format(bet_res.status_code, bet_res.text))


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
        # 投注

        cate_list = []
        for item in r['data']:
            cate_list.append({
                "code": item['cateCode'],
                "betInfo": item['betInfo'],
                "odds": item['odds'],
                "money": item['money'],
                "betModel": item['betModel'],
                "rebate": item['rebate'],
                "multiple": str(item['multiple']),
                "totalMoney": str(item['totalMoney']),
                "totalNums": item['totalNums'],
                "cateName": item['cateName'],
            })
        print("未开奖列表：{}".format(cate_list))
        return cate_list
    else:
        print("get_unopen_list：{0}".format(res.status_code))


# 自动根据主账号投注
def bet_start():
    print("bet task run at {}".format(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())))
    login.login(username="night123", pwd="night123")
    turn_num = open_info()
    login.login(username="rabbit", pwd="rabbit")
    cate_list = get_unopen_list()
    if len(cate_list) > 0:
        bet(turn_num, cate_list)
    else:
        print("主账号未投注")


# bet_start()

def test_task():
    # 格式化成2016-03-20 11:45:39形式
    print("do task at {}".format(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())))


def auto_task():
    for hour in range(11, 14):
        for minute in range(0, 6):
            # print("time: {0}:{1}3".format(hour, minute))
            schedule.every().day.at("{0}:{1}3".format(hour, minute)).do(test_task)
            # print("time: {0}:{1}7".format(hour, minute))
            schedule.every().day.at("{0}:{1}7".format(hour, minute)).do(test_task)
    print("start time task...")
    while True:
        schedule.run_pending()
        time.sleep(1)


auto_task()
