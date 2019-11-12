controllers.controller("copy_record", ["$scope", "$modal", "msgModalN", "msgModal", "errorModal", "confirmModal", "sysService","loading",
    function ($scope, $modal, msgModalN, msgModal, errorModal, confirmModal, sysService, loading) {
        $scope.args={

        }

        $scope.rowSection = [];
        $scope.totalSerItems = 0;

        $scope.data = [];
        $scope.search = function () {
            loading.open();
            sysService.test3_get_joblist({}, $scope.args, function (res) {
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
        $scope.search();

        $scope.gridOption = {
            enableColumnResize: true,
            multiSelect: true,
            enableRowSelection: true,
            showSelectionCheckbox: true,
            data: 'data',
            selectedItems: $scope.rowSection,
            enablePaging: false,
            pagingOptions: $scope.pagingOptions,
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
                    field: 'file_size', displayName: '文件大小'
                },
                {
                    field: 'copy_time', displayName: '备份时间'
                },
                {
                    field: 'copy_person', displayName: '备份人'
                },

                {
                    displayName: 'JOB链接', width: 200, cellClass: "text-center",
                    cellTemplate: '<div style="width:100%;text-align: center;padding-top: 5px;z-index: 1">' +
                        '<span  ng-click="query(row.entity)" ' +
                        'class="label label-primary label-outline table-span-label" >查看详情</span>' +
                        '</div>'
                }
            ]
        };
    }]);
