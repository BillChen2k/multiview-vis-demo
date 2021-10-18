<template>
  <v-card outlined width="100%">
    <v-card-title>Layouts</v-card-title>
    <v-card-text>
      <p>The depth of the color indicates the visual importance value of the layout.</p>
      <div class="d-inline-flex" style="overflow-x: auto; max-width: 700px">
          <div v-for="layout in layouts"  :key="layout.layout_name">

              <v-img
                  :src="layout.thumbnail"
                  width="64px" height="64px"
                  class="mx-1 hover-gray"
              ></v-img>

          <div class="px-6 text-sm-caption">
            <p>{{ layout.layout_name }}</p>
          </div>

          </div>
      </div>
    </v-card-text>

  </v-card>
</template>

<script>

import layoutData from '../config/layout-config.json';

export default {
  name: "LayoutViewer",

  data: () => ({
    layouts: layoutData.layouts,
  }),

  mounted() {
    this.layouts = this.layouts.map(one => {
      one.thumbnail = require(`@/${one.thumbnail}`);
      return one;
    })
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
