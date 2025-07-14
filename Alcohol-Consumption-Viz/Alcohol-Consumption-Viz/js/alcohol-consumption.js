Promise.all([
  d3.csv("alcohol-attributable-fraction-of-mortality.csv"),
  d3.csv("beer-consumption-per-person.csv"),
  d3.csv("wine-consumption-per-capita.csv"),
  d3.csv("spirits-consumption-per-person.csv"),
  d3.csv("population.csv"),
  d3.json("world.json"),
]).then(function (data) {
  //
  // DATA PARSING
  //

  let mortalityData = data[0];
  let beerData = data[1];
  let wineData = data[2];
  let spiritsData = data[3];
  let populationData = data[4];
  let world = data[5];

  // Combine all csv files by matching country name
  let dataset = [];
  for (let i = 0; i < mortalityData.length; i++) {
    let d = mortalityData[i];
    let name = d["Entity"];

    let beerDatum = beerData.find(function (e) {
      return e["Entity"] === name;
    });
    let wineDatum = wineData.find(function (e) {
      return e["Entity"] === name;
    });
    let spiritsDatum = spiritsData.find(function (e) {
      return e["Entity"] === name;
    });
    let populationDatum = populationData.find(function (e) {
      return e["Entity"] === name;
    });

    // Only keep the entry with all attributes available
    if (beerDatum && wineDatum && spiritsDatum && populationDatum) {
      let code = d["Code"];
      let mortality =
        +d[
          "Alcohol-attributable fractions, all-cause deaths (%) - Sex: both sexes"
        ];
      let beer =
        +beerDatum[
          "Alcohol, recorded per capita (15+) consumption (in litres of pure alcohol) - Beverage types: Beer"
        ];
      let wine =
        +wineDatum[
          "Alcohol, recorded per capita (15+) consumption (in litres of pure alcohol) - Beverage types: Wine"
        ];
      let spirits =
        +spiritsDatum[
          "Alcohol, recorded per capita (15+) consumption (in litres of pure alcohol) - Beverage types: Spirits"
        ];
      let population =
        +populationDatum[
          "Population - Sex: all - Age: all - Variant: estimates"
        ];

      dataset.push({
        name,
        code,
        mortality,
        beer,
        wine,
        spirits,
        population,
      });
    }
  }

  //
  // COLOR SCALE
  //

  // The color scale is shared by all three charts and it's kept consistent across different beverages to facilitate comparison
  let color = d3
    .scaleThreshold()
    .domain([0.1, 0.2, 0.5, 1, 2, 5, 10])
    .range([
      "#cff6fe",
      "#bcd7f3",
      "#a8b9e8",
      "#939bdd",
      "#7d7ed2",
      "#6662c6",
      "#4a46bb",
      "#242baf",
    ]);

  createColorLegend(color);

  //
  // INTERACTIVITY
  //

  let dispatch = d3.dispatch("typechange", "countryhighlight");

  // Handle beverage type change
  d3.selectAll("[name='type']").on("change", function (event) {
    let type = event.target.value;
    dispatch.call("typechange", null, type);
  });

  //
  // INITIALIZATION
  //
  createChoroplethChart(dataset, world, color, dispatch);
  createBarChart(dataset, color, dispatch);
  createScatterChart(dataset, color, dispatch);

  dispatch.call("typechange", null, "beer");
});
