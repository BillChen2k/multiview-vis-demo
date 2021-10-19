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


export default {
  name: "FileSelector",
  data: () => ({
    columns: ["date", "carrier", "destcity", "depdelay", "arrdelay", "time"],
    selectedFile: null,
  }),
  mounted() {
    EventBus.$on(consts.events.WILL_POST_API, (e) => {

    })
  },
  methods: {
    didSelectFile: function() {
      console.log(this.selectedFile);
      if (this.selectedFile) {
        EventBus.$emit(consts.events.DID_SELECT_FILE, {});
      }
    },
    postForResult: function(columsToGenerate) {
      console.log(columsToGenerate);
      let formData = new FormData()
      if (this.selectedFile){
        formData.append("file", this.selectedFile)
        console.log(formData.getAll("file"))
        console.log(this.selectedFile)
        axios.post(consts.api + "/getcharts",
            {
              files: formData,
              cols: columsToGenerate
            },
            {
              headers: {
                'Content-Type': 'multipart/form-data'
              }
            }).then( response => {
          console.log('Success!')
          console.log({response})
        }).catch(error => {
          console.log({error})
        })
      }
    }
  }
}
</script>

<style scoped>

</style>
