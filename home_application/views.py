# -*- coding: utf-8 -*-
import math

from django.http import HttpResponse, JsonResponse
from common.mymako import render_mako_context, render_json
from blueking.component.shortcuts import get_client_by_request, get_client_by_user
from conf.default import APP_ID, APP_TOKEN, BK_PAAS_HOST
from django.db.models import Q
from home_application.models import *
from helper import *
from other_helper import *
from esb_api import *


import datetime
import json


def home(request):
    """
    首页
    """
    return render_mako_context(request, '/home_application/js_factory.html')


def test(request):
    params = request.GET
    result = {}
    for p in params:
        result[p] = params[p]

    return JsonResponse({"result": True, "message": "success", "data": result})


def get_app_list(request):
    client = get_client_by_request(request)
    result = get_business_by_user(client, request.user.username)
    return JsonResponse(result)


def get_business_by_user(client, username):
    res = client.cc.search_business()
    if res["result"]:
        user_business_list = [{"bk_biz_id": i["bk_biz_id"], "bk_biz_maintainer": i["bk_biz_maintainer"],
                               "bk_biz_name": i["bk_biz_name"]} for i in res["data"]["info"]
                              if username in i["bk_biz_maintainer"].split(",")
                              ]
        return {"result": True, "data": user_business_list}
    else:
        return {"result": False, "data": res["data"]}


# 查询
def get_task_model(request):
    try:
        params = json.loads(request.body)
        name = params["name"]
        business = params["business"]
        type = params["type"]
        when_start = params["whenStart"] + " 00:00:00"
        when_end = params["whenEnd"] + " 23:59:59"

        pageSize = int(params["pageOption"]["pageSize"])
        pageNum = int(params["pageOption"]["pageNum"])
        pageOption = paging(pageSize, pageNum)

        task_obj = TaskModel.objects.filter(
            Q(business__contains=business) & Q(type__contains=type) & Q(name__contains=name) & Q(
                when_created__range=(when_start, when_end)))
        result_data = list(task_obj[pageOption[0]:pageOption[1]].values())
        allLen = task_obj.count()
        page_num = math.ceil(allLen / float(pageSize))
        return JsonResponse({'result': True, 'data': result_data, 'allLen': allLen, 'pageNum': page_num})
    except Exception, e:
        print e
        return JsonResponse({"result": False, "data": str(e)})


# 新增
def upload_file_form(request):
    try:
        params = json.loads(request.GET.get("params"))
        params["creator"] = request.user.username
        task_model = TaskModel.create_taskmodel(**params)
        error_list = up_excel_template(request, task_model)
        if len(error_list) > 0:
            return JsonResponse({'result': False, 'error': '、'.join(error_list)})
        return JsonResponse({"result": True})
    except Exception, e:
        print e
        return JsonResponse({"result": False, "data": str(e)})


# 删除
def delete_task_template(request):
    try:
        id = json.loads(request.body)["id"]
        task_obj = TaskModel.objects.get(id=id)
        task_obj.delete()
        return JsonResponse({"result": True})
    except Exception, e:
        print e
        return JsonResponse({"result": False, "data": str(e)})


# 修改
def update_task_template(request):
    try:
        params = json.loads(request.body)
        # TaskModel.objects.update_or_create(name=params["name"], business=params["business"], type=params["type"],
        #                                    creator=request.user.username,
        #                                    when_created=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        #                                    defaults={"id": params["id"]})  #不能用id做判断
        TaskModel.objects.filter(id=params["id"]).update(name=params["name"],
                                                       business=params["business"],
                                                       type=params["type"],
                                                       creator=request.user.username,
                                                       when_created=datetime.datetime.now().strftime(
                                                           "%Y-%m-%d %H:%M:%S"))
        return JsonResponse({"result": True})
    except Exception, e:
        print e
        return JsonResponse({"result": False, "data": str(e)})

