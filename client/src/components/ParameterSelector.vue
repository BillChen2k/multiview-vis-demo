<template>
  <v-card outlined>
    <v-card-title>Parameter Tuner</v-card-title>
    <v-card-text>
      <p>
        Here you can alternate the parameters to get different results.<br>
        K1 and K2 are the weighting factors used in path recommendation, T1 and T2
        are the weighting factors used in infomation-layout recommendation.
      </p>
      <v-row no-gutters>
        <v-col class="pa-2" sm="2"><code>MV:</code></v-col>
        <v-col sm="4">
          <v-select :items="dataSource.mvcount"
                    v-model="parameter.mv"
                    placeholder="Select multivis count."
                    dense
          ></v-select>
        </v-col>
        <v-col class="pa-2" sm="6">
          <p>(Multi vis count)</p>
        </v-col>
      </v-row>

      <v-row no-gutters>
        <v-col class="pa-2" sm="2"><code>K1:</code></v-col>
        <v-col sm="4">
          <v-text-field
              dense
              v-model="parameter.k1"
          ></v-text-field>
        </v-col>
        <v-col class="pa-2" sm="2"><code>K2:</code></v-col>
        <v-col sm="4">
          <v-text-field
              dense
              v-model="parameter.k2"
          ></v-text-field>
        </v-col>
      </v-row>

      <v-row no-gutters>
        <v-col class="pa-2" sm="2"><code>T1:</code></v-col>
        <v-col sm="4">
          <v-text-field
              dense
              v-model="parameter.t1"
          ></v-text-field>
        </v-col>
        <v-col class="pa-2" sm="2"><code>T2:</code></v-col>
        <v-col sm="4">
          <v-text-field
              dense
              v-model="parameter.t2"
          ></v-text-field>
        </v-col>
      </v-row>

      <v-card-actions>
        <v-spacer></v-spacer>
        <v-btn depressed>Confirm</v-btn>
      </v-card-actions>

    </v-card-text>
  </v-card>
</template>

<script>
export default {
  name: "ParameterSelector",
  data: () => ({
    dataSource: {
      mvcount: [5,6,7]
    },
    parameter: {
      mv: 5,
      k1: 0.5,
      k2: 0.5,
      t1: 0.5,
      t2: 0.5
    }
  })
}
</script>

<style scoped>

</style>
