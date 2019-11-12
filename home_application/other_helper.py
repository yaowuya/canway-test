# -*- coding: utf-8 -*-
'''
-------------------------------------------------
   File Name：     other_helper
   Author :        zhongrf
   Date：          2019/10/22
-------------------------------------------------
'''
__author__ = 'zhongrf'

import StringIO
import base64
import codecs
import csv
import json
import os
import sys
import time
import datetime

import xlrd
import xlsxwriter
from common.log import logger
from common.mymako import render_json
from django.http import FileResponse, HttpResponse, JsonResponse
from home_application.models import Template, LogoImg, File,Host
from conf.default import STATIC_URL, PROJECT_ROOT, IMG_FILE

"""导入excel文件，写入数据库"""


def up_excel_template(request, task_model):
    name = "file%s.xls" % (time.time())
    file = open(name, 'wb')
    file.write(request.FILES['files'].read())
    file.close()

    data = xlrd.open_workbook(name)
    table = data.sheets()[0]
    nrows = table.nrows
    # 对应数据库的字段
    index_list = ['num', 'operation', 'desc', 'person']
    data_list = []
    # 从excel文件第几行开始读取数据
    for i in range(1, nrows):
        data_dict = {}
        table_row_value = table.row_values(i)
        for g in range(table_row_value.__len__()):
            data_dict[index_list[g]] = table_row_value[g]
        data_list.append(data_dict)
    error_list = []
    try:
        for g in data_list:
            try:
                # excel_demo = Excel_Demo.objects.filter(InstanceId=g['InstanceId'])
                # if excel_demo:
                #     excel_demo.update(**g)
                # else:
                g['when_created'] = datetime.datetime.now()
                g["task_model"] = task_model
                Template.objects.create(**g)
            except Exception, e:
                print e
                error_list.append(g['PrivateIpAddress'])
    except Exception, e:
        print e
    os.remove(name)
    return error_list


def up_excel(request):
    name = "file%s.xls" % (time.time())
    file = open(name, 'wb')
    file.write(request.FILES['files'].read())
    file.close()

    data = xlrd.open_workbook(name)
    table = data.sheets()[0]
    nrows = table.nrows
    # 对应数据库的字段
    index_list = ['num', 'operation', 'desc', 'person']
    data_list = []
    # 从excel文件第几行开始读取数据
    for i in range(1, nrows):
        data_dict = {}
        table_row_value = table.row_values(i)
        for g in range(table_row_value.__len__()):
            data_dict[index_list[g]] = table_row_value[g]
        data_list.append(data_dict)
    error_list = []
    try:
        for g in data_list:
            try:
                # excel_demo = Excel_Demo.objects.filter(InstanceId=g['InstanceId'])
                # if excel_demo:
                #     excel_demo.update(**g)
                # else:
                g['when_created'] = datetime.datetime.now()
                g["task_model"] = None
                Template.objects.create(**g)
            except Exception, e:
                print e
                error_list.append(g['PrivateIpAddress'])
    except Exception, e:
        print e
    os.remove(name)
    if error_list.__len__() == 0:
        return JsonResponse({"result": True})
    else:
        return JsonResponse({'result': False, 'error': '、'.join(error_list)})


def down_excel(request):
    id = request.GET.get("id")
    template = Template.objects.filter(task_model_id=id)
    title_data = [u"步骤序号", u"操作事项", u"备注", u'责任人', u'创建时间']
    data_list = [[tmp.num, tmp.operation, tmp.desc, tmp.person, tmp.when_created.strftime("%Y-%m-%d %H:%M:%S")] for tmp
                 in template]
    return make_excel(title_data, data_list, "checkList")


# 生成Excel文件
def make_excel(title_list, data_list, get_file_name):
    sio = StringIO.StringIO()
    workbook = xlsxwriter.Workbook(sio)
    worksheet = workbook.add_worksheet()
    header_format = workbook.add_format({
        'num_format': '@',
        'text_wrap': True,
        'valign': 'vcenter',
        'indent': 1,
    })
    index = 0
    if title_list:
        index = 1
        for col, i in enumerate(title_list):
            worksheet.write(0, col, i)

    for row, i in enumerate(data_list):
        for col, j in enumerate(i):
            # worksheet.set_column(col, col, 30)
            if type(j) == dict:
                if "validate" in j.keys():
                    worksheet.data_validation(row + index, col, row + index, col,
                                              {"validate": j["validate"], "source": j["source"]})
                    worksheet.write(row + index, col, j["value"], header_format)
            else:
                worksheet.write(row + index, col, j)
    workbook.close()
    sio.seek(0)
    response = HttpResponse(sio.getvalue(), content_type='APPLICATION/OCTET-STREAM')
    file_name = 'attachment; filename={0}.xlsx'.format(get_file_name)
    response['Content-Disposition'] = file_name
    return response


# 上传图片
def upload_img(request):
    file_img = request.FILES["upfile"]
    content = base64.b64encode(file_img.read())
    LogoImg.objects.filter(key="logo").update(value=content)
    return JsonResponse({"result": True})


# 展示图片
def show_img(request):
    param = request.GET.get("param")
    file_one = open(IMG_FILE, "rb")
    logo_obj, _ = LogoImg.objects.get_or_create(key=param, defaults={"value": base64.b64encode(file_one.read())})
    file_one.close()
    photo_data = base64.b64decode(logo_obj.value)
    response = HttpResponse(photo_data, content_type='image/png')
    response['Content-Length'] = len(photo_data)
    return response


# 下载图片
def down_img(request):
    param = request.GET.get("param")
    obj = LogoImg.objects.get(key=param)
    photo_data = base64.b64decode(obj.value)
    response = HttpResponse(photo_data, content_type='image/png')
    file_name = 'attachment; filename={0}.png'.format(param)
    response['Content-Disposition'] = file_name
    return response


"""第一种方法"""
"""上传普通文件,保存在static目录下，新的名字为test_文件名"""


def upload_info(request):
    try:
        obj_id = int(request.GET.get("obj_id"))
        file_path_name = request.POST.get("file_path")
        upload_info_folder = sys.path[0] + STATIC_URL

        file_one = request.FILES.get('upfile')
        name = file_one.name
        real_name = file_path_name + name
        """可以把文件名保存在数据库对应不同的对象"""
        file_new = open(os.path.join(upload_info_folder, real_name), 'wb')
        file_new.write(file_one.read())
        file_new.close()
        return render_json({"result": True})
    except Exception, e:
        logger.error(e)
        return render_json({"result": False, "data": [u"上传文件失败！"]})


"""从static下载对应名字的文件"""


def down_load_field(request):
    obj_id = request.GET.get('obj_id')
    # 获取对象对应的文件
    # field_name = Host.objects.get(id=obj_id).field_name
    field_name = 'test_test_linux.txt'
    # 目录
    upload_info_folder = sys.path[0] + STATIC_URL
    file = open(os.path.join(upload_info_folder, field_name), 'rb')
    response = FileResponse(file)
    response['Content-Type'] = 'application/*'
    response['Content-Disposition'] = 'attachment;filename=' + field_name
    return response


"""第二种方法"""
"""上传普通文件存入数据库"""


def upload_file(request):
    try:
        file_obj = request.FILES.get('upfile', '')
        name = file_obj.name
        content = file_obj.read()
        file = File.objects.create(file_name=name, file_content=content)
        return render_json({"result": True, 'file_id': file.id})
    except Exception as e:
        return render_json({'result': False})


"""从数据库读取普通文件下载到本地"""


def download_common_file(request):
    file_obj = File.objects.filter(id=2).first()
    if not file_obj:
        return render_json({"result": False, 'data': u"无模板"})
    file_content = file_obj.file_content
    file_name = file_obj.file_name
    response = HttpResponse(file_content, content_type='APPLICATION/OCTET-STREAM')
    response['Content-Disposition'] = 'attachment; filename=' + file_name.encode("utf8")
    response['Content-Length'] = len(file_content)
    return response

"""导出csv"""
def down_csv(request):
    try:
        obj_id = request.GET.get("obj_id")
        data_list = []
        host = Host.objects.get(id=obj_id)

        data_list.append([
            host.name, host.age, host.text, host.when_created.strftime("%Y-%m-%d %H:%M:%S")
        ])
        f = codecs.open('Host-Info.csv', 'wb', "gbk")
        writer = csv.writer(f)
        writer.writerow([u"姓名",u"年龄", u"内容",u"时间"])
        writer.writerows(data_list)
        f.close()
        file_path = "{0}/Host-Info.csv".format(PROJECT_ROOT).replace("\\", "/")
        file_name = "Host-Info.csv"
        return download_file(file_path, file_name)

    except Exception as e:
        logger.exception('download cvs file error:{0}'.format(e.message))
        return HttpResponse('导出失败！')


def download_file(file_path, file_name):
    try:
        file_path = file_path
        file_buffer = open(file_path, 'rb').read()
        response = HttpResponse(file_buffer, content_type='APPLICATION/OCTET-STREAM')
        response['Content-Disposition'] = 'attachment; filename=' + file_name
        response['Content-Length'] = os.path.getsize(file_path)
        return response
    except Exception as e:
        logger.exception("download file error:{0}".format(e.message))



"""导入csv"""
def up_csv(request):
    try:
        username = request.user.username
        up_data = json.loads(request.body)
        # kaoshi_id = up_data[0]['kaoshi_id']
        # host = Host.objects.get(id=kaoshi_id)
        for data in up_data:
            Host.objects.create(name=data['name'], text=data['text'], age=data['age'], when_created=datetime.datetime.now())
        return render_json({"result": True})
    except Exception as e:
        return render_json({'result': False})