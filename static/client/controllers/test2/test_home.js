controllers.controller("test_home", ["$scope", "$modal", "loading", "msgModalN", "msgModal", "errorModal", "confirmModal", "sysService", "$filter",
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

        $scope.get_host = function () {
            $scope.search();
        }

        $scope.rowSection = [];
        $scope.totalSerItems = 0;
        $scope.pagingOptions = {
            pageSizes: [5, 10, 15, 20],
            pageSize: "10",
            currentPage: 1
        };

        $scope.all_len;
        $scope.maxP;
        $scope.data = [];
        $scope.search = function (page_size, current_page) {
            loading.open();
            page_size = page_size || $scope.pagingOptions.pageSize;
            current_page = current_page || $scope.pagingOptions.currentPage;
            $scope.args.pageOption = {
                pageSize: page_size,
                pageNum: current_page
            };
            sysService.tmp_get_hostList({}, $scope.args, function (res) {
                loading.close();
                if (res.result) {
                    $scope.data = res.data;
                    $scope.maxP = res.pageNum;
                    $scope.all_len = res.allLen;
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
            enablePaging: true,
            pagingOptions: $scope.pagingOptions,
            totalServerItems: 'totalSerItems',
            selectWithCheckboxOnly: true,
            columnDefs: [
                {
                    field: 'bk_host_innerip', displayName: '内网IP', width: 120,
                },
                {
                    field: 'bk_os_name', displayName: '系统名'
                },
                {
                    field: 'bk_host_name', displayName: '主机名'
                },
                {
                    field: 'bk_cloud_id', displayName: '云区域id', visible: false
                },
                {
                    field: 'bk_inst_name', displayName: '云区域'
                },
                {
                    field: 'bk_mem_rate', displayName: 'Mem(%)'
                },
                {
                    field: 'bk_disk_rate', displayName: 'Disk(%)'
                },
                {
                    field: 'bk_cpu_rate', displayName: 'CPU(%)'
                },

                {
                    displayName: '操作', width: 200, cellClass: "text-center",
                    cellTemplate: '<div style="width:100%;text-align: center;padding-top: 5px;z-index: 1">' +
                        '<span  ng-click="query(row.entity)" ' +
                        'class="label label-primary label-outline table-span-label" >查询</span>' +
                        '<span ng-if="!row.entity.bk_is_job"  ng-click="add(row.entity)" ' +
                        'class="label label-primary label-outline table-span-label" >添加</span>' +
                        '<span ng-if="row.entity.bk_is_job"  ng-click="remove(row.entity)" ' +
                        'class="label label-info label-outline table-span-label" >移除</span>' +
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

        $scope.query = function (entity) {
            confirmModal.open({
                type: "search",
                text: "是否查询系统资源使用情况？",
                confirmClick: function () {
                    loading.open();
                    sysService.tmp_query_resource({}, {
                        bk_biz_id: $scope.args.business,
                        ip: entity.bk_host_innerip,
                        bk_cloud_id: entity.bk_cloud_id
                    }, function (res) {
                        loading.close();
                        if (res.result) {
                            msgModal.open("success", "查询成功");
                            var resource = res.data;
                            $scope.data = $scope.data.map(function (value) {
                                if (value.bk_host_innerip == resource.ip) {
                                    value.bk_mem_rate = resource.bk_mem_rate;
                                    value.bk_disk_rate = resource.bk_disk_rate;
                                    value.bk_cpu_rate = resource.bk_cpu_rate;
                                }
                                return value;
                            })
                        } else {
                            errorModal.open(res.message);
                        }
                    })
                }
            })
        }

        $scope.add=function (entity) {
            confirmModal.open({
                type: "add",
                text: "是否将主机加入周期性监控的队列？",
                confirmClick: function () {
                    loading.open();
                    sysService.tmp_add_queue({}, {
                        bk_biz_id: $scope.args.business,
                        bk_host_innerip: entity.bk_host_innerip,
                        bk_cloud_id: entity.bk_cloud_id
                    }, function (res) {
                        loading.close();
                        if (res.result) {
                            msgModal.open("success", "添加成功");
                            $scope.search();
                        } else {
                            errorModal.open(res.message);
                        }
                    })
                }
            })
        }
        $scope.remove=function (entity) {
            confirmModal.open({
                type: "delete",
                text: "是否将主机移除出周期性监控的队列？",
                confirmClick: function () {
                    loading.open();
                    sysService.tmp_remove_queue({}, {
                        bk_biz_id: $scope.args.business,
                        bk_host_innerip: entity.bk_host_innerip,
                        bk_cloud_id: entity.bk_cloud_id
                    }, function (res) {
                        loading.close();
                        if (res.result) {
                            msgModal.open("success", "移除成功");
                            $scope.search();
                        } else {
                            errorModal.open(res.message);
                        }
                    })
                }
            })
        }
    }]);
