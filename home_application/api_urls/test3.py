# -*- coding: utf-8 -*-
'''
-------------------------------------------------
   File Name：     test3
   Author :        zhongrf
   Date：          2019/11/2
-------------------------------------------------
'''
__author__ = 'zhongrf'
from django.conf.urls import patterns
urlpatterns = patterns(
    'home_application.api.test3',
    (r'^test3_get_biz$', 'test3_get_biz'),
    (r'^test3_get_app_topo$', 'test3_get_app_topo'),
    (r'^test3_get_host_ip$', 'test3_get_host_ip'),
    (r'^test3_get_joblist$', 'test3_get_joblist'),
    (r'^test3_get_fileinfo$', 'test3_get_fileinfo'),
)