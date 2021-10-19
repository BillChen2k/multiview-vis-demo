<template>
  <v-card outlined width="100%">
    <v-card-title>Multiview Chart Preview</v-card-title>

    <v-card-text>
      <!--    <LineChart :data="data" :options="{}" height="200px"></LineChart>-->
      <div v-show="dataFed">
        The layout you chose is: <b>{{ this.selectedLayoutCols.layout_name }}</b>
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
import LineChart from "./charts/LineChart";
import * as d3 from "d3";
import { EventBus } from "../plugins/event-bus";
import consts from "../config/consts.json";
import ExampleGraph from "../assets/graph/example_graph.json";

export default {
  name: "MultiviewChartPreview",
  components: {},
  data: () => ({
    dataFed: false,
    selectedLayoutCols: {},
    csvColumn: [],
    gridConfig: [],
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

    renderMultiviewGrid: function(rootGrid, rootDom, horizon = true) {
      console.log(rootGrid, rootDom, horizon);
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
        item.className = `multiview-item importance-${rootGrid.importance}`;
        item.setAttribute("id", `multiview-item-no${rootGrid.id}`);
        let text =document.createElement("p");
        text.innerHTML = `importance: ${rootGrid.importance} <br/> id: ${rootGrid.id}`;
        item.appendChild(text);
        rootDom.appendChild(item);
      }
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
  height: 500px;
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
  border: black 1px solid;
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
