# -*- coding: utf-8 -*-
"""
celery 任务示例

本地启动celery命令: python  manage.py  celery  worker  --settings=settings
周期性任务还需要启动celery调度命令：python  manage.py  celerybeat --settings=settings
"""
import datetime

from celery import task
from celery.schedules import crontab
from celery.task import periodic_task

from common.log import logger

from blueking.component.shortcuts import get_client_by_user, get_client_by_request
from home_application.esb_helper import *
from home_application.models import *


@task()
def async_task(x, y):
    """
    定义一个 celery 异步任务
    """
    logger.error(u"celery 定时任务执行成功，执行结果：{:0>2}:{:0>2}".format(x, y))
    return x + y


def execute_task():
    """
    执行 celery 异步任务

    调用celery任务方法:
        task.delay(arg1, arg2, kwarg1='x', kwarg2='y')
        task.apply_async(args=[arg1, arg2], kwargs={'kwarg1': 'x', 'kwarg2': 'y'})
        delay(): 简便方法，类似调用普通函数
        apply_async(): 设置celery的额外执行选项时必须使用该方法，如定时（eta）等
                      详见 ：http://celery.readthedocs.org/en/latest/userguide/calling.html
    """
    now = datetime.datetime.now()
    logger.error(u"celery 定时任务启动，将在60s后执行，当前时间：{}".format(now))
    # 调用定时任务
    async_task.apply_async(args=[now.hour, now.minute], eta=now + datetime.timedelta(seconds=60))


@periodic_task(run_every=crontab(minute='*/5', hour='*', day_of_week="*"))
def get_time():
    """
    celery 周期任务示例

    run_every=crontab(minute='*/5', hour='*', day_of_week="*")：每 5 分钟执行一次任务
    periodic_task：程序运行时自动触发周期任务
    """
    execute_task()
    now = datetime.datetime.now()
    logger.error(u"celery 周期任务调用成功，当前时间：{}".format(now))


@task()
def run_celery(client):
    check_app = {
        'bk_biz_id': 3,
        'ip_list': [{
            'ip': '192.168.165.11',
            'bk_cloud_id': 0
        }]
    }
    execute_account = 'root'
    script_content = 'echo 123'
    result = fast_execute_script(check_app, client, execute_account, script_content)
    log_result = get_task_ip_log(client, check_app["bk_biz_id"], result['data'])
    return log_result


@periodic_task(run_every=crontab(minute='*/1', hour='*', day_of_week="*"))
def run_host_resource():
    try:
        host_obj = HostInfo.objects.filter(bk_is_job=True)
        for host in host_obj:
            check_app = {
                'bk_biz_id': host.bk_biz_id,
                'ip_list': [{
                    'ip': host.bk_host_innerip,
                    'bk_cloud_id': host.bk_cloud_id
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
            result = fast_execute_script_by_user(check_app, host.bk_admin, execute_account, script_content)
            log_result = get_task_ip_log_by_user(host.bk_admin, check_app["bk_biz_id"], result['data'])

            if log_result[0]["is_success"]:
                content_array = log_result[0]["log_content"].split("|")
                HostResource.objects.create(host_info=host,
                                            bk_date=content_array[0].replace("%",""),
                                            bk_mem_rate=content_array[1].replace("%",""),
                                            bk_disk_rate=content_array[2].replace("%",""),
                                            bk_cpu_rate=content_array[3].replace("%",""))
                logger.info(u"run_host_resource 定时任务启动，将在60s后执行，当前时间：{}".format(datetime.datetime.now()))
    except Exception, e:
        print e
