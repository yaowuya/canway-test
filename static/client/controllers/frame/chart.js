controllers.controller("chart", ["$scope", "$modal", "loading", "msgModalN", "msgModal", "errorModal", "confirmModal", "sysService", "$filter",
    function ($scope, $modal, loading, msgModalN, msgModal, errorModal, confirmModal, sysService, $filter) {

        // 时间折线图
        function initTimes() {
            var date = new Date();
            var result = [];
            for (var i = 0; i < 200; i++) {
                var datetime = new Date(date.getTime() - i * 3600 * 1000).getTime();
                var rate = Math.random();
                result.push([datetime, rate]);
            }
            return result;
        }

        $scope.lineSeries = []
        var theme = ["cpu", "disk", "memory"]

        theme.forEach(function (value) {
            $scope.lineSeries.push({name: value, data: initTimes()})
        })


        $scope.lineData = {
            tickInterval: 24 * 3600 * 1000,
            series: $scope.lineSeries
        };


        $scope.lineChart = {
            chart: {type: 'line'},
            yAxis: {
                labels: {
                    format: '{value}%'
                }
            },
            xAxis: {
                type: 'datetime',
                dateTimeLabelFormats: {
                    second: '%M:%S',
                    minute: '%M:%S',
                    hour: '%H:%M:%S',
                    day: '%Y-%m-%d'
                },
                tickInterval: 1 * 3600 * 1000
            },
            //提示框位置和显示内容
            tooltip: {
                crosshairs: [{
                    width: 1,
                    color: 'red'
                }],
                xDateFormat: '%m-%d %H:%M:%S',
                shared: true,
            },
            legend: {
                layout: 'horizontal',
                align: 'center',
                verticalAlign: 'bottom',
                borderWidth: 0
            },
            series: [],
            watchData: "lineData"
        };

        // 普通折线图

        $scope.commonLineChart = {
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
        $scope.lineChartData = {
            categories:["2019-05", "2019-06", "2019-07", "2019-08", "2019-09", "2019-10"],
            series: [{
                "data": [0, 24830.0, 35990.0, 36620.0, 90.0, 90.0],
                "name": "spec_cost"
            }, {
                "data": [0, 4371.5, 8341.199999999999, 8209.600000000002, 35.0, 35.0],
                "name": "disk_cost"
            }, {
                "data": [0, 0, 0, 0, 0, 0],
                "name": "net_cost"
            }, {
                "data": [0, 29201.5, 44331.2, 44829.59999999999, 125.0, 125.0],
                "name": "cost"
            }]
        };


        //柱状图
        $scope.chartColumn = {
            chart: {
                type: 'column',
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
            watchData: "columnData"
        };
        $scope.columnData = {
            categories:["launch-advisor-20190506", "Thomas-Test02"],
            series: [
                {name: "当月成本1", data: [66.0, 59.0]},
                {name: "当月成本2", data: [44.0, 70.0]},
                {name: "当月成本3", data: [60.0, 40.0]},
            ]
        };

        //饼图
        $scope.chartPie = {
            chart: {
                plotBackgroundColor: null,
                plotBorderWidth: null,
                plotShadow: false,
                type: 'pie',
            },
            title: {
                text: '标题'
            },
            tooltip: {
                pointFormat: '{series.name}: <b>{point.percentage:.1f}%</b>'
            },
            plotOptions: {
                pie: {
                    allowPointSelect: true,
                    cursor: 'pointer',
                    dataLabels: {
                        enabled: false
                    },
                    showInLegend: true
                }
            },
            series: [],
            watchData: "pieData"
        };
        $scope.pieData = {
            series: [{
                name: '占本月总成本',
                colorByPoint: true,
                data: [
                    {name: '计算资源消费', y: 65, sliced: true, selected: true},
                    {name: '磁盘消费', y: 20},
                    {name: '网络消费', y: 15}
                ]
            }]
        };


    }])