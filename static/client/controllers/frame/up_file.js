controllers.controller('up_file', ["$scope", "$modalInstance", "loading", "errorModal", "msgModal",'objectItem', function ($scope, $modalInstance, loading, errorModal, msgModal,objectItem) {
    $scope.title = "导入excel";
    $scope.cancel = function () {
        $modalInstance.dismiss("cancel");
    };
    $scope.clickop = false;
    $scope.confirm = function () {
        if ($('.file_input').val() == '') {
            msgModal.open("error", "请选择文件！");
            return
        } else {
            $scope.clickop = true;
            loading.open();
            $('#upload_file_form').ajaxSubmit({
                url: 'up_excel/?obj_id='+objectItem.obj_id,
                type: 'post',
                dataType: 'json',
                success: function (data) {
                    loading.close();
                    if (data.result) {
                        msgModal.open("success", "导入成功");
                        $modalInstance.close();
                    } else {
                        msgModal.open("error", "导入失败");
                        $modalInstance.close();
                    }
                },
                error: function (data) {
                    loading.close();
                    alert('服务器异常')
                }
            });
        }
    }
}]);