controllers.controller("host_detail", ["$scope", "loading", "$modal", "confirmModal", "sysService", "errorModal", "msgModal", "$stateParams",
    function ($scope, loading, $modal, confirmModal, sysService, errorModal, msgModal, $stateParams) {
        $scope.id = $stateParams.id
        console.log($scope.id);
    }]);


