<template>
  <v-card outlined>
    <v-card-title>File Selection</v-card-title>
    <v-card-text>
      <v-file-input
          truncate-length="20"
          show-size="true"
          accept="text/csv"
          placeholder="Select csv file to start."
      ></v-file-input>
    </v-card-text>

  </v-card>
</template>

<script>
export default {
  name: "FileSelector"
}
</script>

<style scoped>

</style>
