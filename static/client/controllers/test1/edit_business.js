controllers.controller('edit_business', ["$scope", "$modalInstance", "msgModal", "loading", "errorModal", "objectItem", "sysService",
    function ($scope, $modalInstance, msgModal, loading, errorModal, objectItem, sysService) {
        $scope.title = "编辑";
        $scope.args = {
            id: "",
            business: "",
            type: "",
            name: ""
        };

        $scope.rowData = objectItem.row

        if ($scope.rowData != undefined) {
            $scope.title = "编辑";
            $scope.args.id = $scope.rowData.id;
            $scope.args.business = $scope.rowData.business;
            $scope.args.type = $scope.rowData.type;
            $scope.args.name = $scope.rowData.name;
        }

        $scope.type = [
            {name: "变更发布"},
            {name: "扩缩容"},
            {name: "上线类"},
            {name: "下架类"},
            {name: "例行维护"}
        ]

        $scope.business = [];

        $scope.initBusiness = function () {
            sysService.get_app_list({}, {}, function (res) {
                if (res.result) {
                    console.log("business:", res.data);
                    $scope.business = res.data;
                } else {
                    msgModal.open("error", res.message);
                }
            })
        }
        $scope.initBusiness();


        $scope.confirm = function () {
            $scope.clickop = true;
            loading.open();
            sysService.update_task_template({}, $scope.args, function (res) {
                loading.close();
                if (res.result) {
                    msgModal.open("success", "成功");
                    $modalInstance.close();
                } else {
                    msgModal.open("error", res.message);
                    $modalInstance.close();
                }
            })
        };

        $scope.cancel = function () {
            $modalInstance.dismiss("cancel");
        };

    }]);