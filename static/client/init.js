var app = angular.module("myApp", ['myController', 'utilServices', 'myDirective', 'ui.bootstrap', 'ui.router', 'webApiService','cwLeftMenu','ngGrid']);
var controllers = angular.module("myController", []);
var directives = angular.module("myDirective", []);


app.config(["$stateProvider", "$urlRouterProvider", "$httpProvider", function ($stateProvider, $urlRouterProvider, $httpProvider) {
    $httpProvider.defaults.headers.post['X-CSRFToken'] = $("#csrf").val();
    $urlRouterProvider.otherwise("/");//默认展示页面
    $stateProvider.state('home', {
        url: "/",
        controller: "home",
        templateUrl: static_url + "client/views/home.html"
    }).state('test', {
        url: "/test",
        controller: "test",
        templateUrl: static_url + "client/views/test.html"
    }).state('task_template', {
        url: "/task_template",
        controller: "task_template",
        templateUrl: static_url + "client/views/test1/task_template.html"
    }).state('host_detail', {
        url: "/host_detail?id",
        controller: "host_detail",
        templateUrl: static_url + "client/views/test1/host_detail.html"
    }).state('common', {
        url: "/common",
        controller: "common",
        templateUrl: static_url + "client/views/frame/common.html"
    }).state('chart', {
        url: "/chart",
        controller: "chart",
        templateUrl: static_url + "client/views/frame/chart.html"
    }).state('up_down', {
        url: "/up_down",
        controller: "up_down",
        templateUrl: static_url + "client/views/frame/up_down.html"
    }).state('api_test', {
        url: "/api_test",
        controller: "api_test",
        templateUrl: static_url + "client/views/frame/api_test.html"
    }).state('test_home', {
        url: "/test_home",
        controller: "test_home",
        templateUrl: static_url + "client/views/test2/test_home.html"
    }).state('host_status', {
        url: "/host_status",
        controller: "host_status",
        templateUrl: static_url + "client/views/test2/host_status.html"
    }).state('host_list', {
        url: "/host_list",
        controller: "host_list",
        templateUrl: static_url + "client/views/test2/host_list.html"
    }).state('copy_operate', {
        url: "/copy_operate",
        controller: "copy_operate",
        templateUrl: static_url + "client/views/test3/copy_operate.html"
    }).state('copy_record', {
        url: "/copy_record",
        controller: "copy_record",
        templateUrl: static_url + "client/views/test3/copy_record.html"
    })
}]);
