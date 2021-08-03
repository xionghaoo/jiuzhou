import xlwings as xw
import login
import static_value as g
import json
import requests as req

URL_TODAY_LIST = "http://9757928.com/api/cp/records/todayList"
URL_HOST_LIST = "http://9757928.com/api/cp/records/historyList"


def load_today_records(user):
    wb = xw.Book()
    wb.save("today_bet_data_{}.xlsx".format(user))
    global sheet
    sheet = wb.sheets['Sheet1']
    sheet.range('A1').value = ["期号", "投注号码", "开奖号码", "投注金额", "奖金", "投注时间", "每期开始时间", "每期结束时间"]
    sheet.range('A1').column_width = 14
    sheet.range('B1').column_width = 10
    sheet.range('C1').column_width = 26
    sheet.range('D1').column_width = 9
    sheet.range('E1').column_width = 9
    sheet.range('F1').column_width = 15
    sheet.range('G1').column_width = 15
    sheet.range('H1').column_width = 15
    sheet.range('A1:H1').api.Font.Bold = True
    sheet.range("A1").row_height = 16
    sheet.range("A1:H1").api.HorizontalAlignment = -4108
    sheet.range("A1:H1").api.VerticalAlignment = -4130
    for i in range(1, 24):
        print('load page {}'.format(i))
        # 今天投注记录
        today_list(user, i, "")


def today_list(user, page, status):
    params = {
        'page': page,
        'rows': 10,
        "gameId": "",
        "status": status
    }
    if user == "rabbit":
        token = g.main_token
    else:
        token = g.bet_token
    response = req.get(URL_TODAY_LIST, params=params, cookies={'token': token})
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
        for index, item in enumerate(r['data']):
            # today_record_file.write(
            #     "{0}, {1}, {2}, {3}, {4}\n".format(item['turnNum'],
            #                                             item['betInfo'], item['openNum'], item['totalMoney'],
            #                                             item['reward'])
            # )
            line = [
                item['turnNum'],
                item['betInfo'],
                item['openNum'],
                item['totalMoney'],
                item['reward'],
                item['addTime'],
                item['betStartTime'],
                item['betEndTime']
            ]
            if page == 1:
                line_index = index + 2
            else:
                line_index = index + 2 + (page - 1) * 10
            sheet.range("A{}".format(line_index)).value = line
            sheet.range("A{}".format(line_index)).row_height = 16
            sheet.range("A{0}:H{1}".format(line_index, line_index)).api.HorizontalAlignment = -4108
            sheet.range("A{0}:H{1}".format(line_index, line_index)).api.VerticalAlignment = -4130
            if float(item['reward']) > 0:
                # sheet.range("A{}".format(line_index)).api.Font.Color = 0xFFFFFF
                sheet.range("A{0}:H{1}".format(line_index, line_index)).color = (129, 212, 188)
    else:
        print("加载投注记录失败：{0}".format(response.status_code))


def today_bet_data():
    wb = xw.Book()
    wb.save("test.xlsx")
    sheet = wb.sheets['Sheet1']
    sheet.range('A1').value = ["name", "age", "gender"]
    sheet.range('A2').value = ["name", "age", "gender"]
    sheet.range('A1').row_height = 16
    sheet.range('A1').column_width = 14
    print(sheet.range('A1').row_height)
    print(sheet.range('A2').column_width)
    sheet.range('A1:A3').api.HorizontalAlignment = -4108
    sheet.range('A1:A3').api.VerticalAlignment = -4130


login.login("night123", "night123")
load_today_records("night123")

# login.login("rabbit", "rabbit")
# load_today_records("rabbit")

# today_bet_data()

