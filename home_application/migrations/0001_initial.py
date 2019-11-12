# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='File',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('file_content', models.BinaryField(null=True)),
                ('file_name', models.CharField(max_length=100, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Host',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=30, null=True)),
                ('age', models.CharField(max_length=30, null=True)),
                ('text', models.TextField(null=True)),
                ('when_created', models.DateTimeField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='HostData',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('bk_biz_id', models.CharField(max_length=30, null=True)),
                ('bk_set_id', models.CharField(max_length=30, null=True)),
                ('bk_host_innerip', models.CharField(max_length=50, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='HostInfo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('bk_host_innerip', models.CharField(max_length=50)),
                ('bk_biz_id', models.CharField(max_length=50, null=True)),
                ('bk_cloud_id', models.CharField(max_length=50, null=True)),
                ('bk_is_job', models.BooleanField(default=False)),
                ('bk_admin', models.CharField(max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='HostResource',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('bk_mem_rate', models.CharField(max_length=50, null=True)),
                ('bk_disk_rate', models.CharField(max_length=50, null=True)),
                ('bk_cpu_rate', models.CharField(max_length=50, null=True)),
                ('bk_date', models.CharField(max_length=50, null=True)),
                ('host_info', models.ForeignKey(to='home_application.HostInfo')),
            ],
        ),
        migrations.CreateModel(
            name='LogoImg',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('key', models.CharField(max_length=100)),
                ('value', models.BinaryField()),
            ],
        ),
        migrations.CreateModel(
            name='TaskModel',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=200, null=True)),
                ('business', models.CharField(max_length=200, null=True)),
                ('type', models.CharField(max_length=200, null=True)),
                ('creator', models.CharField(max_length=200, null=True)),
                ('when_created', models.CharField(max_length=100, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Template',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('num', models.IntegerField(null=True)),
                ('operation', models.CharField(max_length=300, null=True)),
                ('desc', models.CharField(max_length=500, null=True)),
                ('person', models.CharField(max_length=20, null=True)),
                ('when_created', models.DateTimeField(null=True)),
                ('task_model', models.ForeignKey(to='home_application.TaskModel')),
            ],
        ),
    ]
