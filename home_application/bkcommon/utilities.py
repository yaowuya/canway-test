# -*- coding:utf-8 -*-
import datetime
import json


# 获取当前时间 年-月-日 时:分:秒
def get_time_now_str():
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")


# 获取当前日期 年-月-日
def get_date_now_str():
    return datetime.datetime.now().strftime("%Y-%m-%d")


# DateTimeField格式化
class CJsonEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(obj, datetime.date):
            return obj.strftime('%Y-%m-%d')
        else:
            return json.JSONEncoder.default(self, obj)
