controllers.controller("copy_operate", ["$scope", "$modal", "loading", "msgModalN", "msgModal", "errorModal", "confirmModal", "sysService",
    function ($scope, $modal, loading, msgModalN, msgModal, errorModal, confirmModal, sysService) {
        $scope.args = {
            business: "",
            host: "",
            host_obj: [],
            folder: "",
            filename: "",
        };

        $scope.allServer = [];
        $scope.serverList = [];
        $scope.filterObj = {value: ''};
        $scope.attrList = [];
        $scope.select_attr = {value: ''};
        // 单选
        $scope.business = {
            data: "business_list",
            multiple: false,
            modelData: "args.business"
        };
        $scope.business_list = []

        $scope.initBusiness = function () {
            sysService.test3_get_biz({}, {}, function (res) {
                if (res.result) {
                    console.log("business:", res.data);
                    $scope.business_list = res.data;
                    $scope.args.business = res.data[0].id;
                    $scope.get_tree();
                } else {
                    msgModal.open("error", res.message);
                }
            })
        }
        $scope.initBusiness();

        $scope.businessTopo = [];

        $scope.get_tree = function () {
            sysService.test3_get_app_topo({}, {bk_biz_id: $scope.args.business}, function (res) {
                if (res.result) {
                    $scope.businessTopo = res.data;
                    msgModal.open("success", "查询拓扑树成功");
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
            onCheck: function (event, treeId, treeNode) {
                console.log("check", treeNode);
                $scope.searchHost(treeNode);
            }
        };

        $scope.searchHost = function (treeNode) {
            sysService.test3_get_host_ip({}, {
                bk_biz_id: $scope.args.business,
                bk_obj_id: treeNode.bk_obj_id,
                value: treeNode.bk_inst_id
            }, function (res) {
                if (res.result) {
                    var hostIp = "";
                    $scope.args.host_obj = []
                    res.data.forEach(function (value) {
                        hostIp += value.bk_host_innerip + "\n";
                        $scope.args.host_obj.push({
                            "ip": value.bk_host_innerip,
                            "bk_cloud_id": value.bk_cloud_id
                        })
                    })
                    if (hostIp.length > 0) {
                        hostIp = hostIp.substring(0, hostIp.length - 1);
                    }
                    $scope.args.host = hostIp;
                } else {
                    msgModal.open("error", res.message);
                }
            })
        }

        // 根据属性过滤主机，不重新查询接口 ，$filter
        $scope.filterServer = function () {
            if ($scope.select_attr.value === '') {
                $scope.serverList = angular.copy($scope.allServer)
            } else {
                // 循环主机列表，有该属性值的主机则返回
                $scope.serverList = $filter('filter')($scope.allServer, function (i) {
                    if (i[$scope.select_attr.value] == undefined || i[$scope.select_attr.value] == null)
                        return false;
                    return i[$scope.select_attr.value].indexOf($scope.filterObj.value) > -1
                })
            }
        };

        $scope.rowSection = [];
        $scope.totalSerItems = 0;
        $scope.data = [];
        $scope.search = function () {
            loading.open();
            sysService.test3_get_fileinfo({}, $scope.args, function (res) {
                loading.close();
                if (res.result) {
                    $scope.data = res.data;
                } else if (res.message == "403 Forbidden") {
                    window.location.href = site_url;
                } else {
                    msgModal.open("error", res.message);
                }
            })
        };

        $scope.gridOption = {
            enableColumnResize: true,
            multiSelect: true,
            enableRowSelection: true,
            showSelectionCheckbox: true,
            data: 'data',
            selectedItems: $scope.rowSection,
            enablePaging: false,
            totalServerItems: 'totalSerItems',
            selectWithCheckboxOnly: true,
            columnDefs: [
                {
                    field: 'num', displayName: '序号',
                },
                {
                    field: 'ip', displayName: 'IP'
                },
                {
                    field: 'file_list', displayName: '文件列表'
                },
                {
                    field: 'file_num', displayName: '文件数量'
                },
                {
                    field: 'file_size', displayName: '文件总大小'
                },
                {
                    displayName: '操作', width: 200, cellClass: "text-center",
                    cellTemplate: '<div style="width:100%;text-align: center;padding-top: 5px;z-index: 1">' +
                        '<span  ng-click="query(row.entity)" ' +
                        'class="label label-primary label-outline table-span-label" >备份</span>' +
                        '</div>'
                }
            ]
        };


        $scope.goToPage = function (page) {
            if (page == 0 && $scope.pagingOptions.currentPage != 1) {
                $scope.pagingOptions.currentPage = 1;
            } else if (page == -1 && $scope.pagingOptions.currentPage != 1) {
                $scope.pagingOptions.currentPage = $scope.pagingOptions.currentPage - 1;
            } else if (page == 1 && $scope.pagingOptions.currentPage != $scope.maxP) {
                $scope.pagingOptions.currentPage = $scope.pagingOptions.currentPage + 1;
            } else if (page == 9 && $scope.pagingOptions.currentPage != $scope.maxP) {
                $scope.pagingOptions.currentPage = $scope.maxP;
            } else if (page.num != undefined)
                $scope.pagingOptions.currentPage = page.num;
        };

        $scope.$watch("pagingOptions.currentPage", function (e) {
            if ($scope.maxP)
                $scope.search($scope.pagingOptions.pageSize, e);
        });
        $scope.$watch("pagingOptions.pageSize", function (e) {
            if ($scope.maxP)
                $scope.search(e, $scope.pagingOptions.currentPage);
        });
    }]);
