controllers.controller("site", ["$scope",
    function ($scope) {
        $scope.menuList = [
            {
                displayName: "首页", iconClass: "fa fa-tachometer fa-lg", url: "#/"
            },
            {
                displayName: "test", url: "#/test"
            },
            {
                displayName: "模拟1", children: [
                    {displayName: "任务模板", url: "#/task_template"},
                    {displayName: "任务中心", url: "#/p2-2"}
                ]
            },
            {
                displayName: "模拟2", children: [
                    {displayName: "首页", url: "#/test_home"},
                    {displayName: "主机状态", url: "#/host_status"},
                    {displayName: "主机列表", url: "#/host_list"}
                ]
            },
            {
                displayName: "模拟3", children: [
                    {displayName: "备份操作", url: "#/copy_operate"},
                    {displayName: "备份记录", url: "#/copy_record"},
                ]
            },
            {
                displayName: "框架", children: [
                    {displayName: "常用组件", url: "#/common"},
                    {displayName: "chart", url: "#/chart"},
                    {displayName: "上传下载", url: "#/up_down"},
                    {displayName: "接口练习", url: "#/api_test"}
                ]
            },
        ];
        $scope.menuOption = {
            data: $scope.menuList
        };
    }]);

