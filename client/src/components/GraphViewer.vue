<template>
  <v-card outlined  width="100%">
    <v-card-title>Graph Viewer</v-card-title>
    <v-card-text>
      <div v-if="dataFeeded">
        <v-container fluid id="graph-container">
          <v-col id="graph"></v-col>
        </v-container>
      </div>
      <div v-else>
        No data selected.
      </div>

    </v-card-text>
  </v-card>
</template>

<script>

import * as d3 from "d3";
import { EventBus } from "../plugins/event-bus";
import consts from "../config/consts.json";

export default {
  name: "GraphViewer",
  data: () => ({
    dataFeeded: false,
    graph: {
      vertex: [],
      edges: []
    }
  }),
  mounted() {
    this.generateGraph();
    EventBus.$on(consts.events.GRAPH_DATA_LOADED, (e) => {
      alert(e.msg);

    })
  },
  methods: {
    generateGraph: () => {
      console.log("Generating Graph");
      const w = d3.select("#graph-container").attr("width");
      const h = 500;
      const svg = d3
          .select("#arc")
          .append("svg")
          .attr("width", w)
          .attr("height", h);

      svg.append("g")
    }
  }
}
</script>

<style scoped>

</style>
