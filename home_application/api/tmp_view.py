# -*- coding: utf-8 -*-

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


def tmp_test(request):
    last_login = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return render_json({
        'username': request.user.username,
        'phone': u'18800000000',
        'last_login': last_login,
        'result': True,
        'email': u'admin@qq.com',
    })


def test_celery(request):
    try:
        client = get_client_by_request(request)
        result = run_celery.delay(client)
        return render_json({"result": True, "data": result})
    except Exception, e:
        print e
        return render_json({"result": False, "data": str(e)})


def tmp_get_biz(request):
    return get_all_biz(request)


# 获取集群
def tmp_get_set(request):
    try:
        bk_biz_id = json.loads(request.body)["bk_biz_id"]
        client = get_client_by_request(request)
        kwargs = {
            'bk_biz_id': bk_biz_id,
            'condition': {},
            'fields': ["bk_set_id", "bk_set_name"],
            'page': {'limit': 20, 'sort': 'bk_set_name', 'start': 0}
        }
        res = client.cc.search_set(kwargs)
        if not res["result"]:
            return render_json({"result": False, "data": res["data"]})
        else:
            info = res["data"]["info"]
            result = [{"id": i["bk_set_id"], "text": i["bk_set_name"]} for i in info]
            return render_json({"result": True, "data": result})
    except Exception, e:
        return render_json({"result": False, "message": str(e)})


# 获取主机
def tmp_get_host(request):
    bk_biz_id = json.loads(request.body)["business"]
    bk_set_id = json.loads(request.body)["set"]
    client = get_client_by_request(request)

    if len(bk_set_id) > 0:
        kwargs = {
            "condition": [
                {
                    "bk_obj_id": "biz",
                    "fields": [],
                    # 根据业务ID查询主机
                    "condition": [
                        {
                            "field": "bk_biz_id",
                            "operator": "$eq",
                            "value": int(bk_biz_id)
                        }
                    ]
                },
                {
                    "bk_obj_id": "set",
                    "fields": [],
                    "condition": [
                        {
                            "field": "bk_set_id",
                            "operator": "$eq",
                            "value": int(bk_set_id)
                        }
                    ]
                }
            ]

        }
    else:
        kwargs = {
            "condition": [
                {
                    "bk_obj_id": "biz",
                    "fields": [],
                    # 根据业务ID查询主机
                    "condition": [
                        {
                            "field": "bk_biz_id",
                            "operator": "$eq",
                            "value": int(bk_biz_id)
                        }
                    ]
                }
            ]
        }

    result = client.cc.search_host(kwargs)
    return_data = []
    for i in result['data']['info']:
        return_data.append({
            'id': i['host']['bk_host_innerip'],
            'text': i['host']['bk_host_innerip']
        })
    return render_json({"result": True, 'data': return_data})


def tmp_add_host(request):
    try:
        bk_biz_id = json.loads(request.body)["business"]
        bk_set_id = json.loads(request.body)["set"]
        bk_host_innerip = json.loads(request.body)["host"]

        HostData.objects.create(bk_biz_id=bk_biz_id,
                                bk_set_id=bk_set_id,
                                bk_host_innerip=bk_host_innerip)
        return render_json({"result": True})
    except Exception, e:
        print e
        return render_json({"result": False, "message": str(e)})


def tmp_get_hostList(request):
    try:
        bk_biz_id = json.loads(request.body)["business"]
        host = json.loads(request.body)["host"]
        bk_host_outerip = host.split()
        client = get_client_by_request(request)

        kwargs = {
            "ip": {"flag": "bk_host_innerip|bk_host_outerip", "exact": 1, "data": bk_host_outerip},
            "condition": [
                {
                    "bk_obj_id": "biz",
                    "fields": [],
                    # 根据业务ID查询主机
                    "condition": [
                        {
                            "field": "bk_biz_id",
                            "operator": "$eq",
                            "value": int(bk_biz_id)
                        }
                    ]
                }
            ]
        }

        result = client.cc.search_host(kwargs)
        return_data = []
        for i in result['data']['info']:
            i['host']['bk_os_type'] = OS_TYPE.get(i['host']['bk_os_type'], '')
            if len(i['host']['bk_cloud_id']) == 0:
                continue
            i['host']['bk_inst_name'] = i['host']['bk_cloud_id'][0]['bk_inst_name']
            i['host']['bk_cloud_id'] = i['host']['bk_cloud_id'][0]['bk_inst_id']
            i['host']['bk_mem_rate'] = '--'
            i['host']['bk_disk_rate'] = '--'
            i['host']['bk_cpu_rate'] = '--'
            host_obj = HostInfo.objects.filter(bk_host_innerip=i['host']['bk_host_innerip'],
                                               bk_cloud_id=i['host']['bk_cloud_id'])
            if len(host_obj) > 0:
                i['host']['bk_is_job'] = host_obj[0].bk_is_job
            else:
                i['host']['bk_is_job'] = False
            return_data.append(i['host'])

        return render_json({"result": True, 'data': return_data})
    except Exception, e:
        print e
        return render_json({"result": False, "message": str(e)})


def tmp_query_resource(request):
    try:
        params = json.loads(request.body)
        check_app = {
            'bk_biz_id': params["bk_biz_id"],
            'ip_list': [{
                'ip': params["ip"],
                'bk_cloud_id': params["bk_cloud_id"]
            }]
        }
        execute_account = 'root'
        script_content = """#!/bin/bash

            MEMORY=$(free -m | awk 'NR==2{printf "%.2f%%", $3*100/$2 }')
            DISK=$(df -h | awk '$NF=="/"{printf "%s", $5}')
            CPU=$(top -bn1 | grep load | awk '{printf "%.2f%%", $(NF-2)}')
            DATE=$(date "+%Y-%m-%d %H:%M:%S")
            echo -e "$DATE|$MEMORY|$DISK|$CPU"
        """
        client = get_client_by_request(request)
        result = fast_execute_script(check_app, client, execute_account, script_content)
        log_result = get_task_ip_log(client, check_app["bk_biz_id"], result['data'])

        result_data = {}
        if log_result[0]["is_success"]:
            result_data["ip"] = log_result[0]["ip"]
            content_array = log_result[0]["log_content"].split("|")
            result_data["bk_mem_rate"] = content_array[1]
            result_data["bk_disk_rate"] = content_array[2]
            result_data["bk_cpu_rate"] = content_array[3]
            return render_json({"result": True, "data": result_data})
        else:
            return render_json({"result": False, "message": str(log_result)})
    except Exception, e:
        print e
        return render_json({"result": False, "message": str(e)})


def tmp_add_queue(request):
    try:
        params = json.loads(request.body)
        HostInfo.objects.update_or_create(
            bk_host_innerip=params["bk_host_innerip"],
            bk_biz_id=params["bk_biz_id"],
            bk_cloud_id=params["bk_cloud_id"],
            bk_admin=request.user.username,
            defaults={"bk_is_job": True}
        )
        return render_json({"result": True})
    except Exception, e:
        print e
        return render_json({"result": False, "message": str(e)})


def tmp_remove_queue(request):
    try:
        params = json.loads(request.body)
        HostInfo.objects.filter(bk_host_innerip=params["bk_host_innerip"],
                                bk_biz_id=params["bk_biz_id"],
                                bk_cloud_id=params["bk_cloud_id"]).update(bk_is_job=False)
        return render_json({"result": True})
    except Exception, e:
        print e
        return render_json({"result": False, "message": str(e)})


def tmp_query_host_resource(request):
    try:
        bk_host_innerip = json.loads(request.body)["bk_host_innerip"]
        now = datetime.datetime.now()
        before_hour = now - timedelta(hours=1)
        host_resource = HostResource.objects.filter(
            host_info__bk_host_innerip=bk_host_innerip,
            bk_date__range=(before_hour.strftime("%Y-%m-%d %H:%M:%S"), now.strftime("%Y-%m-%d %H:%M:%S"))
        ).order_by("bk_date")
        x_axis = []
        result = {
            "mem": [],
            "disk": [],
            "cpu": []
        }
        for hr in host_resource:
            x_axis.append(hr.bk_date)
            result["mem"].append(float(hr.bk_mem_rate))
            result["disk"].append(float(hr.bk_disk_rate))
            result["cpu"].append(float(hr.bk_cpu_rate))

        return render_json({"result": True, "xAxis": x_axis, "data": result})
    except Exception, e:
        print e
        return render_json({"result": False, "message": str(e)})


# 获取业务拓扑树
def tmp_get_app_topo(request):
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
