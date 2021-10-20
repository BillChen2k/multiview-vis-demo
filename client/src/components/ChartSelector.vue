<template>
  <v-card outlined :loading="loading">
    <v-card-title>Candidate Charts</v-card-title>
    <v-card-text v-if="selectedViewId == -1">
      No view selected.
    </v-card-text>
    <v-card-text v-else>
      <p>
        Generated following chart recommendation based on column: <br>
        <b>{{ columnNames.join(", ") }}</b>.
      </p>

      <template v-for="(item, index) in chartData">
        <v-row @click="didSelectChartData(index)" :key="index" class="chart-container mb-2 mx-1">
          <echart :tabledata="item" height="208px" ></echart>
        </v-row>
      </template>
    </v-card-text>
  </v-card>
</template>

<script>
import { EventBus } from "../plugins/event-bus";
import consts from "../config/consts.json";
import Echart from "./charts/EChart";


export default {
  name: "ChartSelector.vue",
  components: {Echart},
  data: () => ({
    selectedViewId: -1,
    columnNames: [],
    columns: [],
    chartData: [],
    loading: false
  }),
  methods: {
    didSelectChartData: function(chart_id) {
      console.log("Chart result selected", chart_id);
      EventBus.$emit(consts.events.DID_SELECT_CHART_RESULT, {
        chartData: this.chartData[chart_id]
      });
    }
  },
  mounted() {
    EventBus.$on(consts.events.DID_SELECT_SUBVIEW, ({ grid_id, column_names, columns}) => {
      this.selectedViewId = grid_id;
      this.columnNames = [...column_names];
      this.columns = [...columns];
      this.chartData = [];
      if (grid_id != -1) this.loading = true;
    });
    EventBus.$on(consts.events.DID_SELECT_LAYOUT, e => {
      this.chartData = [];
      this.selectedViewId = -1;
    })
    EventBus.$on(consts.events.DID_POST_API, ( { charts }) => {
      console.log("Received chart data.");
      console.log(charts);
      charts = charts.map(one => { one.table_name = " "; return one;});
      this.loading = false;
      this.chartData = charts;
    })

  }
}
</script>

<style scoped>

.chart-container {
  border: #CECECE solid 1px;
  border-radius: 6px;
  transition-duration: 0.3s;
}

.chart-container:hover {
  background-color: aliceblue;
}
</style>
