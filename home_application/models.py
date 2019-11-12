# -*- coding: utf-8 -*-
from django.db import models
import datetime


class TaskModel(models.Model):
    name = models.CharField(max_length=200, null=True)
    business = models.CharField(max_length=200, null=True)
    type = models.CharField(max_length=200, null=True)
    creator = models.CharField(max_length=200, null=True)
    when_created = models.CharField(max_length=100, null=True)

    @classmethod
    def create_taskmodel(cls, **kwargs):
        when_created = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        kwargs["when_created"] = when_created
        task_model = cls(**kwargs)
        task_model.save()
        return task_model


class Template(models.Model):
    task_model = models.ForeignKey(TaskModel)
    num = models.IntegerField(null=True)
    operation = models.CharField(max_length=300, null=True)
    desc = models.CharField(max_length=500, null=True)
    person = models.CharField(max_length=20, null=True)
    when_created = models.DateTimeField(null=True)


class LogoImg(models.Model):
    key = models.CharField(max_length=100)
    value = models.BinaryField()


class File(models.Model):
    file_content = models.BinaryField(null=True)
    file_name = models.CharField(max_length=100, null=True)


class Host(models.Model):
    name = models.CharField(max_length=30, null=True)
    age = models.CharField(max_length=30, null=True)
    text = models.TextField(null=True)
    when_created = models.DateTimeField(null=True)


class HostData(models.Model):
    bk_biz_id = models.CharField(max_length=30, null=True)
    bk_set_id = models.CharField(max_length=30, null=True)
    bk_host_innerip = models.CharField(max_length=50, null=True)


class HostInfo(models.Model):
    bk_host_innerip = models.CharField(max_length=50)
    bk_biz_id = models.CharField(max_length=50, null=True)
    bk_cloud_id = models.CharField(max_length=50, null=True)
    bk_is_job = models.BooleanField(default=False)
    bk_admin = models.CharField(max_length=30)


class HostResource(models.Model):
    host_info = models.ForeignKey(HostInfo)
    bk_mem_rate = models.CharField(max_length=50, null=True)
    bk_disk_rate = models.CharField(max_length=50, null=True)
    bk_cpu_rate = models.CharField(max_length=50, null=True)
    bk_date = models.CharField(max_length=50, null=True)
