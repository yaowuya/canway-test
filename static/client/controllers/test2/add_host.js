controllers.controller('add_host', ["$scope", "$modalInstance", "msgModal", "loading", "errorModal", "objectItem", "sysService",
    function ($scope, $modalInstance, msgModal, loading, errorModal, objectItem, sysService) {
        $scope.title = "添加";
        $scope.args = {
            business: "",
            set: "",
            host: ""
        };

        // 单选
        $scope.business = {
            data: "business_list",
            multiple: false,
            modelData: "args.business"
        };
        $scope.business_list = []
        // 单选
        $scope.set = {
            data: "set_list",
            multiple: false,
            modelData: "args.set"
        };
        $scope.set_list = []
        // 单选
        $scope.host = {
            data: "host_list",
            multiple: false,
            modelData: "args.host"
        };
        $scope.host_list = []

        $scope.initBusiness = function () {
            sysService.tmp_get_biz({}, {}, function (res) {
                if (res.result) {
                    console.log("business:", res.data);
                    $scope.business_list = res.data;
                } else {
                    msgModal.open("error", res.message);
                }
            })
        }
        $scope.initBusiness();

        $scope.get_set = function () {
            $scope.get_set_list();
        }

        $scope.get_set_list = function () {
            sysService.tmp_get_set({}, {bk_biz_id: $scope.args.business}, function (res) {
                if (res.result) {
                    console.log("set:", res.data);
                    $scope.set_list = res.data;
                } else {
                    msgModal.open("error", res.message);
                }
            })
        }

        $scope.get_host = function () {
            $scope.get_host_list();
        }

        $scope.get_host_list = function () {
            sysService.tmp_get_host({}, $scope.args, function (res) {
                if (res.result) {
                    console.log("host:", res.data);
                    $scope.host_list = res.data;
                } else {
                    msgModal.open("error", res.message);
                }
            })
        }


        $scope.confirm = function () {
            $scope.clickop = true;
            loading.open();
            sysService.tmp_add_host({}, $scope.args, function (res) {
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