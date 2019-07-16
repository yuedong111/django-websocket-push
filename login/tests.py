from django.test import TestCase

# Create your tests here.
# !/usr/bin/python
# -*- coding: utf-8 -*-
import json, urllib
from urllib.parse import urlencode
import requests

# ----------------------------------
# 短信API服务调用示例代码 － 聚合数据
# 在线接口文档：http://www.juhe.cn/docs/54
# ----------------------------------

def main():
    # 配置您申请的APPKey
    appkey = "7bd93b0103405f80b1a7560bd8c8fe90"

    # 1.屏蔽词检查测
    # request1(appkey, "GET")

    # 2.发送短信
    request2(appkey, "GET")


# 屏蔽词检查测
def request1(appkey, m="GET"):
    url = "http://v.juhe.cn/sms/black"
    params = {
        "word": "",  # 需要检测的短信内容，需要UTF8 URLENCODE
        "key": appkey,  # 应用APPKEY(应用详细页查询)

    }
    params = urlencode(params)
    if m == "GET":
        f = requests.get("{}?{}".format(url, params))
    else:
        f = requests.get(url, data=params)

    content = f.json()
    res = json.loads(content)
    print(content)
    if res:
        error_code = res["error_code"]
        if error_code == 0:
            print(res["result"])
        else:
            print("%s:%s" % (res["error_code"], res["reason"]))
    else:
        print("request api error")


# 发送短信
def request2(appkey, m="GET"):
    url = "http://v.juhe.cn/sms/send"
    params = {
        "mobile": "17783886899",
        "tpl_id": "126424",
        "tpl_value": "#code#=234576",
        "key": appkey,
        "dtype": "json",

    }
    params = urlencode(params)
    if m == "GET":
        r = requests.get("{}?{}".format(url, params))
    else:
        r = requests.get(url,data=params)

    res = r.json()
    print(res)
    if res:
        error_code = res["error_code"]
        if error_code == 0:
            # 成功请求
            print(res["result"])
        else:
            print("%s:%s" % (res["error_code"], res["reason"]))
    else:
        print("request api error")


if __name__ == '__main__':
    main()