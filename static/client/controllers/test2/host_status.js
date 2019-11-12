controllers.controller("host_status", ["$scope", "$modal", "loading", "msgModalN", "msgModal", "errorModal", "confirmModal", "sysService", "$filter",
    function ($scope, $modal, loading, msgModalN, msgModal, errorModal, confirmModal, sysService, $filter) {
        $scope.args = {
            business: "",
            host: "",
            set: ""
        };
        // 单选
        $scope.business = {
            data: "business_list",
            multiple: false,
            modelData: "args.business"
        };
        $scope.business_list = []
        // 单选
        $scope.host = {
            data: "host_list",
            multiple: false,
            modelData: "args.host"
        };
        $scope.host_list = [];

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
            sysService.tmp_get_host({}, $scope.args, function (res) {
                if (res.result) {
                    console.log("host:", res.data);
                    $scope.host_list = res.data;
                } else {
                    msgModal.open("error", res.message);
                }
            })
        }


        $scope.lineChart = {
            chart: {
                type: 'line',
            },
            yAxis: {
                lineWidth: 1,
                tickWidth: 1,
                labels: {
                    enabled: true
                },
                title: {
                    text: ''
                }
            },
            xAxis: {
                lineWidth: 1,
                tickWidth: 1,
                labels: {
                    enabled: true
                },
                categories: []
            },
            plotOptions: {
                series: {
                    lineWidth: 1,
                    marker: {
                        enabled: false
                    },
                    label: {
                        connectorAllowed: false
                    }
                }
            },
            //提示框位置和显示内容
            tooltip: {
                shared: true
            },
            legend: {
                enabled: true
            },
            series: [],
            watchData: "lineChartData"
        };
        $scope.get_line = function () {
            loading.open();
            sysService.tmp_query_host_resource({}, {bk_host_innerip: $scope.args.host}, function (res) {
                loading.close();
                if (res.result) {
                    msgModal.open("success", "查询成功");
                    var resData = res.data;
                    console.log(resData.mem);
                    $scope.lineChartData = {
                        categories: res.xAxis,
                        series: [{
                            "data": resData.mem,
                            "name": "Mem"
                        }, {
                            "data": resData.disk,
                            "name": "Disk"
                        }, {
                            "data": resData.cpu,
                            "name": "Cpu"
                        }]
                    };

                } else {
                    errorModal.open(res.message);
                }
            })
        }
    }]);
