# -*- coding: utf-8 -*-
'''
-------------------------------------------------
   File Name：     test3
   Author :        zhongrf
   Date：          2019/11/2
-------------------------------------------------
'''
__author__ = 'zhongrf'
import StringIO
import json
import xlrd
import xlsxwriter

from django.db.models import Q
from django.http import HttpResponse, JsonResponse
from datetime import datetime, timedelta
from blueking.component.shortcuts import get_client_by_request
from common.mymako import render_json
from home_application.models import *
from home_application.celery_tasks import run_celery
from home_application.esb_api import *
from home_application.esb_helper import *


def test3_get_biz(request):
    return get_all_biz(request)


# 获取业务拓扑树
def test3_get_app_topo(request):
    try:
        bk_biz_id = json.loads(request.body)["bk_biz_id"]
        client = get_client_by_request(request)
        result = client.cc.search_biz_inst_topo({
            'bk_biz_id': bk_biz_id,
            'level': -1
        })
        return_data = result["data"]
        for i in return_data:
            set_data = get_set_data(i)
            i["child"] = set_data
            format_is_parent(i)
        return render_json({"result": True, 'data': result["data"]})
    except Exception, e:
        print e
        return render_json({"result": False, "message": str(e)})


def get_set_data(one_obj):
    return_data = []
    for i in one_obj["child"]:
        if i["bk_obj_id"] == 'set':
            return_data.append(i)
            continue
        else:
            return_data.extend(get_set_data(i))
    return return_data


def format_is_parent(i):
    i["isParent"] = len(i["child"]) > 0
    if i["isParent"]:
        for u in i["child"]:
            format_is_parent(u)


def test3_get_host_ip(request):
    try:
        params = json.loads(request.body)
        bk_biz_id = params["bk_biz_id"]
        client = get_client_by_request(request)
        if params["bk_obj_id"] not in ['biz', 'module', 'set']:
            params["bk_obj_id"] = 'object'
            condition = [{"field": "bk_inst_id", "operator": "$eq", "value": int(params["value"])}]
        else:
            condition = [
                {"field": "bk_%s_id" % params["bk_obj_id"], "operator": "$eq", "value": int(params["value"])}]
        kwargs = {
            'bk_biz_id': bk_biz_id,
            "condition": [
                {
                    "bk_obj_id": params["bk_obj_id"],
                    "fields": [],
                    "condition": condition
                },
                {
                    "bk_obj_id": "host",
                    "fields": [],
                    "condition": []
                }
            ]
        }
        result = client.cc.search_host(kwargs)
        return_data = []
        for i in result['data']['info']:
            i['host']['bk_os_type'] = OS_TYPE.get(i['host']['bk_os_type'], '')
            if len(i['host']['bk_cloud_id']) == 0:
                i['host']['bk_cloud_id'] = 0
            else:
                i['host']['bk_cloud_id'] = i['host']['bk_cloud_id'][0]['bk_inst_id']
            return_data.append(i['host'])
        return render_json({"result": True, 'data': return_data})
    except Exception, e:
        print e
        return render_json({"result": False, "message": str(e)})


def test3_get_joblist(request):
    try:
        result = [
            {
                'num': 1,
                'ip': '192.168.0.1',
                'file_list': 'a.txt;b.txt;c.txt',
                'file_num': 3,
                'file_size': '30M',
                'copy_time': '2019-11-02 10:11:24',
                'copy_person': 'admin',

            }, {
                'num': 2,
                'ip': '192.168.0.2',
                'file_list': 'a.txt;b.txt;c.txt',
                'file_num': 3,
                'file_size': '30M',
                'copy_time': '2019-11-02 10:11:24',
                'copy_person': 'admin',

            }, {
                'num': 3,
                'ip': '192.168.0.3',
                'file_list': 'a.txt;b.txt;c.txt',
                'file_num': 3,
                'file_size': '30M',
                'copy_time': '2019-11-02 10:11:24',
                'copy_person': 'admin',

            }
        ]
        return render_json({"result": True, 'data': result})
    except Exception, e:
        print e
        return render_json({"result": False, "message": str(e)})


def test3_get_fileinfo(request):
    try:
        params = json.loads(request.body)
        check_app = {
            'bk_biz_id': params["business"],
            'ip_list': params["host_obj"]
        }
        execute_account = 'root'
        script_content = """#!/bin/bash 
        
            cd /data/logs
            du -ch *.txt
            ls -lR | grep .txt|wc -l
        """

        client = get_client_by_request(request)
        result = fast_execute_script(check_app, client, execute_account, script_content)
        log_result = get_task_ip_log(client, check_app["bk_biz_id"], result['data'])

        result_list = []
        for index, log in enumerate(log_result):
            result_data = {}
            if log["is_success"]:
                result_data["num"] = index
                result_data["ip"] = log["ip"]
                content = log['log_content'].split("\n")
                content_num = int(content[len(content) - 2])
                result_data["file_num"] = content_num

                file_list = []

                for i in range(content_num+1):
                    if i == content_num:
                        result_data["file_size"] = content[i].split("\t")[0]
                    else:
                        file_list.append(content[i].split("\t")[1])
                result_data["file_list"] = ",".join(file_list)
                result_list.append(result_data)
        return render_json({"result": True, 'data': result_list})
    except Exception, e:
        print e
        return render_json({"result": False, "message": str(e)})
