function createScatterChart(dataset, color, dispatch) {
  let type, highlighted;
  let w = 1152;
  let h = 600;
  let marginTop = 32;
  let marginRight = 20;
  let marginBottom = 48;
  let marginLeft = 28;
  let minRadius = 2;
  let maxRadius = 40;

  const maxValue = d3.max(["beer", "wine", "spirits"], function (type) {
    return d3.max(dataset, function (d) {
      return d[type];
    });
  });
  let x = d3
    .scaleLinear()
    .domain([0, maxValue])
    .range([marginLeft, w - marginRight])
    .nice();

  let y = d3
    .scaleLinear()
    .domain([
      0,
      d3.max(dataset, function (d) {
        return d.mortality;
      }),
    ])
    .range([h - marginBottom, marginTop])
    .nice();

  let r = d3
    .scaleSqrt()
    .domain([
      0,
      d3.max(dataset, function (d) {
        return d.population;
      }),
    ])
    .range([minRadius, maxRadius]);

  let xAxis = d3.axisBottom(x).ticks(5);

  let yAxis = d3.axisLeft(y).ticks(5);

  let tooltip = d3.select("#tooltip");

  let svg = d3
    .select("#scatterChart")
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

  svg
    .append("text")
    .attr("class", "title")
    .attr("text-anchor", "end")
    .attr("x", w - marginRight)
    .attr("y", h - 8)
    .text("Annual per capita consumption (APC), in liters of pure alcohol");

  svg
    .append("g")
    .attr("class", "axis")
    .attr("transform", `translate(0,${h - marginBottom})`)
    .call(xAxis);

  svg
    .append("text")
    .attr("class", "title")
    .attr("y", 16)
    .text("Alcohol-attributable fraction (AAF), in %");

  svg
    .append("g")
    .attr("class", "axis")
    .attr("transform", `translate(${marginLeft},0)`)
    .call(yAxis);

  // Sort the data by population so the small countries won't be blocked by large countries.
  let sorted = dataset.slice().sort(function (a, b) {
    return d3.descending(a.population, b.population);
  });

  let country = svg
    .append("g")
    .selectAll("circle")
    .data(sorted, function (d) {
      return d.code;
    })
    .enter()
    .append("circle")
    .attr("class", "country")
    .attr("cursor", "pointer")
    .attr("r", function (d) {
      return r(d.population);
    })
    .attr("cx", y(0))
    .attr("cy", function (d) {
      return y(d.mortality);
    })
    .attr("fill", "#ebeff4")
    .attr("stroke", "#fff")
    .on("mouseover", function (event, d) {
      tooltip
        .classed("hidden", false)
        .style("top", `${event.pageY}px`)
        .style("left", `${event.pageX}px`).html(`
        <div><b>${d.name}</b></div>  
        <div>APC: <b>${d[type]} litres of ${type}</b></div>
        <div>AAF: <b>${d.mortality}%</b></div>
        <div>Population: <b>${d3.format(",")(d.population)}</b></div>
        <div><i>Click to toggle highlight</i></div>
        `);
    })
    .on("mouseout", function () {
      tooltip.classed("hidden", true);
    })
    .on("click", function (event, d) {
      dispatch.call(
        "countryhighlight",
        null,
        highlighted === d.code ? null : d.code
      );
    });

  dispatch.on("typechange.scatter", update);
  dispatch.on("countryhighlight.scatter", highlight);

  function update(newType) {
    type = newType;

    country
      .transition()
      .duration(500)
      .attr("cx", function (d) {
        return x(d[type]);
      })
      .attr("fill", function (d) {
        return color(d[type]);
      });
  }

  function highlight(newHighlighted) {
    highlighted = newHighlighted;

    country.classed("highlighted", function (d) {
      return highlighted === d.code;
    });
  }
}
