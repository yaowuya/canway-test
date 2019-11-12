# -*- coding: utf-8 -*-

from django.conf.urls import patterns

urlpatterns = patterns(
    'home_application.views',
    (r'^$', 'home'),
    # (r'^/api/test$', 'test'),

    (r'^get_task_model$', 'get_task_model'),
    (r'^delete_task_template$', 'delete_task_template'),
    (r'^update_task_template$', 'update_task_template'),
    # 获取业务信息
    (r'^get_app_list$', 'get_app_list'),
    # excel文件
    (r'^upload_file_form/$', 'upload_file_form'),
    (r'^upload_img/$', 'upload_img'),
    (r'^show_img/$', 'show_img'),
    (r'^down_img/$', 'down_img'),
    # 上传普通文件存入数据库，从数据库读取普通文件下载到本地
    (r'^upload_file/$', 'upload_file'),
    (r'^download_common_file/$', 'download_common_file'),
    (r'^upload_info/$', 'upload_info'),
    (r'^down_load_field/$', 'down_load_field'),
    # 导入、导出csv
    (r'^down_csv/$', 'down_csv'),
    (r'^up_csv$', 'up_csv'),
    # 导入、导出excel文件
    (r'^up_excel/$', 'up_excel'),
    (r'^down_excel/$', 'down_excel'),
)
# 考试把下面的删除即可
from home_application.api_urls import tmp_view,test3

urlpatterns += tmp_view.urlpatterns
urlpatterns += test3.urlpatterns
