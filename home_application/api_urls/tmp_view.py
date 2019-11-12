# -*- coding: utf-8 -*-
'''
-------------------------------------------------
   File Name：     tmp_view
   Author :        zhongrf
   Date：          2019/10/25
-------------------------------------------------
'''
__author__ = 'zhongrf'

from django.conf.urls import patterns

urlpatterns = patterns(
    'home_application.api.tmp_view',
    (r'^api/test/$', 'tmp_test'),
    (r'^test_celery$', 'test_celery'),
    (r'^tmp_get_biz$', 'tmp_get_biz'),
    (r'^tmp_get_set$', 'tmp_get_set'),
    (r'^tmp_get_host$', 'tmp_get_host'),
    (r'^tmp_add_host$', 'tmp_add_host'),
    (r'^tmp_get_hostList$', 'tmp_get_hostList'),
    (r'^tmp_query_resource$', 'tmp_query_resource'),
    (r'^tmp_add_queue$', 'tmp_add_queue'),
    (r'^tmp_remove_queue$', 'tmp_remove_queue'),
    (r'^tmp_query_host_resource$', 'tmp_query_host_resource'),
    (r'^tmp_get_app_topo$', 'tmp_get_app_topo'),
)