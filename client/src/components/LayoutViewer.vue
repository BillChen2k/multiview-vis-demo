<template>
  <v-card outlined width="100%">
    <v-card-title>Layout Gallary</v-card-title>
    <v-card-text v-if="dataFeeded">
      <p>The depth of the color indicates the visual importance value of the layout.<br/> Number below indicates the recommendation score of the layout.</p>

      <v-container style="margin: 0; padding: 0" fluid>
        <v-row>
          <v-col  sm="10" class=" d-inline-flex" style="overflow-x: auto;"
                  @mouseleave="leaveLayout"
          >
            <div v-for="[layout_cid, layout] in this.recommend_layout_cols"  :key="layout_cid">
              <v-tooltip top>
                <template v-slot:activator="{ on, attrs }">
                  <div v-bind="attrs"
                       @click="selectLayoutCol(layout_cid)"
                       :class="selectedLayoutCols.layout_name == layout.layout_name ? 'layout-item layout-selected' : 'layout-item'"
                       v-on="on">
                    <v-img
                        :src="layout.details.thumbnail"
                        width="64px" height="64px"
                        class="mr-1 hover-gray"
                        :id="layout_cid"
                        @mouseenter="hoverOnLayout(layout.layout_name)"
                    ></v-img>
                    <div class="px-6 text-sm-caption">
                      <span> {{ layout.layout_name }} </span>
                    </div>
                    <div class="text-sm-caption text-center">
                      <span> {{ layout.score.toFixed(2) }}</span>
                    </div>
                  </div>

                </template>

                <span>Path: {{ layout.order.toString() }}</span>
              </v-tooltip>


            </div>
          </v-col>
          <v-col sm="2">
            <v-img :src="layoutGraphImg"
                   transition="true"
                class="img-layoutgraph float-sm-right" width="96px" height="96px"></v-img>
          </v-col>
        </v-row>

      </v-container>

    </v-card-text>

    <v-card-text v-else>
      No data selected.
    </v-card-text>

  </v-card>
</template>

<script>

import layoutData from '../config/layout-config.json';
import ExampleGraph from '../assets/graph/example_graph.json';
import { EventBus } from "../plugins/event-bus";
import consts from "../config/consts.json";

const defaultLayoutGraph = require(`@/assets/layouts/layoutgraph/00.png`);

export default {
  name: "LayoutViewer",

  data: () => ({
    dataFeeded: false,
    layouts: layoutData.layouts,
    recommend_layout_cols: null,
    layoutGraphImg: defaultLayoutGraph,
    layoutGraphImgMap: new Map(),
    selectedLayoutCols: {}
  }),

  mounted() {
    EventBus.$on(consts.events.DID_SELECT_PARAMETER, ({ layoutDaya, graphData }) => {
      this.dataFeeded = true;
      //todo: Feed layout
      this.loadLayouts();
    });
    EventBus.$on(consts.events.DID_SELECT_FILE, ({ file }) => {
      if (!file) {
        this.dataFeeded = false;
        EventBus.$emit(consts.events.DID_SELECT_LAYOUT, {layout_cols: null});
      }
    });
  },

  methods: {
    loadLayouts: function(layoutColsAll) {
      this.layouts = this.layouts.map(one => {
        one.thumbnail = require(`@/${one.thumbnail}`);
        this.layoutGraphImgMap.set(one.layout_name, require(`@/${one.layoutgraph}`));
        return one;
      })
      let allLayoutsCols = layoutColsAll || ExampleGraph.layout;
      allLayoutsCols.sort((a, b) => {
        return b.score - a.score;
      });
      let recommend_layout_cols = new Map();
      let nameLayoutMap = new Map();
      this.layouts.forEach(one => { nameLayoutMap.set(one["layout_name"], one); });
      for (const [i, layout] of allLayoutsCols.entries()) {
        if (!recommend_layout_cols.has(layout["layout_name"])) {
          recommend_layout_cols.set(layout["layout_name"], {...layout, rank: i, details: nameLayoutMap.get(layout["layout_name"])});
        }
        if (recommend_layout_cols.size == 8) {
          // break; //todo: uncomment
        }
      }
      console.log(recommend_layout_cols);
      this.recommend_layout_cols = recommend_layout_cols;
    },

    hoverOnLayout: function(layout_name) {
     this.layoutGraphImg = this.layoutGraphImgMap.get(layout_name);
    },

    leaveLayout: function() {
      if (this.selectedLayoutCols.layout_name) {
        this.layoutGraphImg = this.layoutGraphImgMap.get(this.selectedLayoutCols.layout_name);
      }
      else {
        this.layoutGraphImg = defaultLayoutGraph;
      }
    },

    selectLayoutCol: function(layout_cid) {
      const layout_cols = this.recommend_layout_cols.get(layout_cid);
      this.selectedLayoutCols = layout_cols;
      EventBus.$emit(consts.events.DID_SELECT_LAYOUT, {
        layout_cols: layout_cols
      });
    }
  }


}

</script>

<style scoped>
.hover-gray {
  transition-duration: 0.5s;
}
.hover-gray:hover {
  opacity: 0.5;
}

.img-layoutgraph {
  border: #CECECE 1px solid;
  border-radius: 4px;
}

.layout-item {
  border-radius: 4px;
  border: #FFFFFF 1px solid;
  transition-duration: 0.3s;
}

.layout-selected {
  box-sizing: border-box;
  -moz-box-sizing: border-box;
  -webkit-box-sizing: border-box;
  border: #B5B5B5 1px solid;
  border-radius: 4px;
}
</style>
