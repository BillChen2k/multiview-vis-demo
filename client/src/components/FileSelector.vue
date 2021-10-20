<template>
  <v-card outlined>
    <v-card-title>File Selection</v-card-title>
    <v-card-text>
      <form>
        <v-file-input
            dense
            truncate-length="30"
            show-size="true"
            accept="text/csv"
            placeholder="Select csv file to start."
            v-model="selectedFile"
            @change="didSelectFile"
        ></v-file-input>
      </form>
      <div v-if="selectedFile">
        <p class="mt-2">
          The file contains following columns:
        </p>
        <span  v-for="col in this.columns" :key="col">
         <code> {{ col }}</code>,
      </span>
      </div>


    </v-card-text>

  </v-card>
</template>

<script>
import axios from "axios";
import consts from "../config/consts.json";
import { EventBus } from "../plugins/event-bus";

const api = process.env.NODE_ENV == 'development' ? consts.api : 'api';

export default {
  name: "FileSelector",
  data: () => ({
    columns: ["date", "carrier", "destcity", "depdelay", "arrdelay", "time"],
    selectedFile: null,
  }),
  mounted() {
    EventBus.$on(consts.events.DID_SELECT_SUBVIEW, ({ grid_id, column_names, columns}) => {
      this.postForResult(columns);
    });
  },
  methods: {
    didSelectFile: function() {
      console.log(this.selectedFile);
      setTimeout(() => {
          EventBus.$emit(consts.events.DID_SELECT_FILE, { file: this.selectedFile });
      }, 100);
    },
    postForResult: function(columsToGenerate) {
      let formData = new FormData()
      if (this.selectedFile){
        formData.append("file", this.selectedFile)
        formData.append('cols', columsToGenerate);
        axios.post(api + "/getcharts",
            formData,
            {
              headers: {
                'Content-Type': 'multipart/form-data'
              }
            })
          .then( response => {
              console.log({response});
              EventBus.$emit(consts.events.DID_POST_API, { charts: response.data });
          }).catch(error => {
          console.log({error})
        });
      }
    }
  }
}
</script>

<style scoped>

</style>
