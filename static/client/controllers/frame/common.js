controllers.controller("common", ["$scope", "$modal", "msgModalN", "msgModal", "errorModal", "confirmModal",
    function ($scope, $modal, msgModalN, msgModal, errorModal, confirmModal) {
    $scope.obj = {
        sex: "0"
    };

    $scope.modal_type = function(type){
        console.log(type)
        msgModal.open(type, "提示信息");
    }

    // 提示弹窗
    $scope.success_modal_n = function () {
        var message = "提示正文";
        msgModalN.open("success", message);
    };
    $scope.success_modal_n1 = function () {
        var message = "欢迎使用普通对话框";
        msgModalN.open("success1", message);
    };
    $scope.error_modal_n = function () {
        var message = "提示正文";
        msgModalN.open("error", message);
    };
    $scope.error_modal_n1 = function () {
        var message = "欢迎使用普通对话框";
        msgModalN.open("error1", message);
    };

    //错误提示框
    $scope.error_modal = function () {
        var error = ["错误1", "错误2", "错误3"];
        errorModal.open(error);
    };

    $scope.confirm_modal = function () {
        confirmModal.open({
            text: "是否确定编辑这些内容?",
            type: "modify",
            confirmClick: function () {
                alert("成功");
            }
        });
    };
    $scope.delete_modal = function () {
        confirmModal.open({
            text: "是否确定删除这些内容?",
            type: "delete",
            confirmClick: function () {
                msgModal.open("error", "修改成功");
            }
        });
    };

    // 多选
    $scope.appOption = {
        data: "app_list",
        multiple: true,
        modelData: "app_id"
    };
    // 单选
    $scope.appOption1 = {
        data: "app_list",
        multiple: false,
        modelData: "app_id1"
    };


    $scope.app_list = [
        {id: 1, text: '张三'},
        {id: 2, text: '李四'},
        {id: 3, text: '王五'},
    ]

    // 表格
    $scope.PagingData = [];
    $scope.totalSerItems = 0;
    $scope.pagingOptions = {
        pageSizes: [10, 50, 100],
        pageSize: "10",
        currentPage: 1
    };
    $scope.mail_list = [
        {name: "张三", age: 17, sex: "男"},
        {name: "张三", age: 17, sex: "男"},
        {name: "张三", age: 17, sex: "男"},
    ];

    $scope.setPagingData = function (data, pageSize, page) {
        $scope.PagingData = data.slice((page - 1) * pageSize, page * pageSize);
        $scope.totalSerItems = data.length;
        if (!$scope.$$phase) {
            $scope.$apply();
        }
    };
    $scope.getPagedDataAsync = function (pageSize, page) {
        $scope.setPagingData($scope.mail_list ? $scope.mail_list : [], pageSize, page);
    };

    $scope.pagingOptions.currentPage = 1;
    $scope.getPagedDataAsync($scope.pagingOptions.pageSize, $scope.pagingOptions.currentPage);


    $scope.$watch('pagingOptions', function (newVal, oldVal) {
        $scope.getPagedDataAsync($scope.pagingOptions.pageSize, $scope.pagingOptions.currentPage);
    }, true);

    $scope.gridOption = {
        data: 'PagingData',
        enablePaging: true,
        showFooter: true,
        pagingOptions: $scope.pagingOptions,
        totalServerItems: 'totalSerItems',
        columnDefs: [
            {field: 'name', displayName: '姓名', width: 150},
            {field: 'age', displayName: '年龄', width: 150},
            {field: 'sex', displayName: '性别', width: 150},
            {
                displayName: '操作',
                cellTemplate: '<div style="width:100%;text-align: center;padding-top: 5px;z-index: 1">' + '<span class="label label-info label-outline" style="min-width:50px;margin-left: 5px;">info</span>' +
                '<span class="label label-primary label-outline" style="min-width:50px;margin-left: 5px;">primary</span>' +
                '<span class="label label-success label-outline" style="min-width:50px;margin-left: 5px;">success</span>' +
                '<span class="label label-warning label-outline" style="min-width:50px;margin-left: 5px;">warning</span>' +
                '<span class="label label-danger label-outline" style="min-width:50px;margin-left: 5px;">danger</span>' +
                '<span class="label label-default label-outline" style="min-width:50px;margin-left: 5px;">disabled</span>' +
                '</div>'
            }

        ]
    };

    // 选项卡

    $scope.codeIndex = 0;
    $scope.codeTitle = [
        {'index': 0, 'title': '列1'},
        {'index': 1, 'title': '列2'},
        {'index': 2, 'title': '列3'},
    ];

    $scope.showCode = function (m) {
        $scope.codeIndex = m.index;
    };

    $scope.codeContent = ['内容1', '内容2', '内容3']


    // 弹框
    $scope.add = function () {
        var modalInstance = $modal.open({
            templateUrl: static_url + 'client/views/modal.html',
            windowClass: 'dialog_config',
            controller: 'modalCtrl',
            backdrop: 'static',
            resolve: {
                itemObj: function () {
                    return {};
                }
            }
        });
        modalInstance.result.then(function () {
            // $scope.search();

        })
    };

}]);
