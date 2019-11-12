controllers.controller("up_down", ["$scope", "$modal", "loading", "msgModalN", "msgModal", "errorModal", "confirmModal", "sysService", "$filter",
    function ($scope, $modal, loading, msgModalN, msgModal, errorModal, confirmModal, sysService, $filter) {
        $scope.select_pic = function () {
            console.log("select_pic");
            document.getElementById('uploadFile').value = '';
            document.getElementById('uploadFile').click();
        }

        $scope.upload_img = function () {
            var fd = new FormData();
            var files = $("#uploadFile").get(0).files;
            var error_list = test_error(files);
            if (error_list.length > 0) {
                errorModal.open(error_list);
                return
            }
            fd.append("upfile", $("#uploadFile").get(0).files[0]);
            fd.append("param", "1");
            loading.open();
            $.ajax({
                url: site_url + "upload_img/",
                type: "POST",
                processData: false,
                contentType: false,
                data: fd,
                success: function (res) {
                    loading.close();
                    if (res.result) {
                        msgModal.open("success", "上传成功");
                        window.location.reload();
                    } else {
                        errorModal.open(res.data);

                    }
                }
            });
        };
        var test_error = function (files) {
            var file_type = files[0].type;
            var file_size = files[0].size / 1024;
            var error_list = [];
            if (file_type !== "image/png" && file_type !== 'image/jpeg') {
                error_list.push("只允许png,jpg,jpeg格式的图片!");
            }
            if (file_size > 500) {
                error_list.push("请保证文件小于500K!");
            }
            return error_list;
        };

        $scope.show_pic = function () {
            $scope.logo_img = site_url + "show_img/?param=logo"
        }

        $scope.show_pic();

        $scope.down_img = function () {
            window.open(site_url + "down_img/?param=logo")
        }

        $scope.upload_field = function () {
            $('#uploadInfo').click();
        }
        $scope.down_load_field = function () {
            window.open("down_load_field/?obj_id=1")
        }

        $scope.uploadItem = function () {
            var fd = new FormData();
            var files = $("#uploadInfo").get(0).files;
            var error_list = file_error(files);
            if (error_list.length > 0) {
                errorModal.open(error_list);
                return
            }
            var name_path = "test_";
            fd.append("upfile", files[0]);
            fd.append("file_path", name_path);
            loading.open();
            $.ajax({
                url: site_url + "upload_info/?obj_id=1",
                type: "POST",
                processData: false,
                contentType: false,
                data: fd,
                success: function (res) {
                    loading.close();
                    if (res.result) {
                        msgModal.open("success", "上传成功");
                        window.location.reload();
                    } else {
                        errorModal.open(res.data);

                    }
                }
            });
        }

        var file_error = function (files) {
            var file_name = files[0].name.toLowerCase();
            var file_type = file_name.split(".")[1];
            console.log(file_name, file_type);
            var file_size = files[0].size / 1024;
            var error_list = [];
            var typeArray = ["txt", "xls", "docx"];
            var flag = false;
            typeArray.forEach(function (value) {
                if (value == file_type) {
                    flag = true;
                }
            })
            if (!flag) {
                error_list.push("只允许txt,xls,docx格式的文件!");
            }
            if (file_size > 10240) {
                error_list.push("文件大小不能超过10M！");
            }
            return error_list;
        };

        // 导入excel文件
        $scope.upload = function () {
            var modalInstance = $modal.open({
                templateUrl: static_url + 'client/views/frame/up_file.html',
                windowClass: 'dialog_custom',
                controller: 'up_file',
                backdrop: 'static',
                resolve: {
                    objectItem: function () {
                        return {obj_id: '1'}
                    }
                }
            });
            modalInstance.result.then(function (res) {
                //导入成功后的动作，比如刷新页面等
            })
        };
        //导出excel文件
        $scope.down_excel = function () {
            window.open("down_excel/?obj_id=1")
        };

        // 导入csv文件
        $scope.up_csv=function(){
            document.getElementById('uploadCsvFile').value = '';
            document.getElementById('uploadCsvFile').click();
        }
        $scope.uploadCsv = function () {
            CWApp.uploadCsv("uploadCsvFile", callBack);
        };
        var callBack = function () {
            var content = fr.result;
            content = content.replace(new RegExp("\"", "gm"), "");
            var temp_list = [];
            var content_list = content.substring(0, content.lastIndexOf("\n")).split("\n");
            var column_len = content_list[0].split(",").length;
            var up_cvs = function (data) {
                loading.open();
                // 导入的后台方法
                sysService.up_csv({}, data, function (res) {
                    loading.close();
                    if (res.result) {
                        alert("上传成功")
                    } else {
                        alert('上传失败')
                    }
                })
            }
            for (var i = 1; i < content_list.length; i++) {
                var device_obj = {};
                var columns = content_list[i].replace("\r", "").split(",");
                var a = columns.slice(0, 8);
                var b = columns.slice(8);
                var device_obj = {
                    name: a[0],
                    age: a[1],
                    text: a[2]
                };
                temp_list.push(device_obj)
            }
            $scope.csvList = temp_list;
            // 开始请求后台方法
            up_cvs($scope.csvList)
        };


        //导出csv文件
        $scope.down_csv = function () {
            window.open("down_csv/?obj_id=1")
        };
    }])