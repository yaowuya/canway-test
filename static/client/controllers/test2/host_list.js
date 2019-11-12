controllers.controller("host_list", ["$scope", "$modal", "loading", "msgModalN", "msgModal", "errorModal", "confirmModal", "sysService", "$filter",
    function ($scope, $modal, loading, msgModalN, msgModal, errorModal, confirmModal, sysService, $filter) {
        $scope.add = function () {
            var modalInstance = $modal.open({
                templateUrl: static_url + 'client/views/test2/add_host.html',
                windowClass: 'dialogForm',
                controller: 'add_host',
                backdrop: 'static',
                resolve: {
                    objectItem: function () {
                        return angular.copy({});
                    }
                }
            });
            modalInstance.result.then(function (res) {

            })
        };
    }]);
