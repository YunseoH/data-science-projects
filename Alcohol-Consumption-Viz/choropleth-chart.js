function createChoroplethChart(dataset, world, color, dispatch) {
  let type, highlighted;
  let w = 1152;
  let h = 500;

  let projection = d3.geoNaturalEarth1().fitSize([w, h], world);
  let path = d3.geoPath().projection(projection);

  let tooltip = d3.select("#tooltip");

  let svg = d3
    .select("#choroplethChart")
    .append("svg")
    .attr("width", w)
    .attr("height", h);

  svg
    .append("rect")
    .attr("width", w)
    .attr("height", h)
    .attr("fill", "#fff")
    .on("click", function () {
      dispatch.call("countryhighlight", null, null);
    });

  let country = svg
    .selectAll("path")
    .data(world.features, function (d) {
      return d.properties.iso_a3;
    })
    .enter()
    .append("path")
    .attr("class", "country")
    .attr("d", path)
    .attr("stroke", "#fff")
    .attr("fill", "#ebeff4");

  // Only attach mouse event to countries with data
  country
    .filter(function (d) {
      let code = d.properties.iso_a3;
      let e = dataset.find(function (e) {
        return e.code === code;
      });
      return e !== undefined;
    })
    .attr("cursor", "pointer")
    .on("mouseover", function (event, d) {
      // Move hovered country to the front
      d3.select(this).raise();

      let code = d.properties.iso_a3;
      let e = dataset.find(function (e) {
        return e.code === code;
      });
      tooltip
        .classed("hidden", false)
        .style("top", `${event.pageY}px`)
        .style("left", `${event.pageX}px`).html(`
      <div><b>${e.name}</b></div>  
      <div>APC: <b>${e[type]} litres of ${type}</b></div>
      <div><i>Click to toggle highlight</i></div>
      `);
    })
    .on("mouseout", function () {
      // Keep highlighted country to the front
      country
        .filter(function (d) {
          let code = d.properties.iso_a3;
          return highlighted === code;
        })
        .raise();

      tooltip.classed("hidden", true);
    })
    .on("click", function (event, d) {
      let code = d.properties.iso_a3;
      dispatch.call(
        "countryhighlight",
        null,
        highlighted === code ? null : code
      );
    });

  dispatch.on("typechange.choropleth", update);
  dispatch.on("countryhighlight.choropleth", highlight);

  function update(newType) {
    type = newType;

    country
      .transition()
      .duration(500)
      .attr("fill", function (d) {
        let code = d.properties.iso_a3;
        let e = dataset.find(function (e) {
          return e.code === code;
        });
        if (e) {
          return color(e[type]);
        } else {
          return "#ebeff4";
        }
      });
  }

  function highlight(newHighlighted) {
    highlighted = newHighlighted;

    country
      .classed("highlighted", function (d) {
        let code = d.properties.iso_a3;
        return highlighted === code;
      })
      // Move highlighted country to the front
      .filter(function (d) {
        let code = d.properties.iso_a3;
        return highlighted === code;
      })
      .raise();
  }
}
