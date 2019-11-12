//js通用服务

//随机数
var randomIndex = Math.random();
var loadingStack = [];
angular.module('utilServices', []).factory('guid', function () {
    return {
        newGuid: function () {
            var guid = "";
            for (var i = 1; i <= 32; i++) {
                var n = Math.floor(Math.random() * 16.0).toString(16);
                guid += n;
                if ((i == 8) || (i == 12) || (i == 16) || (i == 20))
                    guid += "-";
            }
            return guid;
        },
        empty: function () {
            return "00000000-0000-0000-0000-000000000000";
        }
    };
})

.factory('confirmModal', ["$modal", function ($modal) {
    return {
        open: function (options) {
            var defaultOptions = {
               // confirmClick: function () { },
                text: '确认要执行此操作吗？',
                type: 'modify'
            };
            extendOptions = angular.extend({}, defaultOptions, options);
            var modalInstance = $modal.open({
                templateUrl: static_url+'client/views/ConfirmModal.html?index=' + randomIndex,
                windowClass: 'dialogConfirm',
                controller: 'confirm',
                backdrop: 'static',
                resolve: {
                    options: function () {
                        return extendOptions;
                    }
                }
            });
            modalInstance.result.then(
               function () {
                   extendOptions.confirmClick();
               });
        }
    };
}])

.factory('errorModal', ["$modal", function ($modal) {
    return {
        open: function (errorList) {
            var modalInstance = $modal.open({
                templateUrl: static_url+'client/views/ErrorModal.html' ,
                windowClass: 'dialogError',
                controller: 'error',
                backdrop: 'static',
                resolve: {
                    errorList: function () {
                        return errorList;
                    }
                }
            });
        }
    };
}])


.factory('loading', ["$rootScope", function ($rootScope) {
    return {
        open: function (text, scope, fontSize, color) {
            var loadingText = "请稍候";
            var loadingScope = "#main-content";
            var width = "";
            var height = "";
            var fontsize = "22";
            var fontcolor = "#333";
            if (arguments.length > 0 && text != null && text != '' && text != undefined) {
                loadingText = text;
            }
            if(fontSize){
                fontsize = fontSize;
            }
            if(color)
                fontcolor = color;
            if (arguments.length > 1) {
                loadingScope = scope;
            }
            if ($(loadingScope).children(".showFullLoading").length == 0) {
                width = $(loadingScope).width();
                height = $(loadingScope).height();

                $(loadingScope).append('<div class="showFullLoading" style="font-size:'+fontsize+'px;color:'+fontcolor+';height: ' + height + 'px; width: ' + width + 'px;padding-top:20%;text-align: center "> \
                <i class="fa fa-spinner fa-pulse" style="margin-right: 5px;"></i>' + loadingText + '...\
               </div>');
            }
        },
        close: function (scope) {
            var loadingScope = "#main-content";
            if (arguments.length > 0) {
                loadingScope = scope;
            }
            if ($(loadingScope).children(".showFullLoading").length > 0) {
                $(loadingScope).children(".showFullLoading").remove();
            }
        }
    };
}])

.factory('msgModalN', ["$modal", function ($modal) {
    return {
        open: function (type, msg, callBack) {
            var modalInstance = $modal.open({
                templateUrl: static_url+'client/views/Message.html' ,
                windowClass: 'dialogConfirm',
                controller: 'Message',
                backdrop: 'static',
                resolve: {
                    info: function () {
                        return {
                            msg: msg,
                            type: type
                        };
                    }
                }
            });
            modalInstance.result.then(function () {
                 if(callBack)
                     callBack();
            });
        }
    };
}])

.factory('msgModal', ["$modal", function ($modal) {
    return {
        open: function (level, msg, position) {
            if (!position) {
                position = "middle-content"
            }
            toastr.remove();
            if (!level){
                level = "info";
            }
            var title = "";
            if (level == "info") {
                title = "提示";
            }
            else if (level == "warning") {
                title = "警告";
            }
            else if (level == "success") {
                title = "成功";
            }
            else {
                title = "错误";
                level = "error";
            }
            toastr[level](msg, title, {
                positionClass: position,timeOut:500
            });
        }
    };
}])
;//这是结束符，请勿删除。

