controllers.controller('add_business', ["$scope", "$modalInstance", "msgModal", "loading", "errorModal", "objectItem", "sysService",
    function ($scope, $modalInstance, msgModal, loading, errorModal, objectItem, sysService) {
        $scope.title = "添加";
        $scope.args = {
            business: "",
            type: "",
            name: ""
        };

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
            $('#upload_file_form').ajaxSubmit({
                url: "upload_file_form/?params=" + JSON.stringify($scope.args),
                type: 'post',
                dataType: 'json',
                data: {},
                success: function (data) {
                    loading.close();
                    if (data.result) {
                        msgModal.open("success", "导入成功");
                        $modalInstance.close();
                    } else {
                        msgModal.open("error", "数据异常，未导入");
                        $modalInstance.close();
                    }
                },
                error: function (data) {
                    loading.close();
                    msgModal.open("error", "服务器异常");
                }
            });
        };

        $scope.cancel = function () {
            $modalInstance.dismiss("cancel");
        };

    }]);