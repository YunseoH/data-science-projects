function createColorLegend(color) {
  let w = 800;
  let h = 64;
  let marginTop = 24;
  let marginRight = 1;
  let marginBottom = 24;
  let marginLeft = 1;

  let x = d3
    .scaleBand()
    .domain(color.range())
    .range([marginLeft, w - marginRight]);

  let svg = d3
    .select("#colorLegend")
    .append("svg")
    .attr("width", w)
    .attr("height", h);

  svg
    .append("text")
    .attr("class", "title")
    .attr("y", 16)
    .text("Annual per capita consumption (APC), in liters of pure alcohol");

  svg
    .append("g")
    .selectAll("rect")
    .data(color.range())
    .enter()
    .append("rect")
    .attr("x", function (d) {
      return x(d);
    })
    .attr("y", marginTop)
    .attr("width", x.bandwidth())
    .attr("height", h - marginTop - marginBottom)
    .attr("fill", function (d) {
      return d;
    });

  svg
    .append("g")
    .attr("text-anchor", "middle")
    .attr("transform", `translate(0,${h - marginBottom})`)
    .selectAll("text")
    .data(color.range())
    .enter()
    .append("text")
    .attr("y", 20)
    .attr("x", function (d) {
      return x(d) + x.bandwidth() / 2;
    })
    .text(function (d) {
      let [min, max] = color.invertExtent(d);
      if (min === undefined) {
        // The first tick
        return `Less than ${max}`;
      } else if (max === undefined) {
        // The last tick
        return `${min} or more`;
      } else {
        return `${min}-${max}`;
      }
    });
}
