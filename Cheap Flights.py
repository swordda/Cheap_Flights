import requests
from urllib.parse import urlencode
import datetime
import json
import pymysql
import EmailSender

connection = pymysql.connect(
    host='localhost',
    user='root',
    password='', # 本地数据库密码
    db='', # 本地数据库名称
    charset='utf8',
    cursorclass=pymysql.cursors.DictCursor
)
base_url = "https://r.fliggy.com/rule/domestic?"
headers = {
    "accept": "*/*",
    "accept-language": "zh-CN,zh;q=0.9",
    "sec-ch-ua": "\"Not_A Brand\";v=\"99\", \"Microsoft Edge\";v=\"109\", \"Chromium\";v=\"109\"",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "\"Windows\"",
    "sec-fetch-dest": "script",
    "sec-fetch-mode": "no-cors",
    "sec-fetch-site": "same-site",
    "cookie": "cna=7H5yG/23jlMCAW8TXkMev2F7; xlly_s=1; sgcookie=E100Sz36mgb++XCZG2VFFnh9YxwKID6ShefUAkwyJySDVDnrSK3MVDvM7v8fwY0sw/d2vSwWXCES7g+BtrZ1HoaMFNFkByG66sQ7jKeAqCm0m1pOybMVJkbLTTTLNVfMpc2s; t=50b00a8ca16825936207864640edc27d; tracknick=tb99997706; lid=tb99997706; enc=XKaSByxe9ypV7d27zYCO7xjYOKtFaIOJ5Hav9mtlYPQqD+/CKFTYNxUj/W6Kqs3TJ4saYwtLYlgk4NLfwegvRw==; _tb_token_=ee1ebebebb3e6; cookie2=123f1dcb303134484eb3c4d38ffb8979; tfstk=cwx1BPYIm5V6Son0j1MEQDmI4Ns5a_25hV1MCfQhU4C08ypC9squ4_wa9EVA0tBC.; l=fBM9EJBlTDXGwlhfBO5Zlurza77tUQOf5sPzaNbMiIEGa66f6F_1RNCeTkn9JdtjgT5YpetPzjfqZdhJJ4zU-xaRbqJN7QO6RivwReM3N7AN.; isg=BCUlFfdOquoxY862NkavCj7INOFfYtn06KPMvCcJt9xrPkyw77ISxWOYyKJIPvGs",
    "referer": "https://www.fliggy.com/",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36 Edg/109.0.1518.61",
    "referrerPolicy": "strict-origin-when-cross-origin",
    "body": "null",
    "method": "GET",
    "mode": "cors",
    "credentials": "include"
}


def write_in_datebase(arrName, time, price):
    curse = connection.cursor()
    sql = "insert into DisconutPassenger(insertTime,depDate,price,setupTime) values(\"%s\",\"%s\",\"%s\",\"%s\");" % (
        datetime.date.today(), arrName, price, time)
    connection.ping(reconnect=True)
    try:
        curse.execute(sql)
    except:
        print("异常")
    connection.commit()
    connection.close()


def find_in_database(arrName, time, price):
    curse = connection.cursor()
    sql = "SELECT * from DisconutPassenger where price = %s AND setupTime = \"%s\" AND depDate = \"%s\";" % (
        price, time, arrName)
    connection.ping(reconnect=True)
    try:
        a = curse.execute(sql)
    except:
        print("异常")
    connection.commit()
    connection.close()
    if a == 0:
        write_in_datebase(arrName, time, price)
        return 0
    else:
        return 1


def get_page():
    params = {
        "routes": "SIA-",  # 出发城市三字代码
        "startDate": datetime.date.today(),
        "endDate": datetime.date.today() + datetime.timedelta(days=45),
        "flag": 1,
        "ruleld": 99,
        "calback": "neonsaleDatalist"
    }
    url = base_url + urlencode(params)
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.text
    except requests.ConnectionError as e:
        print("error", e.args)


if __name__ == '__main__':
    res = get_page()
    json1 = json.loads(res[5:-1])
    for i in range(0, 17):
        print(i)
        if json1['data'].get('flights')[i]['price'] <= 180: # 价格小于180发邮件
            str3 = json1['data'].get('config').get('moreLink').split('&')[0] + '&depCity=' + json1['data'].get('flights')[i]['depCode'] + '&arrCity=' + json1['data'].get('flights')[i]['arrCode'] + '&tripType=0&depDate=' + json1['data'].get('flights')[i]['depDate'] + '&searchBy=1314&scene=%E6%9C%BA%E7%A5%A8%E9%A2%91%E9%81%93%E9%A6%96%E9%A1%B5'
            str2 = json1['data'].get('flights')[i][
                       'depDate'] + '有到' + json1['data'].get('flights')[i]['arrName'] + '的飞机，价格' + str(
                json1['data'].get('flights')[i]['price']) + '元'
            a = find_in_database(json1['data'].get('flights')[i]['arrName'], json1['data'].get('flights')[i]['depDate'],
                                 json1['data'].get('flights')[i]['price'])
            print(str2,a)
            if a == 0:
                EmailSender.Send(str2, str3)

# http://s.jipiao.trip.taobao.com/cheap_flight_search.htm?spm=181.7091613.a1z67.10021&depCityName=&depCity=&dep&range=15&arrCityName=&arrCity=
# https://sjipiao.fliggy.com/homeow/trip_flight_search.htm?spm=181.14011266.7662523580.1.63225ec2lCBkof&depCity=BJS&arrCity=HRB&tripType=0&depDate=2023-01-26&searchBy=1314&scene=%E6%9C%BA%E7%A5%A8%E9%A2%91%E9%81%93%E9%A6%96%E9%A1%B5
