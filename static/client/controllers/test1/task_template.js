controllers.controller("task_template", ["$scope", "$modal", "loading", "msgModalN", "msgModal", "errorModal", "confirmModal", "sysService", "$filter",
    function ($scope, $modal, loading, msgModalN, msgModal, errorModal, confirmModal, sysService, $filter) {
        var startTime = new Date()
        $scope.start = startTime.setDate(startTime.getDate() - 30)
        $scope.end = new Date()

        $scope.args = {
            business: "",
            type: "",
            name: "",
            whenStart: $filter('date')($scope.start, 'yyyy-MM-dd'),
            whenEnd: $filter('date')($scope.end, 'yyyy-MM-dd')
        };

        $scope.type = [
            {name: "变更发布"},
            {name: "扩缩容"},
            {name: "上线类"},
            {name: "下架类"},
            {name: "例行维护"}
        ]

        // 单选
        $scope.business = {
            data: "business_list",
            multiple: false,
            modelData: "args.business"
        };
        $scope.business_list = []

        $scope.initBusiness = function () {
            sysService.get_app_list({}, {}, function (res) {
                if (res.result) {
                    console.log("business:", res.data);
                    // $scope.business = res.data;
                    res.data.forEach(function (value) {
                        $scope.business_list.push({id: value.bk_biz_name, text: value.bk_biz_name})
                    })
                } else {
                    msgModal.open("error", res.message);
                }
            })
        }
        $scope.initBusiness();


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
            sysService.get_task_model({}, $scope.args, function (res) {
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
        $scope.search();

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
                    field: 'id', displayName: 'ID'
                },
                {
                    field: 'name', displayName: '模板名称'
                },
                {
                    field: 'business', displayName: '业务名称'
                },
                {
                    field: 'type', displayName: '模型类型'
                },
                {
                    field: 'creator', displayName: '创建者'
                },
                {
                    field: 'when_created',
                    displayName: '创建时间',
                    cellTemplate: '<span class="table-tip" title="{{row.entity.when_created}}">' +
                        '{{row.entity.when_created}}</span>'
                },
                {
                    field: 'creator', displayName: '更新者'
                },
                {
                    field: 'when_created',
                    displayName: '更新时间',
                    cellTemplate: '<span class="table-tip" title="{{row.entity.when_created}}">' +
                        '{{row.entity.when_created}}</span>'
                },
                {
                    displayName: '操作', width: 300, cellClass: "text-center",
                    cellTemplate: '<div style="width:100%;text-align: center;padding-top: 5px;z-index: 1">' +
                        '<span  ng-click="add(row.entity)" ' +
                        'class="label label-primary label-outline table-span-label" >添加</span>' +
                        '<span  ng-click="edit(row.entity)" ' +
                        'class="label label-success label-outline table-span-label" >编辑</span>' +
                        '<span  ng-click="download(row.entity)" ' +
                        'class="label label-info label-outline table-span-label" >下载</span>' +
                        '<span ng-click="delete(row.entity)" ' +
                        'class="label label-danger label-outline table-span-label" >删除</span>' +
                        '<span ui-sref="host_detail({id:row.entity.id})" ' +
                        ' class="label label-danger label-outline table-span-label">详情跳转</span>' +
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

        $scope.add = function (row) {
            var modalInstance = $modal.open({
                templateUrl: static_url + 'client/views/test1/add_business.html',
                windowClass: 'dialogForm',
                controller: 'add_business',
                backdrop: 'static',
                resolve: {
                    objectItem: function () {
                        return angular.copy({});
                    }
                }
            });
            modalInstance.result.then(function (res) {
                $scope.search();
            })
        };

        $scope.edit = function (row) {
            var modalInstance = $modal.open({
                templateUrl: static_url + 'client/views/test1/edit_business.html',
                windowClass: 'dialogForm',
                controller: 'edit_business',
                backdrop: 'static',
                resolve: {
                    objectItem: function () {
                        return angular.copy({row: row});
                    }
                }
            });
            modalInstance.result.then(function (res) {
                $scope.search();
            })
        };

        $scope.delete = function (row) {
            confirmModal.open({
                type: "delete",
                text: "确认是否要删除该记录？",
                confirmClick: function () {
                    loading.open();
                    sysService.delete_task_template({}, {id: row.id}, function (res) {
                        if (res.result) {
                            msgModal.open("success", "删除成功!");
                            $scope.search($scope.pagingOptions.pageSize, $scope.pagingOptions.currentPage);
                        } else {
                            errorModal.open(res.data);
                        }
                    })
                }
            })
        };

        $scope.download = function (row) {
            confirmModal.open({
                type: "download",
                text: "确认下载模板吗?",
                confirmClick: function () {
                    window.open("down_excel/?id=" + row.id)
                }
            })
        };
    }]);
