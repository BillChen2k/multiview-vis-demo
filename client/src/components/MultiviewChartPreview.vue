<template>
  <v-card outlined width="100%">
    <v-card-title>Dashboard Preview</v-card-title>
    <v-card-text>
      <div v-show="dataFed">
        <v-row>
          <v-col sm="8">
            <p>The layout you chose is: <b>{{ this.selectedLayoutCols.layout_name }}</b></p>
          </v-col>
          <v-col sm="4" >
            <v-btn
                @click="downloadMultiview"
                style="top: -6px"
                class="float-sm-right"
                color="dark-grey"
                icon outlined>
              <v-icon>mdi-download</v-icon>
            </v-btn>
            <span class="float-sm-right mr-2">Download image:</span>
          </v-col>
        </v-row>
        <div id="multiview-container" class="multiview-container">

<!--                    <div class="multiview-container-row">-->
<!--                      <div class="multiview-container-col">-->
<!--                        <div class="multiview-item"></div>-->
<!--                      </div>-->
<!--                      <div class="multiview-container-col">-->
<!--                        <div class="multiview-container-row">-->
<!--                          <div class="multiview-container-col">-->
<!--                            <div class="multiview-item"></div>-->
<!--                          </div>-->
<!--                          <div class="multiview-container-col">-->
<!--                            <div class="multiview-item"></div>-->
<!--                          </div>-->
<!--                          <div class="multiview-container-col">-->
<!--                            <div class="multiview-item"></div>-->
<!--                          </div>-->
<!--                        </div>-->
<!--                        <div class="multiview-container-row">-->
<!--                          <div class="multiview-item"></div>-->
<!--                        </div>-->
<!--                      </div>-->
<!--                    </div>-->

        </div>
      </div>

      <div v-show="!dataFed">
        Please select a layout recommended for you in the upper panel.
      </div>

    </v-card-text>
  </v-card>
</template>

<script>
import * as d3 from "d3";
import { EventBus } from "../plugins/event-bus";
import consts from "../config/consts.json";
import ExampleGraph from "../assets/graph/example_graph.json";
import Echart from "./charts/EChart";
import Vue from "vue";
import html2canvas from "html2canvas"

export default {
  name: "MultiviewChartPreview",
  components: {},
  data: () => ({
    dataFed: false,
    selectedLayoutCols: {},
    selectedGridId: -1,
    csvColumnNames: new Map(),
    csvColumn: new Map(),
    gridConfig: [],
    chartData: new Map(),
    data: {
      labels: [
        'January',
        'February',
        'March',
        'April',
        'May',
        'June',
      ],
      datasets: [{
        label: 'This is just an example chart.',
        backgroundColor: 'rgb(255, 99, 132)',
        borderColor: 'rgb(255, 99, 132)',
        data: [0, 10, 5, 2, 20, 30, 45],
      }]
    },
  }),

  mounted() {
    EventBus.$on(consts.events.DID_SELECT_LAYOUT, ( { layout_cols }) => {
      console.log("did select layout");
      console.log(layout_cols);
      this.dataFed = true;
      // {
      //     "layout_name": "5C",
      //     "order": [4,5,7,8,0]
      //     "score": 1065.455995726375,
      //     "rank": 13,
      //     "details": {
      //       "layout_name": "5C",
      //       "thumbnail": "..",
      //       "mv_count": 5,
      //       "layout": []
      //       }
      // }
      this.selectedLayoutCols = layout_cols;
      this.prepareData();
    });

    EventBus.$on(consts.events.DID_SELECT_CHART_RESULT, ({ chartData }) => {
      this.injectChart(chartData);
    });
  },

  methods: {
    prepareData: function() {
      this.gridConfig = this.selectedLayoutCols.details.layout;
      this.selectedLayoutCols.order.forEach(one => {
        let node = ExampleGraph.vertex.filter(v => v.id == one)[0];
        let cols = node.cols;
        let cols_name = node.name.split("_");
      })
      let container = document.getElementById("multiview-container");
      while(container.firstChild) container.removeChild(container.firstChild);
      this.renderMultiviewGrid(this.gridConfig, container, true);
    },

    loadColumnName: function(grid_id, node_id) {
      let node = ExampleGraph.vertex.filter(one => one.id == node_id);
      let columnNames = node[0].name.split("_");
      this.csvColumnNames.set(grid_id, columnNames);
      this.csvColumn.set(grid_id, node[0].col);
      return columnNames;
    },

    renderMultiviewGrid: function(rootGrid, rootDom, horizon = true) {
      if (rootGrid instanceof Array) {
        for(let subGrid of rootGrid) {
          let subDom = document.createElement("div");
          subDom.className = horizon ? "multiview-container-row" : "multiview-container-col";
          rootDom.appendChild(subDom);
          this.renderMultiviewGrid(subGrid, subDom, !horizon);
        }
      }
      else {
        let item = document.createElement("div");
        item.addEventListener('click', (e) => {
          this.gridSelected(rootGrid.id);
        });
        item.className = `importance-${rootGrid.importance} multiview-item `;
        item.setAttribute("id", `multiview-item-no${rootGrid.id}`);
        const columnNames = this.loadColumnName(rootGrid.id, this.selectedLayoutCols.order[rootGrid.id]);
        let text = document.createElement("p");
        text.className = `pa-2`;
        text.innerHTML = `importance: ${rootGrid.importance} <br/> id: ${rootGrid.id} <br/> columns: ${columnNames.join(", ")}`;
        item.appendChild(text);
        rootDom.appendChild(item);
      }
    },

    gridSelected: function(grid_id) {

      if (this.selectedGridId == -1) {
        let gridDom = document.getElementById(`multiview-item-no${grid_id}`);
        gridDom.classList.add("multiview-selected");
        this.selectedGridId = grid_id;
        EventBus.$emit(consts.events.DID_SELECT_SUBVIEW, {
          grid_id: grid_id,
          column_names: this.csvColumnNames.get(grid_id),
          columns: this.csvColumn.get(grid_id)
        });
      }
      else {
        let oldGridDom = document.getElementById(`multiview-item-no${this.selectedGridId}`);
        oldGridDom.classList.remove("multiview-selected");
        if (this.selectedGridId == grid_id) {
          // Unselect
          this.selectedGridId = -1;
          EventBus.$emit(consts.events.DID_SELECT_SUBVIEW, {
            grid_id: -1,
            column_names: [],
            columns: []
          });
        }
        else {
          // Unselect and select new
          let gridDom = document.getElementById(`multiview-item-no${grid_id}`);
          gridDom.classList.add("multiview-selected");
          this.selectedGridId = grid_id;
          EventBus.$emit(consts.events.DID_SELECT_SUBVIEW, {
            grid_id: grid_id,
            column_names: this.csvColumnNames.get(grid_id),
            columns: this.csvColumn.get(grid_id)
          });
        }
      }
    },

    injectChart: function(chartData) {
      if (this.selectedGridId == -1) {
        console.warn("No grid selected.");
        return;
      }
      let gridDom = document.getElementById(`multiview-item-no${this.selectedGridId}`);
      gridDom.removeChild(gridDom.lastChild);     // remove text or echat component
      gridDom.classList.add("multiview-echart-item");
      for (let i of ["importance-1", "importance-2", "importance-3", "multiview-item"]) {
        gridDom.classList.remove(i);
      }
      let echartContainer = document.createElement("div");
      echartContainer.setAttribute("id", `multiview-echart-no${this.selectedGridId}`);
      gridDom.appendChild(echartContainer);

      let echartCtr = Vue.extend(Echart);
      let echart = new echartCtr({
        propsData: {
          tabledata: chartData,
          height: `${gridDom.offsetHeight - 30}px`
        }
      });
      echart.$mount(`#multiview-echart-no${this.selectedGridId}`);
      console.log("chart injected.");
    },

    downloadMultiview: function() {
      function saveAs(uri, filename) {
        let link = document.createElement('a');
        if (typeof link.download === 'string') {
          link.href = uri;
          link.download = filename;
          // Firefox requires the link to be in the body
          document.body.appendChild(link);
          //simulate click
          link.click();
          //remove the link when done
          document.body.removeChild(link);
        } else {
          window.open(uri);
        }
      }
      html2canvas(document.getElementById("multiview-container")).then( (canvas) => {
          // canvas is the final rendered <canvas> element
          saveAs(canvas.toDataURL(), `Multiview_${new Date().getTime()}.png`);
          console.log("Image captured.");
      })
    }

  }
}
</script>

<style>
.multiview-container {
  display: flex;
  flex-direction: column;
  flex-wrap: nowrap;
  width: 100%;
  height: 700px;
}

.multiview-container-row {
  display: flex;
  flex: 1;
  flex-direction: row;
  flex-wrap: nowrap;
  justify-content: center;
}

.multiview-container-col {
  display: flex;
  flex: 1;
  flex-direction: column;
  flex-wrap: nowrap;
  justify-content: center;
  flex: 1
}

.multiview-item {
  flex: 1;
  background-color: aliceblue;
  border: white 2px solid;
  border-radius: 6px;
  transition-duration: 0.3s;
}

.multiview-item:hover {
  background-color: #eaf9ff;
}

.multiview-echart-item {
  flex: 1;
  background-color: white;
  border: #dcdcdc 1px solid;
  /*box-shadow: #CECECE 2px 2px 2px;*/
  margin: 2px;
  border-radius: 6px;
  transition-duration: 0.3s;
}

.multiview-selected {
  background-color: #fcd9bd !important;
  font-weight: bold;
}

.importance-1 {
  background-color: #9E9E9E;
}

.importance-2 {
  background-color: #B5B5B5;
}

.importance-3 {
  background-color: #CECECE;
}

.importance-4 {
  background-color: #E0E0E0;
}

</style>
