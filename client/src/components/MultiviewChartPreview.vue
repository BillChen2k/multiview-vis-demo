<template>
  <v-card outlined width="100%">
    <v-card-title>Multiview Chart Preview</v-card-title>
    <LineChart :data="data" :options="{}" height="200px"></LineChart>
  </v-card>
</template>

<script>
import LineChart from "./charts/LineChart";
export default {
  name: "MultiviewChartPreview",
  components: {LineChart},

  data: () => ({
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
        label: 'My First dataset',
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
