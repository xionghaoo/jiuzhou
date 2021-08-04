from bs4 import BeautifulSoup
import requests as req
from datetime import datetime
import static_value as g
import login


def getOddsMap():
    # http://9757928.com/data/game/pk300/cate/82_GY.html?t=1628091907000
    page_format = 'gb18030'
    headers = {
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7,zh-TW;q=0.6',
        'DNT': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36'
    }
    params = {'t': datetime.now().timestamp()}
    r = req.get('http://9757928.com/data/game/pk300/cate/82_GY.html', params=params, headers=headers, cookies={'token': g.bet_token})
    r.encoding = page_format
    soup = BeautifulSoup(r.text, 'html.parser')
    odd_name = soup.select('tr > td.data-focus-17361')[0].contents
    odd = soup.select('tr > td.data-focus-17361 > b')
    print("odd_name: {0}, {1}".format(odd_name, odd))


def test():
    login.login('night123', 'night123')
    getOddsMap()


test()

# 五分赛车游戏信息
# amount: 288
# cate: 3
# code: "pk300"
# collectType: 0
# curTurnNum: ""
# hot: 0
# id: 82
# interval: 5
# isBan: 0
# isCredit: 1
# isOffcial: 1
# jsType: 1
# maxReward: 0
# name: "5分赛车"
# open: 0
# openFrequency: "每5分钟一���"
# openLength: 2
# openNum: 10
# openNumFormat: "^((0[1-9]|10)[,]){9}(0[1-9]|10){1}$"
# remark: ""
# restEndDate: "2019-02-21 23:59:59"
# restStartDate: "2019-02-15 00:00:00"
# rules: "timeFormat"
# sort: 6
# turnFormat: "yyyyMMdd"
# turnLength: 3