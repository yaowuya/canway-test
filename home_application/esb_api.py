# -*- coding: utf-8 -*-
import base64
import json
import time

from blueking.component.shortcuts import get_client_by_user, get_client_by_request
from common.log import logger
from common.mymako import render_json
from conf.default import APP_ID, APP_TOKEN


# 查询所有的业务 [{"id": 2, "text": "蓝鲸"}]
def get_all_biz(request):
    try:
        username = request.user.username
        client = get_client_by_request(request)
        result = client.cc.search_business()
        user_business_list = []
        if result["result"]:
            user_business_list = [
                {"id": i["bk_biz_id"], "text": i["bk_biz_name"]} for i in result["data"]["info"] if
                username in i["bk_biz_maintainer"].split(",")
            ]
        return render_json({"result": True, "data": user_business_list})
    except Exception, e:
        return render_json({"result": False, "msg": [u"查询业务失败!!"]})


# 获取主机的全部属性
def get_host_attr(request):
    client = get_client_by_user(request)
    param = {
        "bk_app_code": APP_ID,
        "bk_app_secret": APP_TOKEN,
        "bk_username": 'admin',
        "bk_obj_id": 'host'
    }
    result = client.cc.search_object_attribute(param)
    return_data = []
    if result['result']:
        for i in result['data']:
            return_data.append({'id': i['bk_property_id'], 'text': i['bk_property_name']})
    return render_json({"result": True, 'data': return_data})


# @TryException(u'获取主机的全部属性')
# def get_host_attr(request):
#     client = get_client_by_request(request)
#     result = client.cc.search_object_attribute({'bk_obj_id': 'host'})
#     return render_json({"result": True, 'data': [{'id': i['bk_property_id'], 'text': i['bk_property_name']} for i in result['data']]
#                         })


# 主机系统类型
OS_TYPE = {'1': 'Linux', '2': 'Windows'}


def search_server_list(request):
    filter_obj = eval(request.body)
    bk_biz_id = request.GET["bk_biz_id"]
    client = get_client_by_request(request)
    if filter_obj["bk_obj_id"] not in ['biz', 'module', 'set']:
        filter_obj["bk_obj_id"] = 'object'
        condition = [{"field": "bk_inst_id", "operator": "$eq", "value": int(filter_obj["value"])}]
    else:
        condition = [
            {"field": "bk_%s_id" % filter_obj["bk_obj_id"], "operator": "$eq", "value": int(filter_obj["value"])}]
    kwargs = {
        'bk_biz_id': bk_biz_id,
        "condition": [
            {
                "bk_obj_id": filter_obj["bk_obj_id"],
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
        i['host']['bk_cloud_id'] = i['host']['bk_cloud_id'][0]['bk_inst_name']
        return_data.append(i['host'])
    return render_json({"result": True, 'data': return_data})


# 只获取集群模块
def get_app_topo(request):
    app_id = request.GET["app_id"]
    client = get_client_by_request(request)
    result = client.cc.search_biz_inst_topo({
        'bk_biz_id': app_id, 'level': -1
    })
    return_data = result["data"]
    for i in return_data:
        set_data = get_set_data(i)
        i["child"] = set_data
        format_is_parent(i)
    return render_json({"result": True, 'data': result["data"]})


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


# 获取所有的topo节点
def get_all_app_topo(request):
    app_id = request.GET["app_id"]
    client = get_client_by_request(request)
    result = client.cc.search_biz_inst_topo({
        'bk_biz_id': app_id, 'level': -1
    })
    if result['result']:
        get_inst_of_same_level(result['data'])
    return render_json({"result": True, 'data': result["data"]})


def get_inst_of_same_level(children):
    """获取所有的层级"""
    for child in children:
        if child['child']:
            child['isParent'] = True
        else:
            child['isParent'] = False
        get_inst_of_same_level(child['child'])


# 查询业务下的所有主机
def get_host_by_biz(request):
    try:
        client = get_client_by_user(request.user.username)
        request_data = json.loads(request.body)

        kwargs = {
            "bk_app_code": APP_ID,
            "bk_app_secret": APP_TOKEN,
            "bk_username": 'admin',
            "ip": {"flag": "bk_host_innerip|bk_host_outerip", "exact": 1, "data": []},

            "condition": [
                {
                    "bk_obj_id": "biz",
                    "fields": [
                        "default",
                        "bk_biz_id",
                        "bk_biz_name",
                    ],
                    # 根据业务ID查询主机
                    "condition": [
                        {
                            "field": "bk_biz_id",
                            "operator": "$eq",
                            "value": int(request_data['biz_id'])
                        }
                    ]
                },

                {
                    "bk_obj_id": "module",
                    "fields": [],
                    "condition": []
                },

                {
                    "bk_obj_id": "set",
                    "fields": [],
                    "condition": []
                },
            ]
        }
        result = client.cc.search_host(kwargs)
        host_list = []
        if result["result"]:
            for i in result['data']['info']:
                host_list.append({
                    'id': i['host']['bk_host_innerip'],
                    'text': i['host']['bk_host_innerip'],
                    'biz_id': i['biz'][0]['bk_biz_id'],
                    'bk_cloud_id': i['host']['bk_cloud_id'][0]['id'],
                    'area': i['host']['bk_cloud_id'][0]['bk_inst_name'],
                })

        return render_json({"result": True, "data": host_list})
    except Exception as e:
        logger.error(e)


# 获取脚本任务Log
def get_ip_log_content(client, username, task_id, biz_id, i=1):
    kwargs = {
        "app_code": APP_ID,
        "app_secret": APP_TOKEN,
        "username": username,
        "job_instance_id": task_id,
        'bk_biz_id': biz_id
    }
    result = client.job.get_job_instance_log(kwargs)
    if result["result"]:
        if result["data"][0]["is_finished"]:
            ip_log_content = []
            for i in result["data"][0]["step_results"]:
                if i["ip_status"] == 9:
                    result_op = True
                else:
                    result_op = False
                for z in i['ip_logs']:
                    ip_log_content.append({
                        'result': result_op,
                        'ip': z['ip'],
                        'bk_cloud_id': z['bk_cloud_id'],
                        'log_content': z['log_content'],
                    })
            return {"result": True, "data": ip_log_content}
        else:
            time.sleep(1)
            return get_ip_log_content(client, username, task_id, kwargs['bk_biz_id'])
    else:
        i += 1
        if i < 5:
            time.sleep(1)
            return get_ip_log_content(client, username, task_id, kwargs['bk_biz_id'])
        else:
            err_msg = "get_logContent_timeout;task_id:%s;err_msg:%s" % (task_id, result["message"])

            return render_json({"result": False, "msg": err_msg})


# 执行脚本接口
def excute_by_script(username, biz_id, ip_list, script_content, script_type=1, script_timeout=600):
    client = get_client_by_user(username)
    #   app_list=[{'ip':'192.168.165.51','bk_cloud_id':'2'}]
    kwargs = {
        "bk_app_code": APP_ID,
        "bk_app_secret": APP_TOKEN,
        "bk_biz_id": int(biz_id),
        "bk_username": username,
        "script_content": base64.b64encode(script_content),
        "ip_list": ip_list,
        "script_type": script_type,
        "account": 'root',
        "script_timeout": script_timeout
    }
    """
    查询某个目录下以txt结尾的文件，并统计大小
    cd /data || exit
    du -ch *.txt

    """

    result = client.job.fast_execute_script(kwargs)
    if result["result"]:
        task_id = result["data"]["job_instance_id"]
        time.sleep(2)
        return get_ip_log_content(client, username, task_id, biz_id)
    else:
        return {"result": False, "data": result["message"]}


# 快速分发脚本
def fast_push_file(instance_info, username, install_info):
    kwargs = {
        "bk_app_code": APP_ID,
        "bk_app_secret": APP_TOKEN,
        "bk_username": "admin",
        "bk_biz_id": 2,
        "file_target_path": "/tmp/[FILESRCIP]/",
        "file_source": [
            {
                "files": [
                    "/tmp/REGEX:[a-z]*.txt"
                ],
                "account": "root",
                "ip_list": [
                    {
                        "bk_cloud_id": 0,
                        "ip": "10.0.0.1"
                    }
                ],
                "custom_query_id": []
            }
        ],
        "ip_list": [
            {
                "bk_cloud_id": 0,
                "ip": "10.0.0.1"
            }
        ],
        "custom_query_id": [],
        "account": "root",
    }

    client = get_client_by_user(username)
    result = client.job.fast_push_file(kwargs)
    if result["result"]:
        task_id = result["data"]["taskInstanceId"]
        time.sleep(2)
        return get_ip_log_content(client, username, task_id, 2)
    else:
        return {"result": False, "data": result["message"]}


# 获取平台所有的用户
def get_all_user(request):
    try:
        client = get_client_by_user(request.user.username)
        param = {
            "bk_app_code": APP_ID,
            "bk_app_secret": APP_TOKEN,
            "bk_username": 'admin',

            # "bk_role": 0   用户角色，0：普通用户，1：超级管理员，2：开发者，3：职能化用户，4：审计员
        }
        result = client.bk_login.get_all_users(param)
        user_business_list = []
        if result["result"]:
            user_business_list = [
                {"id": i["bk_username"], "text": i["bk_username"]} for i in result["data"]
            ]
        return render_json({"result": True, "data": user_business_list})
    except Exception as e:
        logger.error(e)


# 获取当前用户信息
def get_current_user(request):
    try:
        client = get_client_by_user(request.user.username)
        param = {
            "bk_app_code": APP_ID,
            "bk_app_secret": APP_TOKEN,
            "bk_username": request.user.username

            # "bk_role": 0   用户角色，0：普通用户，1：超级管理员，2：开发者，3：职能化用户，4：审计员
        }
        result = client.bk_login.get_user(param)
        data = {}
        if result["result"]:
            data = result['data']
        return render_json({"result": True, "data": data})
    except Exception as e:
        logger.error(e)


# 根据ip获取主机详情
def get_host_info(request):
    try:
        client = get_client_by_user(request.user.username)
        request_data = json.loads(request.body)
        ip = '1' if request_data.get('ip', '') else '10.0.1.45'
        kwargs = {
            "bk_app_code": APP_ID,
            "bk_app_secret": APP_TOKEN,
            "bk_username": 'admin',
            "ip": {"flag": "bk_host_innerip|bk_host_outerip", "exact": 1, "data": [ip]},

            "condition": [
                {
                    "bk_obj_id": "biz",
                    "fields": [],
                    # 根据业务ID查询主机
                    "condition": []
                },

                {
                    "bk_obj_id": "module",
                    "fields": [],
                    "condition": []
                },

                {
                    "bk_obj_id": "set",
                    "fields": [],
                    "condition": []
                },
            ]
        }
        result = client.cc.search_host(kwargs)
        host_list = []
        if result["result"]:
            for i in result['data']['info']:
                host_list.append({
                    'id': i['host']['bk_host_innerip'],
                    'text': i['host']['bk_host_innerip'],
                    'biz_id': i['biz'][0]['bk_biz_id'],
                    'bk_cloud_id': i['host']['bk_cloud_id'][0]['id'],
                    'area': i['host']['bk_cloud_id'][0]['bk_inst_name'],
                })

        return render_json({"result": True, "data": host_list})
    except Exception as e:
        logger.error(e)


# 查询不属于该业务下所有主机
def search_all_host_by_biz(request):
    try:
        client = get_client_by_user(request.user.username)
        kwargs = {
            "bk_app_code": APP_ID,
            "bk_app_secret": APP_TOKEN,
            "bk_username": 'admin',
            "ip": {"flag": "bk_host_innerip|bk_host_outerip", "exact": 1, "data": []},
            "condition": [
                {
                    "bk_obj_id": "biz",
                    "fields": [
                        "default",
                        "bk_biz_id",
                        "bk_biz_name",
                    ],
                    # 根据业务ID查询主机
                    "condition": [{"field": "bk_biz_id", "operator": "$nin", "value": 6}]
                }
            ]
        }
        result = client.cc.search_host(kwargs)
        host_list = []
        if result["result"]:
            for i in result['data']['info']:
                host_list.append({
                    'id': i['host']['bk_host_id'],
                    'text': i['host']['bk_host_innerip']
                })
        return render_json({"result": True, "data": host_list})
    except Exception as e:
        logger.error(e)


# 获取平台所有模型, 如：主机管理，业务拓扑，组织架构
def search_classifications(request):
    try:
        client = get_client_by_user(request.user.username)
        param = {
            "bk_app_code": APP_ID,
            "bk_app_secret": APP_TOKEN,
            "bk_username": 'admin'
        }
        result = client.cc.search_classifications(param)
        data_list = []
        if result['result']:
            for i in result['data']:
                data_list.append({
                    "id": i['bk_classification_id'],
                    "text": i['bk_classification_name']
                })
        return render_json({'result': True, 'data': data_list})
    except Exception as e:
        logger.error(e)


# 获取该模型分类下的所有模型，如： 业务拓扑，bk_biz_topo ,查询结果为集群、模块等
def search_all_objects(request):
    try:
        client = get_client_by_user(request.user.username)
        param = {
            "bk_app_code": APP_ID,
            "bk_app_secret": APP_TOKEN,
            "bk_username": 'admin',
            'bk_classification_id': 'bk_biz_topo'
        }
        result = client.cc.search_objects(param)
        data_list = []
        if result['result']:
            for i in result['data']:
                data_list.append({
                    "id": i['bk_obj_id'],
                    "text": i['bk_obj_name']
                })
        return render_json({'result': True, 'data': data_list})
    except Exception as e:
        logger.error(e)


# 获取该模型下所有的实例,例如 集群：set 的所有实例
def search_inst(request):
    try:
        client = get_client_by_user(request.user.username)
        param = {
            "bk_app_code": APP_ID,
            "bk_app_secret": APP_TOKEN,
            "bk_username": 'admin',
            'bk_obj_id': 'set',
            'condition': {},
            'bk_supplier_account': '0'
        }
        result = client.cc.search_inst(param)
        inst_data = []
        if result['result']:
            for i in result['data']['info']:
                inst_data.append({"id": i['bk_set_id'], 'text': i['bk_set_name']})

        return render_json({'result': True, 'data': inst_data})
    except Exception as e:
        logger.error(e)


# 根据实例名获取实例详情,例如集群中的一个实例 故障自愈
def search_inst_detail(request):
    try:
        client = get_client_by_user(request.user.username)
        param = {
            "bk_app_code": APP_ID,
            "bk_app_secret": APP_TOKEN,
            "bk_username": 'admin',
            "bk_obj_id": "set",
            "page": {"start": 0, "limit": 0, "sort": "-bk_inst_id"},
            "fields": {},
            "condition": {'bk_inst_name': u'故障自愈'}
        }
        result = client.cc.search_inst_by_object(param)
        inst_data = {}
        if result['result']:
            inst_data = {'inst_id': result['data']['info'][0]['bk_inst_id']}
        return render_json({'result': True, 'data': inst_data})
    except Exception as e:
        logger.error(e)


# 查询主机的agent状态
def get_agent_status(request):
    try:
        client = get_client_by_user(request.user.username)
        param = {
            "bk_app_code": APP_ID,
            "bk_app_secret": APP_TOKEN,
            "bk_username": 'admin',
            "bk_supplier_account": '0',
            "hosts": [{"ip": "10.0.1.45", "bk_cloud_id": 0}],

        }
        result = client.gse.get_agent_status(param)
        inst_data = {}
        status = 0
        if result['result']:
            key = "%d:%s" % (param['hosts'][0]['bk_cloud_id'], param['hosts'][0]['ip'])
            status = result['data'][key]['bk_agent_alive']
        return render_json({'result': True, 'data': status})
    except Exception as e:
        logger.error(e)


# 查询作业模板详情，获取脚本信息等
def get_job_detail(request):
    try:
        client = get_client_by_user(request.user.username)
        param = {
            "bk_app_code": APP_ID,
            "bk_app_secret": APP_TOKEN,
            "bk_username": 'admin',
            "bk_biz_id": 2,
            "bk_job_id": 1040,

        }
        result = client.job.get_job_detail(param)

        if result['result']:
            script = result['data']['steps'][0]['script_content']
        return render_json({'result': True, 'data': {}})
    except Exception as e:
        logger.error(e)


# 根据模板id执行作业
def execute_job(request):
    try:
        client = get_client_by_user(request.user.username)
        param = {
            "bk_app_code": APP_ID,
            "bk_app_secret": APP_TOKEN,
            "bk_username": 'admin',
            "bk_biz_id": 2,
            "bk_job_id": 1037,

        }
        result = client.job.get_job_detail(param)
        steps = result['data']['steps']

        steps[0]['ip_list'] = [{'ip': '10.0.1.28', 'bk_cloud_id': 0}]
        steps[0]['script_param'] = base64.b64encode("/data txt backup.tar.gz")
        steps[1]['file_source'] = [
            {'account': 'root', 'files': ['/data/backup.tar.gz'], 'ip_list': [{'ip': '10.0.1.28', 'bk_cloud_id': 0}]}]
        steps[1]['ip_list'] = [{'ip': '10.0.1.19', 'bk_cloud_id': 0}]

        param['bk_job_id'] = 1037
        param['steps'] = steps

        job_detail = client.job.execute_job(param)

        if result['result']:
            log_detail = get_ip_log_content(client, request.user.username, job_detail['data']['job_instance_id'], 2)

        return render_json({'result': True, 'data': {}})
    except Exception as e:
        logger.error(e)
