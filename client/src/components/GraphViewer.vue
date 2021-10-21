<template>
  <v-card outlined  width="100%">
    <v-card-title>Information Network</v-card-title>
    <v-card-text>
      <div v-show="dataFeeded">
        <v-container fluid id="graph-container">
          <v-col id="graph"></v-col>
        </v-container>
        The name of the node indicates the combination of two columns in the csv file. The width of the edges indicate the score of each connection.
      </div>
      <div v-show="!dataFeeded">
        No data selected.
      </div>
    </v-card-text>
  </v-card>
</template>

<script>

import * as d3 from "d3";
import { EventBus } from "../plugins/event-bus";
import consts from "../config/consts.json";
import exampleGraph from "../assets/graph/example_graph.json";

export default {
  name: "GraphViewer",
  data: () => ({
    dataFeeded: false,
    graph: {
      vertex: exampleGraph.vertex,
      edges: exampleGraph.edge
    }
  }),
  mounted() {
    EventBus.$on(consts.events.DID_SELECT_PARAMETER, ( { parameter, graphData, layoutData }) => {
      console.log("did select param.");
      this.dataFeeded = true;
      //todo: Feed the graph
      this.generateGraph();
    });
    EventBus.$on(consts.events.DID_SELECT_FILE, ({ file }) => {
      if (!file) this.dataFeeded = false;
    });

  },
  methods: {
    forceGraph: function({
                           nodes, // an iterable of node objects (typically [{id}, …])
                           links // an iterable of link objects (typically [{source, target}, …])
                         }, {
                           nodeId = d => d.id, // given d in nodes, returns a unique identifier (string)
                           nodeGroup, // given d in nodes, returns an (ordinal) value for color
                           nodeGroups, // an array of ordinal values representing the node groups
                           nodeTitle, // given d in nodes, a title string
                           nodeFill = "currentColor", // node stroke fill (if not using a group color encoding)
                           nodeStroke = "#fff", // node stroke color
                           nodeStrokeWidth = 1.5, // node stroke width, in pixels
                           nodeStrokeOpacity = 1, // node stroke opacity
                           nodeRadius = 5, // node radius, in pixels
                           linkSource = ({source}) => source, // given d in links, returns a node identifier string
                           linkTarget = ({target}) => target, // given d in links, returns a node identifier string
                           linkStroke = "#bdbdbd", // link stroke color
                           linkStrokeOpacity = 0.6, // link stroke opacity
                           linkStrokeWidth = 0.5, // given d in links, returns a stroke width in pixels
                           linkStrokeLinecap = "round", // link stroke linecap
                           colors = d3.schemeTableau10, // an array of color strings, for the node groups
                           width = 640, // outer width, in pixels
                           height = 300, // outer height, in pixels
                           invalidation // when this promise resolves, stop the simulation
                         } = {})
    {
      // Compute values.
      const N = d3.map(nodes, nodeId).map(intern);
      const LS = d3.map(links, linkSource).map(intern);
      const LT = d3.map(links, linkTarget).map(intern);
      const NR = d3.map(nodes, d => d.score).map(intern);
      if (nodeTitle === undefined) nodeTitle = (_, i) => N[i];
      const T = nodeTitle == null ? null : d3.map(nodes, nodeTitle);
      const G = nodeGroup == null ? null : d3.map(nodes, nodeGroup).map(intern);
      const W = typeof linkStrokeWidth !== "function" ? null : d3.map(links, linkStrokeWidth);
      const Important = d3.map(links, (l) => l.important);

      // Replace the input nodes and links with mutable objects for the simulation.
      nodes = d3.map(nodes, (_, i) => ({id: N[i]}));
      links = d3.map(links, (_, i) => ({source: LS[i], target: LT[i]}));

      // Compute default domains.
      if (G && nodeGroups === undefined) nodeGroups = d3.sort(G);

      // Construct the scales.
      const color = nodeGroup == null ? null : d3.scaleOrdinal(nodeGroups, colors);

      const simulation = d3.forceSimulation(nodes)
          // .alphaMin(0.9)
          .force("link", d3.forceLink(links).id(({index: i}) => N[i]).distance(120))
          .force("charge", d3.forceManyBody().strength(({index: i}) => Math.pow(-NR[i], 3)))
          .force("center", d3.forceCenter())
          .on("tick", ticked);

      const svg = d3.create("svg")
          .attr("id", "graphsvg")
          .attr("width", width)
          .attr("height", height)
          .attr("viewBox", [-width / 2, -height / 2, width, height])
          .attr("style", "max-width: 100%; height: auto; height: intrinsic;");

      const link = svg.append("g")
          .attr("stroke", linkStroke)
          .attr("stroke-opacity", linkStrokeOpacity)
          .attr("stroke-width", typeof linkStrokeWidth !== "function" ? linkStrokeWidth : null)
          .attr("stroke-linecap", linkStrokeLinecap)
          .selectAll("line")
          .data(links)
          .join("line");

      const node = svg.append("g")
          .selectAll(".node")
          .data(nodes)
          .join("g")
          .attr("fill", nodeFill)
          .attr("stroke-opacity", nodeStrokeOpacity)
          .attr("stroke-width", nodeStrokeWidth)
          .call(drag(simulation));

      const circle = node.append('circle')
          .attr("r", nodeRadius)
          .attr("stroke", nodeStroke)
          .attr("fill", color);

      if (W) link.attr("stroke-width", ({index: i}) => W[i]);
      if (Important) link.attr("stroke", (e) => {let i = e.index; return Important[i] ? "#c65555" : "#BDBDBD";});
      if (G) node.attr("fill", ({index: i}) => color(G[i]));
      if (T) {
        node.append("text")
            .text(({index: i}) => T[i])
            .style('fill', 'black').style('font-size', '12px')
            .attr('x', 12)
            .attr('y', 3);
        node.append("text")
            .text(({index: i}) => `id = ${i}, score = ${NR[i].toFixed(2)}`)
            .style('fill', 'black').style('font-size', '12px')
            .attr('x', 12)
            .attr('y', 16);
      }
      if (NR) circle.attr("r", ({index: i}) => NR[i]);

      if (invalidation != null) invalidation.then(() => simulation.stop());

      function intern(value) {
        return value !== null && typeof value === "object" ? value.valueOf() : value;
      }

      function ticked() {
        link
            .attr("x1", d => d.source.x)
            .attr("y1", d => d.source.y)
            .attr("x2", d => d.target.x)
            .attr("y2", d => d.target.y);

        node
            .attr("transform", d => `translate(${d.x}, ${d.y})`);
            // .attr("cx", d => d.x)
            // .attr("cy", d => d.y);
      }

      function drag(simulation) {
        function dragstarted(event) {
          if (!event.active) simulation.alphaTarget(0.3).restart();
          event.subject.fx = event.subject.x;
          event.subject.fy = event.subject.y;
        }

        function dragged(event) {
          event.subject.fx = event.x;
          event.subject.fy = event.y;
        }

        function dragended(event) {
          if (!event.active) simulation.alphaTarget(0);
          event.subject.fx = null;
          event.subject.fy = null;
        }

        return d3.drag()
            .on("start", dragstarted)
            .on("drag", dragged)
            .on("end", dragended);
      }

      return Object.assign(svg.node(), { scales: { color } } );

    },

    generateGraph: function() {
      // let node = svg.append("g")
      //   .selectAll("nodes")
      //   .data(this.graph.vertex)
      //   .enter();
      //
      // let circle = node.append("circle")
      //   .attr("cx", () => {return Math.random() * w})
      //   .attr("cy", () => {return Math.random() * h})
      //   .attr("r", (node) => { return 2 * node.score})
      //   .style("fill", "#34323d");

      let edges = [];
      let path = Object.keys(exampleGraph.tree)[0].trim().split(" ").map(one => parseInt(one));
      console.warn(path);
      for (let i = 0; i < this.graph.edges.length; i++) {
        for(let j = 0; j < this.graph.edges.length; j++) {
          edges.push( {
            source: i,
            target: j,
            value: this.graph.edges[i][j],
            important: path.includes(i) && path.includes(j) && Math.abs(path.indexOf(i) - path.indexOf(j)) === 1 ? true : false
          } );
        }
      }
      console.log(edges);
      let margin = {top: 0, right: 0, bottom: 0, left: 0};
      const w = 350 - margin.left - margin.right;
      const h = 350 - margin.top - margin.bottom;

      const graphDom = this.forceGraph({nodes: this.graph.vertex, links: edges},
          {
            nodeId: d => d.id,
            nodeGroup: d => 0,
            nodeTitle: d => d.name,
            linkStroke: "#bdbdbd",
            linkStrokeWidth: l => Math.pow(l.value, 2) / 150,
            width: w,
            height: h,
            // invalidation // a promise to stop the simulation when the cell is re-run
          });
      let graphContainer = document.getElementById("graph");
      while(graphContainer.firstChild) graphContainer.removeChild(graphContainer.firstChild);
      graphContainer.appendChild(graphDom);
      const svg = d3.select("#graphsvg");

    }
  }
}
</script>

<style scoped>

</style>
