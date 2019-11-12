controllers.controller("api_test", ["$scope", "$modal", "loading", "msgModalN", "msgModal", "errorModal", "confirmModal", "sysService", "$filter",
    function ($scope, $modal, loading, msgModalN, msgModal, errorModal, confirmModal, sysService, $filter) {

        $scope.args = {
            business: "",
            host: "",
        };

        // 单选
        $scope.business = {
            data: "business_list",
            multiple: false,
            modelData: "args.business"
        };
        $scope.business_list = []

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


        $scope.fastRunScript = function () {
            sysService.test_celery({}, {}, function (res) {
                if (res.result) {
                    console.log("test_celery:", res.data);
                } else {
                    msgModal.open("error", res.message);
                }
            })
        }

        $scope.businessTopo = [];

        $scope.get_tree = function () {
            sysService.tmp_get_app_topo({}, {bk_biz_id: $scope.args.business}, function (res) {
                if (res.result) {
                    $scope.businessTopo = res.data;
                    msgModal.open("success", "成功");
                } else {
                    msgModal.open("error", res.message);
                }
            })
        }

        // 树形topo组件
        $scope.zTreeOptions = {
            check: {
                enable: true,
                chkStyle: "checkbox",
                chkboxType: {"Y": "ps", "N": "ps"}
            },
            data: {
                key: {
                    // 显示的字段
                    name: "bk_inst_name",
                    children: "child",
                    isParent: "isParent"
                }
            },
            onClick: function (event, treeId, treeNode) {
                console.log(treeNode);
            },
            onCheck: function (event, treeId, treeNode) {
                console.log("check", treeNode);
            }
        };


    }])