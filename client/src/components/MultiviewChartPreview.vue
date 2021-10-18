<template>
  <v-card outlined width="100%">
    <v-card-title>Multiview Chart Preview</v-card-title>

    <v-card-text>
      <!--    <LineChart :data="data" :options="{}" height="200px"></LineChart>-->
      <v-row v-if="selectedLayout">

      </v-row>

    </v-card-text>
  </v-card>
</template>

<script>
import LineChart from "./charts/LineChart";
export default {
  name: "MultiviewChartPreview",
  components: {},
  data: () => ({
    selectedLayout: null,
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
    }
  })
}
</script>

<style scoped>

</style>
