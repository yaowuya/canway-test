services = angular.module('webApiService', ['ngResource', 'utilServices']);

//生产代码
var POST = "POST";
var GET = "GET";

//测试代码
//var sourceRoute = "./Client/MockData";
//var fileType = ".html";
//var POST = "GET";
//var GET = "GET";
services.factory('sysService', ['$resource', function ($resource) {
    return $resource(site_url + ':actionName/', {},
        {
             get_app_list: {method: POST, params: {actionName: 'get_app_list'}, isArray: false},
             get_task_model: {method: POST, params: {actionName: 'get_task_model'}, isArray: false},
             delete_task_template: {method: POST, params: {actionName: 'delete_task_template'}, isArray: false},
             update_task_template: {method: POST, params: {actionName: 'update_task_template'}, isArray: false},

            //tmp测试用
            test_celery: {method: POST, params: {actionName: 'test_celery'}, isArray: false},
            tmp_get_biz: {method: POST, params: {actionName: 'tmp_get_biz'}, isArray: false},
            tmp_get_set: {method: POST, params: {actionName: 'tmp_get_set'}, isArray: false},
            tmp_get_host: {method: POST, params: {actionName: 'tmp_get_host'}, isArray: false},
            tmp_add_host: {method: POST, params: {actionName: 'tmp_add_host'}, isArray: false},
            tmp_get_hostList: {method: POST, params: {actionName: 'tmp_get_hostList'}, isArray: false},
            tmp_query_resource: {method: POST, params: {actionName: 'tmp_query_resource'}, isArray: false},
            tmp_add_queue: {method: POST, params: {actionName: 'tmp_add_queue'}, isArray: false},
            tmp_remove_queue: {method: POST, params: {actionName: 'tmp_remove_queue'}, isArray: false},
            tmp_query_host_resource: {method: POST, params: {actionName: 'tmp_query_host_resource'}, isArray: false},
            tmp_get_app_topo: {method: POST, params: {actionName: 'tmp_get_app_topo'}, isArray: false},

            //test3
            test3_get_biz: {method: POST, params: {actionName: 'test3_get_biz'}, isArray: false},
            test3_get_app_topo: {method: POST, params: {actionName: 'test3_get_app_topo'}, isArray: false},
            test3_get_host_ip: {method: POST, params: {actionName: 'test3_get_host_ip'}, isArray: false},
            test3_get_joblist: {method: POST, params: {actionName: 'test3_get_joblist'}, isArray: false},
            test3_get_fileinfo: {method: POST, params: {actionName: 'test3_get_fileinfo'}, isArray: false},
        });
}])


;//这是结束符，请勿删除