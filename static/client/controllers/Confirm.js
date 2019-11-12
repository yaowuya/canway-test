controllers.controller('confirm', ["$scope", "$modalInstance", "options", function ($scope, $modalInstance, options) {
    $scope.typeList = {
        modify: "编辑",
        delete: "删除",
        sync: "同步",
        export: "导出",
        open: "开机",
        close: "关机",
        restart: "重启",
        reset: "重置",
        force: "硬关机",
        soldout: "下架",
        retry:"重试",
        download:"下载",
        search:"查询",
        add:"添加",
    };

    $scope.text = options.text;
    $scope.type = options.type;

    $scope.confirm = function () {
        $modalInstance.close();
    };
    $scope.cancel = function () {
        $modalInstance.dismiss('cancel');
    };
}]);