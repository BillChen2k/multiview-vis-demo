<template>
  <v-container fluid>
    <div ref="myChart" :style="{width: '100%', height: this.height}"></div>
  </v-container>
</template>

<script>
// 引入基本模板
// let echarts = require('echarts/lib/echarts');
// 引入柱状图组件
// require('echarts/lib/chart/bar');
// // 引入提示框和title组件
// require('echarts/lib/component/tooltip');
// require('echarts/lib/component/title');
// require('echarts/lib/component/grid');

import * as echarts from 'echarts';

export default {
  name: "echart",
  props:{
    tabledata: {
      required: true
    },
    height: {
      required: false,
      default: '280px'
    }
  },
  data: () => ({}),
  mounted() {
    this.drawchart()
  },
  methods: {
    draw2dbar(myechart){
      var xdata = []
      if(this.tabledata["x_data"].length == 1)
        xdata = this.tabledata["x_data"][0]
      else
        xdata =this.tabledata["x_data"]
      myechart.setOption({
        title: {
          text: this.tabledata["table_name"],
          subtext: this.tabledata["describe"],
          textStyle: {
            fontSize: "50%"
          },
          left: "center",
          top: "5%",
          padding: 5,
          itemGap: 10
        },
        xAxis: {
          type: 'category',
          data: xdata,
          name: this.tabledata["x_name"],
          axisLabel: {
            interval:0,//代表显示所有x轴标签显示
          }
        },
        yAxis: {
          type: 'value',
          name: this.tabledata["y_name"]
        },
        grid: {
          show: false,
          zlevel: 0,
          z: 2,
          top: "20%",
          bottom: "20%",
          containLabel: false,
          backgroundColor: "transparent",
          borderColor: "#ccc",
          borderWidth: 1
        },
        tooltip: {
          show: true,
          trigger: "item",
          triggerOn: "mousemove|click",
          axisPointer: {
            type: "line"
          },
          showContent: true,
          alwaysShowContent: false,
          showDelay: 0,
          hideDelay: 100,
          textStyle: {
            fontSize: 14
          },
          borderWidth: 0,
          padding: 5
        },
        toolbox:{
          show: true,
          orient: 'vertical',
          left: 'right',
          top: 'center',
          feature: {
            mark: {show: true},
            dataView: {show: true, readOnly: false},
            magicType: {show: true, type: [ 'bar', 'tiled']},
            restore: {show: true},
            saveAsImage: {show: true}
          }
        },
        series: {
          data: this.tabledata["y_data"][0],
          type: "bar"
        }
      });
    },
    draw2dline(myechart){
      var xdata = []
      if(this.tabledata["x_data"].length == 1)
        xdata = this.tabledata["x_data"][0]
      else
        xdata =this.tabledata["x_data"]
      myechart.setOption({
        title: {
          text: this.tabledata["table_name"],
          textStyle: {
            fontSize: "50%"
          },
          subtext: this.tabledata["describe"],
          left: "center",
          top: "5%",
          padding: 5,
          itemGap: 10
        },
        xAxis: {
          type: 'category',
          data: xdata,
          name: this.tabledata["x_name"]
        },
        yAxis: {
          type: 'value',
          name: this.tabledata["y_name"]
        },
        grid: {
          show: false,
          zlevel: 0,
          z: 2,
          top: "20%",
          bottom: "20%",
          containLabel: false,
          backgroundColor: "transparent",
          borderColor: "#ccc",
          borderWidth: 1
        },
        tooltip: {
          show: true,
          trigger: "item",
          triggerOn: "mousemove|click",
          axisPointer: {
            type: "line"
          },
          showContent: true,
          alwaysShowContent: false,
          showDelay: 0,
          hideDelay: 100,
          textStyle: {
            fontSize: 14
          },
          borderWidth: 0,
          padding: 5
        },
        toolbox:{
          show: true,
          orient: 'vertical',
          left: 'right',
          top: 'center',
          feature: {
            mark: {show: true},
            dataView: {show: true, readOnly: false},
            magicType: {show: true, type: ['line', 'tiled']},
            restore: {show: true},
            saveAsImage: {show: true}
          }
        },
        series: {
          data: this.tabledata["y_data"][0],
          type: "line"
        }
      });
    },
    draw2dpie(myechart){
      var mydata = []
      for(var i=0; i<this.tabledata["x_data"][0].length; i++){
        mydata.push({
          name: this.tabledata["x_data"][0][i],
          value: this.tabledata["y_data"][0][i]
        })
      }
      myechart.setOption({
        title: {
          text: this.tabledata["table_name"],
          textStyle: {
            fontSize: "50%"
          },
          subtext: this.tabledata["describe"],
          left: "center",
          top: "5%",
          padding: 5,
          itemGap: 10
        },
        legend: {
          data: this.tabledata["x_data"][0],
          selected: {},

        },
        grid: {
          show: false,
          zlevel: 0,
          z: 2,
          top: "20%",
          bottom: "20%",
          containLabel: false,
          backgroundColor: "transparent",
          borderColor: "#ccc",
          borderWidth: 1
        },
        tooltip: {
          show: true,
          trigger: "item",
          triggerOn: "mousemove|click",
          axisPointer: {
            type: "line"
          },
          showContent: true,
          alwaysShowContent: false,
          showDelay: 0,
          hideDelay: 100,
          textStyle: {
            fontSize: 14
          },
          borderWidth: 0,
          padding: 5
        },
        toolbox:{
          show: true,
          orient: 'vertical',
          left: 'right',
          top: 'center',
          feature: {
            mark: {show: true},
            dataView: {show: true, readOnly: false},
            // magicType: {show: true, type: ['line', 'bar', 'stack', 'tiled']},
            // restore: {show: true},
            saveAsImage: {show: true}
          }
        },
        series: {
          name: this.tabledata["y_name"],
          type: "pie",
          clockwise: true,
          data: mydata,
          radius : "60%",
          center: [
            "50%",
            "50%"
          ],
          label: {
            "show": true,
            "position": "top",
            "margin": 8
          },
          itemStyle: {
            emphasis: {
              shadowBlur: 10,
              shadowOffsetX: 0,
              shadowColor: 'rgba(0, 0, 0, 0.5)'
            },
            normal:{
              label:{
                show: true,
                formatter: '{b} : {c} ({d}%)'
              },
              labelLine :{show:true}
            }
          }

        }
      });

    },
    draw3dscatter(myechart){
      var myseries = []
      for(var i=0; i<this.tabledata["x_data"].length; i++){
        var mydata = []
        for(var j=0; j<this.tabledata["x_data"][i].length; j++){
          mydata.push([this.tabledata["x_data"][i][j],this.tabledata["y_data"][i][j]])
        }
        myseries.push(
            {
              type: "scatter",
              name: this.tabledata["classify"][i],
              symbolSize: 10,
              data: mydata,
              label: {
                show: false,
                position: "top",
                margin: 8
              }
            }
        )
      }
      myechart.setOption({
        title: {
          text: this.tabledata["table_name"],
          subtext: this.tabledata["describe"],
          textStyle: {
            fontSize: "50%"
          },
          left: "center",
          top: "5%",
          padding: 5,
          itemGap: 10
        },
        toolbox:{
          show: true,
          orient: 'vertical',
          left: 'right',
          top: 'center',
          feature: {
            mark: {show: true},
            dataView: {show: true, readOnly: false},
            // magicType: {show: true, type: ['line', 'bar', 'stack', 'tiled']},
            // restore: {show: true},
            saveAsImage: {show: true}
          }
        },
        tooltip: {
          show: true,
          trigger: "item",
          triggerOn: "mousemove|click",
          axisPointer: {
            type: "line"
          }
        },
        legend: {
          data: this.tabledata["classify"],
          show: true,
          padding: 5,
          itemGap: 10,
          itemWidth: 25,
          itemHeight: 14
        },
        grid: {
          show: false,
          zlevel: 0,
          z: 2,
          top: "20%",
          bottom: "20%",
          containLabel: false,
          backgroundColor: "transparent",
          borderColor: "#ccc",
          borderWidth: 1
        },
        xAxis: [
          {
            type: 'value',
            name: this.tabledata["x_name"],
            data: this.tabledata["x_data"][0]
          }
        ],
        yAxis: [
          {
            type: 'value',
            name: this.tabledata["y_name"]
          }
        ],
        series: myseries
      });
    },
    draw3dbar(myechart){
      var rawdata = this.tabledata
      var myseries = []
      for(var i=0; i<rawdata["classify"].length; i++){
        myseries.push({
          name: rawdata["classify"][i],
          type: 'bar',
          stack: 'stack1',
          data: rawdata["y_data"][i]
        })
      }
      var xdata = []
      if(rawdata["x_data"].length == 1)
        xdata = rawdata["x_data"][0]
      else
        xdata =rawdata["x_data"]
      myechart.setOption({
        title: {
          text: this.tabledata["table_name"],
          subtext: this.tabledata["describe"],
          textStyle: {
            fontSize: "50%"
          },
          left: "center",
          top: "5%",
          padding: 5,
          itemGap: 10
        },
        toolbox:{
          show: true,
          orient: 'vertical',
          left: 'right',
          top: 'center',
          feature: {
            mark: {show: true},
            dataView: {show: true, readOnly: false},
            magicType: {show: true, type: [ 'bar', 'stack', 'tiled']},
            restore: {show: true},
            saveAsImage: {show: true}

            // saveAsImage:{}
          }
        },
        tooltip: {
          show: true,
          trigger: "item",
          triggerOn: "mousemove|click",
          axisPointer: {
            type: "line"
          }
        },
        legend: {
          data: this.tabledata["classify"],
          show: true,
          padding: 5,
          itemGap: 10,
          itemWidth: 25,
          itemHeight: 14
        },
        grid: {
          show: false,
          zlevel: 0,
          z: 2,
          top: "20%",
          bottom: "20%",
          containLabel: false,
          backgroundColor: "transparent",
          borderColor: "#ccc",
          borderWidth: 1
        },
        xAxis: [
          {
            type: 'category',
            data: xdata,
            name: this.tabledata["x_name"],
            axisLabel: {
              interval:0,//代表显示所有x轴标签显示
            }
          }
        ],
        yAxis: [
          {
            type: 'value',
            name: this.tabledata["y_name"]
          }
        ],
        series: myseries
      });
    },
    draw3dline(myechart){
      var rawdata = this.tabledata
      var myseries = []
      for(var i=0; i<rawdata["classify"].length; i++){
        myseries.push({
          name: rawdata["classify"][i],
          type: 'line',
          stack: 'stack1',
          data: rawdata["y_data"][i]
        })
      }
      var xdata = []
      if(this.tabledata["x_data"].length == 1)
        xdata = this.tabledata["x_data"][0]
      else
        xdata =this.tabledata["x_data"]
      myechart.setOption({
        title: {
          text: this.tabledata["table_name"],
          subtext: this.tabledata["describe"],
          textStyle: {
            fontSize: "50%"
          },
          left: "center",
          top: "5%",
          padding: 5,
          itemGap: 10
        },
        toolbox:{
          show: true,
          orient: 'vertical',
          left: 'right',
          top: 'center',
          feature: {
            mark: {show: true},
            dataView: {show: true, readOnly: false},
            magicType: {show: true, type: ['line', 'stack', 'tiled']},
            restore: {show: true},
            saveAsImage: {show: true}
          }
        },
        tooltip: {
          show: true,
          trigger: "item",
          triggerOn: "mousemove|click",
          axisPointer: {
            type: "line"
          }
        },
        legend: {
          data: this.tabledata["classify"],
          show: true,
          padding: 5,
          itemGap: 10,
          itemWidth: 25,
          itemHeight: 14
        },
        grid: {
          show: false,
          zlevel: 0,
          z: 2,
          top: "20%",
          bottom: "20%",
          containLabel: false,
          backgroundColor: "transparent",
          borderColor: "#ccc",
          borderWidth: 1
        },
        xAxis: [
          {
            type: 'category',
            data: xdata,
            name: this.tabledata["x_name"]
          }
        ],
        yAxis: [
          {
            type: 'value',
            name: this.tabledata["y_name"]
          }
        ],
        series: myseries
      });
    },

    drawchart(){
      let myChart = echarts.init(this.$refs['myChart'])
      // 绘制图表
      if(this.tabledata["classify"].length != 0){
        if(this.tabledata["chart"]=="bar")
          this.draw3dbar(myChart)
        else if(this.tabledata["chart"]=="line")
          this.draw3dline(myChart)
        else
          this.draw3dscatter(myChart)
        console.log(this.tabledata["order1"])
      }
      else{
        if(this.tabledata["chart"]=="bar")
          this.draw2dbar(myChart)
        else if(this.tabledata["chart"]=="line")
          this.draw2dline(myChart)
        else if(this.tabledata["chart"]=="pie")
          this.draw2dpie(myChart)
        else
          this.draw3dscatter(myChart)
      }
    }
  }
}


</script>

<style scoped>

</style>
