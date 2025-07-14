function createBarChart(dataset, color, dispatch) {
  let type, highlighted;
  let w = 1152;
  let h = 500;
  let marginTop = 32;
  let marginRight = 1;
  let marginBottom = 8;
  let marginLeft = 20;

  let x = d3
    .scaleBand()
    .domain(
      dataset.map(function (d) {
        return d.code;
      })
    )
    .range([marginLeft, w - marginRight])
    .paddingInner(0.2);

  const maxValue = d3.max(["beer", "wine", "spirits"], function (type) {
    return d3.max(dataset, function (d) {
      return d[type];
    });
  });
  let y = d3
    .scaleLinear()
    .domain([0, maxValue])
    .range([h - marginBottom, marginTop])
    .nice();

  let yAxis = d3.axisLeft(y).ticks(5);

  let tooltip = d3.select("#tooltip");

  let svg = d3
    .select("#barChart")
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
    .attr("y", 16)
    .text("Annual per capita consumption, in liters of pure alcohol");

  svg
    .append("g")
    .attr("class", "axis")
    .attr("transform", `translate(${marginLeft},0)`)
    .call(yAxis)
    // Extent the zero tick line to span the whole chart
    .select(".tick line")
    .attr("x2", w - marginRight);

  let country = svg
    .append("g")
    .selectAll("rect")
    .data(dataset, function (d) {
      return d.code;
    })
    .enter()
    .append("rect")
    .attr("class", "country")
    .attr("cursor", "pointer")
    .attr("x", function (d) {
      return x(d.code);
    })
    .attr("width", x.bandwidth())
    .attr("y", y(0))
    .attr("height", 0)
    .attr("fill", "#ebeff4")
    .on("mouseover", function (event, d) {
      tooltip
        .classed("hidden", false)
        .style("top", `${event.pageY}px`)
        .style("left", `${event.pageX}px`).html(`
        <div><b>${d.name}</b></div>  
        <div>APC: <b>${d[type]} litres of ${type}</b></div>
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

  dispatch.on("typechange.bar", update);
  dispatch.on("countryhighlight.bar", highlight);

  function update(newType) {
    type = newType;

    let sorted = dataset.slice().sort(function (a, b) {
      return d3.descending(a[type], b[type]);
    });

    x.domain(
      sorted.map(function (d) {
        return d.code;
      })
    );

    country
      .transition()
      .duration(500)
      .attr("x", function (d) {
        return x(d.code);
      })
      .attr("y", function (d) {
        return y(d[type]);
      })
      .attr("height", function (d) {
        return y(0) - y(d[type]);
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
