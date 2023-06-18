const h1 = document.querySelector('h1')
h1.innerHTML = h1.textContent.replace(/\S/g, "<span>$&</span>")


document.querySelectorAll('span').forEach((span, index) => {
    span.style.setProperty('--delay', `${index * 0.1}s`)
})


document.querySelectorAll('li').forEach(button => {
    button.addEventListener('click', e => {
        h1.style.setProperty('--animation', e.target.getAttribute('data-animation'))


        h1.classList.remove('animate')
        void h1.offsetWidth
        h1.classList.add('animate')
    })
})


var data_map;
var data_bar;
var data_pie;
var max_value;

<!--  网页数据初始化函数  -->
function init_data(){
    $.ajax({
      url: '/map_1999',
      type: "GET",
      success: function (response) {
        max_value = 50000;
        data_map = response;
        chart();
      }
    });
    $.ajax({
      url: 'region_Asia',
      type: "GET",
      success: function (response) {
            data_bar = response;
            chart_bar();
      }
    });

    chart_pie();

<!--        $.ajax({-->
<!--          url: 'pie_1999',-->
<!--          type: "GET",-->
<!--          success: function (response) {-->
<!--                data_pie = response;-->
<!--                chart_pie();-->
<!--          }-->
<!--        });-->
}

window.onload = init_data;

<!-- 世界地图数据请求 -->
$(document).ready(function () {
  $(".map").click(function () {
    var param = $(this).data("param");
    var urlStr = "/map_"+param;
    $.ajax({
      url: urlStr,
      type: "GET",
      success: function (response) {
      max_value = 50000;
        data_map = response;
<!--            console.log(data_map);-->
        chart();
      }
    });
  });
});

<!--  3D柱状图数据请求  -->
$(document).ready(function () {
  $(".bar").click(function () {
    var param = $(this).data("param");
    var urlStr = "/region_"+param;
    $.ajax({
      url: urlStr,
      type: "GET",
      success: function (response) {
            data_bar = response;
            chart_bar();
      }
    });
  });
});

<!-- 饼图数据请求 -->
<!--    $(document).ready(function () {-->
<!--      $(".pie").click(function () {-->
<!--        var param = $(this).data("param");-->
<!--        var urlStr = "/pie_"+param;-->
<!--        $.ajax({-->
<!--          url: urlStr,-->
<!--          type: "GET",-->
<!--          success: function (response) {-->
<!--                data_pie = response;-->
<!--                chart_pie();-->
<!--          }-->
<!--        });-->
<!--      });-->
<!--    });-->

<!-- 吸烟率数据请求 -->
$(document).ready(function () {
  $(".pct").click(function () {
    $.ajax({
      url: '/pct',
      type: "GET",
      success: function (response) {
            max_value = 50;
            data_map = response;
            console.log(data_map)
            chart();
      }
    });
  });
});

<!--  页面刷新函数  -->
$(document).ready(function () {
      $("#refresh").click(function () {
            location.reload();
      });
});

<!-- 绘制世界地图函数 -->
 function chart(){
    var myChart = echarts.init(document.getElementById('world'));
    let nameMap = '世界地图.txt'
    option = {
        tooltip: {
            trigger: 'item',
            formatter: function (params) {
                console.log(params)
                if (params.name) {
                    return params.name + ' : ' + (isNaN(params.value) ? 0 : parseInt(params.value));
                }
            }
        },
        layoutCenter: ['40%', '50%'],//位置
        layoutSize: '200%',//大小
        aspectScale: 0.8, //宽高比
        // 视觉映射组件
        grid: {
            left: '40%',
            right: '40%',
            bottom: '3%',
            containLabel: true
        },
        visualMap: {
            type: 'continuous', // continuous 类型为连续型  piecewise 类型为分段型
            show: true, // 显示 visualMap-continuous 组件 如果设置为 false，不会显示，但是数据映射的功能还存在
            // 指定 visualMapContinuous 组件的允许的最小/大值。'min'/'max' 必须用户指定。
            // [visualMap.min, visualMax.max] 形成了视觉映射的『定义域』
            // 文本样式
            min: 0,
            max: max_value,
            textStyle: {
                fontSize: 15,
                color: '#fff'
            },
            realtime: false, // 拖拽时，是否实时更新
            calculable: true, // 是否显示拖拽用的手柄
            // 定义 在选中范围中 的视觉元素
            inRange: {
                color: ['rgb(243, 228, 71)', 'rgb(233, 178, 59)', 'rgb(232, 163, 14)', 'rgb(232, 116, 14)', 'rgb(232, 94, 14)', 'rgb(234, 112, 5)'] // 图元的颜色
            }
        },
        series: [
            {
                name: 'World Population (2010)',
                type: 'map',
                mapType: 'world',
                roam: true,
                itemStyle: {
                    areaColor: 'orange', // 地图区域的颜色 如果设置了visualMap，areaColor属性将不起作用
                    borderWidth: 0.5, // 描边线宽 为 0 时无描边
                    borderColor: '#000', // 图形的描边颜色 支持的颜色格式同 color，不支持回调函数
                    borderType: 'solid', // 描边类型，默认为实线，支持 'solid', 'dashed', 'dotted'
                    emphasis: { label: { show: true } }
                },
                label: {
                    show: false // 是否显示对应地名
                },
                data: data_map,
                nameMap: nameMap
            }
        ]
    };
    myChart.setOption(option);
}

<!-- 绘制饼图函数 -->
function chart_pie(){
    var chartDom = document.getElementById('shanxingtu');
    var myChart1 = echarts.init(chartDom);
    var option;

    option = {
        title: {
            text: '吸烟对男女寿命减少的期望值',
            left: 'center',
            top: 2,
            textStyle: {
                color: 'black'
            }
        },
        tooltip: {
            trigger: 'item'
        },
        visualMap: {
            show: false,
            min: 0,
            max: 5,
            inRange: {
                colorLightness: [0, 1]
            }
        },
        series: [
            {
                name: '吸烟人数',
                type: 'pie',
                radius: '80%',
                center: ['50%', '60%'],
<!--                    data: data_pie,-->
                data: [{'name': 'Male', 'value': 2.93}, {'name': 'Female', 'value': 0.88}],
                roseType: 'radius',
                label: {
                },
                labelLine: {
                    lineStyle: {
                    },
                    smooth: 0.2,
                    length: 1,
                    length2: 2
                },
                itemStyle: {
<!--                        color:-->
                    shadowBlur: 200,
                    shadowColor: '#DCDCDC'
                },
                animationType: 'scale',
                animationEasing: 'elasticOut',
                animationDelay: function (idx) {
                    return Math.random() * 200;
                }
            }
        ]
    };
    option && myChart1.setOption(option);
}

<!--  绘制3D柱状图函数, 有官方bug?  -->
function chart_bar(){
    var chartDom1 = document.getElementById('zhuzhuangtu');
    var myChart2 = echarts.init(chartDom1);
    var option2 = {
        grid3D: {
            viewControl: {
                projection: 'perspective',
                distance: 180
            },
            left: '10%',
            top: '-5%',
            containLabel: true
        },
        xAxis3D: {
            axisLabel: {
                textStyle: {
                    fontSize: '7',
                },
            },
            type: 'category'
        },
        yAxis3D: {
            axisLabel: {
                textStyle: {
                    fontSize: '7',
                },
            },
            type: 'category'
        },
        zAxis3D: {
            axisLabel: {
                textStyle: {
                    fontFamily: '微软雅黑',
                    fontSize: '7',
                },
            }
        },

        visualMap: {
            calculable: false,
            max: 400000,
            inRange: {
                color: ['#313695', '#4575b4', '#74add1', '#abd9e9', '#e0f3f8', '#ffffbf', '#fee090', '#fdae61', '#f46d43', '#d73027', 'black']
            }
        },
        dataset: {
            source: data_bar
        },
        series: [
            {
                type: 'bar3D',
                symbolSize: 5,
                encode: {
                    x: 'name',
                    y: 'year',
                    z: 'value',
                    tooltip: [0, 1, 2]
                }
            }
        ]
    };
    myChart2.setOption(option2, true);
 }



var chart_plot = document.getElementById('zhexiantu');
var myChartPlot = echarts.init(chart_plot);
var option_plot;

<!--  折线图  -->
var app = {};

var chartDom = document.getElementById('zhexiantu');
var myChart = echarts.init(chartDom);
var option;

const posList = [
    'left',
    'right',
    'top',
    'bottom',
    'inside',
    'insideTop',
    'insideLeft',
    'insideRight',
    'insideBottom',
    'insideTopLeft',
    'insideTopRight',
    'insideBottomLeft',
    'insideBottomRight'
];
app.configParameters = {
    rotate: {
        min: -90,
        max: 90
    },
    align: {
        options: {
            left: 'left',
            center: 'center',
            right: 'right'
        }
    },
    verticalAlign: {
        options: {
            top: 'top',
            middle: 'middle',
            bottom: 'bottom'
        }
    },
    position: {
        options: posList.reduce(function (map, pos) {
            map[pos] = pos;
            return map;
        }, {})
    },
    distance: {
        min: 0,
        max: 100
    }
};
app.config = {
    rotate: 0,
    align: 'center',
    verticalAlign: 'bottom',
    position: 'inside',
    distance: 0,
    onChange: function () {
        const labelOption = {
            rotate: app.config.rotate,
            align: app.config.align,
            verticalAlign: app.config.verticalAlign,
            position: app.config.position,
            distance: app.config.distance
        };
        myChart.setOption({
            series: [
                {
                    label: labelOption
                },
                {
                    label: labelOption
                },
                {
                    label: labelOption
                },
                {
                    label: labelOption
                }
            ]
        });
    }
};
const labelOption = {
    show: true,
    position: app.config.position,
    distance: app.config.distance,
    align: app.config.align,
    verticalAlign: app.config.verticalAlign,
    rotate: app.config.rotate,
<!--        formatter: '{c}  {name|{a}}',-->
    formatter: '{c}',
    fontSize: 10,
    rich: {
        name: {}
    }
};
option = {
    tooltip: {
        trigger: 'axis',
        axisPointer: {
            type: 'shadow'
        }
    },
    legend: {
        data: ['男性人口', '男性吸烟人数', '女性人口', '女性吸烟人数']
    },
    toolbox: {
        show: true,
        orient: 'vertical',
        left: 'right',
        top: 'center',
        feature: {
            mark: { show: true },
            dataView: { show: true, readOnly: false },
            magicType: { show: true, type: ['line', 'bar', 'stack'] },
            restore: { show: true },
            saveAsImage: { show: true }
        }
    },
    xAxis: [
        {
            type: 'category',
            axisTick: { show: false },
            data: ['1999', '2004', '2009', '2014', '2019']
        }
    ],
    yAxis: [
        {
            type: 'value'
        }
    ],
    series: [
        {
            name: '男性人口',
            type: 'bar',
            barGap: 0,
            label: labelOption,
            emphasis: {
                focus: 'series'
            },
            data: [3037000, 3239000, 3447000, 3660000, 3873000]
        },
        {
            name: '男性吸烟人数',
            type: 'bar',
            label: labelOption,
            emphasis: {
                focus: 'series'
            },
            data: [858267, 880644, 914975, 931753, 950517]
        },
        {
            name: '女性人口',
            type: 'bar',
            label: labelOption,
            emphasis: {
                focus: 'series'
            },
            data: [2995000, 3190000, 3390000, 3599000, 3808000]
        },
        {
            name: '女性吸烟人数',
            type: 'bar',
            label: labelOption,
            emphasis: {
                focus: 'series'
            },
            data: [202321, 206488, 207419, 199350, 194300]
        }
    ]
};

option && myChart.setOption(option);

