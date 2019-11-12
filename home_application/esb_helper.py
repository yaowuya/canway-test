# -*- coding: utf-8 -*-
'''
-------------------------------------------------
   File Name：     esb_helper
   Author :        zhongrf
   Date：          2019/10/25
-------------------------------------------------
'''
__author__ = 'zhongrf'

import base64
import sys
import time

from common.log import logger
from conf.default import APP_ID, APP_TOKEN
from blueking.component.shortcuts import get_client_by_user, get_client_by_request

reload(sys)
sys.setdefaultencoding("utf8")


def fast_execute_script(check_app, client, execute_account, script_content, script_type=1, param_content='',
                        script_timeout=1000):
    """
    快速执行脚本
    :param check_app: 操作的对象，dict，{"app_id":1,"ip_list":[{"ip":"10.0.0.10","bk_cloud_id":0}]}
    :param client: ESB连接客户端，client class
    :param execute_account: 脚本执行帐号，str
    :param script_content: 脚本执行内容，str
    :param script_type: 脚本类型，int, 1(shell脚本)、2(bat脚本)、3(perl脚本)、4(python脚本)、5(Powershell脚本)
    :param param_content: 脚本参数，str，可不传
    :param script_timeout: 超时时间，int，可不传
    :return: 脚本执行结果，list：[{"ip": '10.0.0.10', "log_content": '123', "bk_cloud_id": 0, "is_success": True}]
    """
    kwargs = {
        "bk_biz_id": check_app["bk_biz_id"],
        "script_content": base64.b64encode(script_content),
        "ip_list": check_app["ip_list"],
        "script_type": script_type,
        "account": execute_account,
        "script_param": base64.b64encode(param_content),
        "script_timeout": script_timeout
    }
    result = client.job.fast_execute_script(kwargs)
    if result["result"]:
        return {"result": True, "data": result["data"]["job_instance_id"]}

    else:
        return {"result": False, "data": result["message"]}


def get_task_ip_log(client, bk_biz_id, task_instance_id, count=0):
    """
    获取脚本执行结果
    :param client: ESB连接客户端，client class
    :param app_id: 业务ID，int
    :param task_instance_id: 作业实例ID，int
    :param user_name: 有查看该脚本执行结果权限的用户 ,str
    :param count: 已重试的次数，直接调用不传
    :return: 脚本执行结果，list：[{"ip": '10.0.0.10', "log_content": '123', "bk_cloud_id": 0, "is_success": True}]
    """
    kwargs = {
        "bk_biz_id": bk_biz_id,
        "job_instance_id": int(task_instance_id)
    }
    result = client.job.get_job_instance_log(kwargs)
    if not result["result"]:
        count += 1
        if count > 5:
            logger.error(result["message"])
            return []
        time.sleep(10)
        return get_task_ip_log(client, bk_biz_id, task_instance_id, count)
    if result["data"][0]["is_finished"]:
        log_content = []
        for i in result["data"][0]["step_results"]:
            log_content += [{"ip": u["ip"], "log_content": u["log_content"], "bk_cloud_id": u["bk_cloud_id"],
                             "is_success": i['ip_status'] == 9} for u in
                            i["ip_logs"]]
        return log_content
    time.sleep(10)
    return get_task_ip_log(client, bk_biz_id, task_instance_id)


def get_business_by_user(client, username):
    kwargs = {
        "bk_app_code": APP_ID,
        "bk_app_secret": APP_TOKEN,
        "bk_username": username
    }
    res = client.cc.search_business(kwargs)
    if res["result"]:
        user_business_list = [
            {"bk_biz_id": i["bk_biz_id"], "bk_biz_name": i["bk_biz_name"]} for i in res["data"]["info"]
            if username in i["bk_biz_maintainer"].split(",")
        ]
        return {"result": True, "data": user_business_list}
    return {"result": False, "data": res["data"]}


# client是通过get_client_by_user获取的
def fast_execute_script_by_user(check_app, username, execute_account, script_content, script_type=1, param_content='',
                                script_timeout=1000):
    """
    快速执行脚本
    :param check_app: 操作的对象，dict，{"app_id":1,"ip_list":[{"ip":"10.0.0.10","bk_cloud_id":0}]}
    :param username: 用户名
    :param execute_account: 脚本执行帐号，str
    :param script_content: 脚本执行内容，str
    :param script_type: 脚本类型，int, 1(shell脚本)、2(bat脚本)、3(perl脚本)、4(python脚本)、5(Powershell脚本)
    :param param_content: 脚本参数，str，可不传
    :param script_timeout: 超时时间，int，可不传
    :return: 脚本执行结果，list：[{"ip": '10.0.0.10', "log_content": '123', "bk_cloud_id": 0, "is_success": True}]
    """
    client = get_client_by_user(username)
    kwargs = {
        "bk_app_code": APP_ID,
        "bk_app_secret": APP_TOKEN,
        "bk_username": username,
        "bk_biz_id": check_app["bk_biz_id"],
        "script_content": base64.b64encode(script_content),
        "ip_list": check_app["ip_list"],
        "script_type": script_type,
        "account": execute_account,
        "script_param": base64.b64encode(param_content),
        "script_timeout": script_timeout
    }
    result = client.job.fast_execute_script(kwargs)
    if result["result"]:
        return {"result": True, "data": result["data"]["job_instance_id"]}

    else:
        return {"result": False, "data": result["message"]}


def get_task_ip_log_by_user(username, bk_biz_id, task_instance_id, count=0):
    """
    获取脚本执行结果
    :param username: 用户名
    :param app_id: 业务ID，int
    :param task_instance_id: 作业实例ID，int
    :param user_name: 有查看该脚本执行结果权限的用户 ,str
    :param count: 已重试的次数，直接调用不传
    :return: 脚本执行结果，list：[{"ip": '10.0.0.10', "log_content": '123', "bk_cloud_id": 0, "is_success": True}]
    """
    kwargs = {
        "bk_app_code": APP_ID,
        "bk_app_secret": APP_TOKEN,
        "bk_username": username,
        "bk_biz_id": bk_biz_id,
        "job_instance_id": int(task_instance_id)
    }
    client = get_client_by_user(username)
    result = client.job.get_job_instance_log(kwargs)
    if not result["result"]:
        count += 1
        if count > 5:
            logger.error(result["message"])
            return []
        time.sleep(10)
        return get_task_ip_log(client, bk_biz_id, task_instance_id, count)
    if result["data"][0]["is_finished"]:
        log_content = []
        for i in result["data"][0]["step_results"]:
            log_content += [{"ip": u["ip"], "log_content": u["log_content"], "bk_cloud_id": u["bk_cloud_id"],
                             "is_success": i['ip_status'] == 9} for u in
                            i["ip_logs"]]
        return log_content
    time.sleep(10)
    return get_task_ip_log(client, bk_biz_id, task_instance_id)
