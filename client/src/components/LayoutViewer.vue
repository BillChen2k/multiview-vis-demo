<template>
  <v-card outlined width="100%">
    <v-card-title>Layouts</v-card-title>
    <v-card-text v-if="dataFeeded">
      <p>The depth of the color indicates the visual importance value of the layout.<br/> Number below indicates the recommendation score of the layout.</p>

      <v-container style="margin: 0; padding: 0" fluid>
        <v-col class="d-inline-flex" style="overflow-x: auto;">

          <div v-for="[layout_cid, layout] in this.recommend_layout_cols"  :key="layout_cid">
            <v-tooltip top offset-overflow="12">
              <template v-slot:activator="{ on, attrs }">
                <div v-bind="attrs"
                     @click="selectLayoutCol(layout_cid)"
                     v-on="on">
                  <v-img
                      :src="layout.details.thumbnail"
                      width="64px" height="64px"
                      class="mr-1 hover-gray"
                      :id="layout_cid"

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
      </v-container>

    </v-card-text>

    <v-card-text v-else>
      No data selected.
    </v-card-text>

  </v-card>
</template>

<script>

import layoutData from '../config/layout-config.json';
import ExampleLayout from '../assets/graph/example_layout.json';
import { EventBus } from "../plugins/event-bus";
import consts from "../config/consts.json";

export default {
  name: "LayoutViewer",

  data: () => ({
    dataFeeded: false,
    layouts: layoutData.layouts,
    recommend_layout_cols: null,
  }),

  mounted() {
    EventBus.$on(consts.events.DID_SELECT_FILE, () => {
      this.dataFeeded = true;
      this.loadLayouts();
    });
  },

  methods: {
    loadLayouts: function() {
      this.layouts = this.layouts.map(one => {
        one.thumbnail = require(`@/${one.thumbnail}`);
        return one;
      })
      let allLayoutsCols = ExampleLayout.layout;
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

    selectLayoutCol: function(layout_cid) {
      const layout_cols = this.recommend_layout_cols.get(layout_cid);
      EventBus.$emit(consts.events.DID_SELECT_LAYOUT, {
        layout_cols
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
</style>
