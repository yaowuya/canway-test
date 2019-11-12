### 培训
留时间部署

选择题一个小时，要20分钟做完，然后提前交，提交后不能修改。
选择题100分，90分过
机试题80分过

学一学怎么部署代码
部署代码后，生成一个token，要重新贴到代码中
部署到测试环境，数据库要创建两个cw-demo 和 cw-demo-test

home_application 下面建一个文件migrations

部署仓库地址http://192.168.165.95/ruifeng/cw-demo.git

常考 蓝鲸配置平台、作业平台和管控平台

返回结果用 jsonResponse

可以注释xss攻击中间件，调用get传时间时，可能会被转译。

尽量使用get_client_by_request

要提交migration里面的文件

考试本地开发时，要在host设置一个域名 127.0.0.1 test.cwbk.com(可以随意取值，但是不能和其他的名称相同)

1、安装项目依赖
pip2 install -r requirements.txt

2、新建数据库、迁移数据库
python2 manage.py makemigrations（生成migrations文件）
python2 manage.py migrate（在数据库创建表）


dev.cwbk.com:8000（dev.cwbk.com 已经在host进行了映射127.0.0.1）


启动celery
D:\1-code\cmp\home_application\celery_tasks.py
主要是同步账号

