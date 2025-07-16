# Alcohol Consumption Data Visualization 🥂📊

This interactive dashboard explores how alcohol consumption patterns vary across countries and how they relate to alcohol-attributable health outcomes. Unlike static tables or simple charts, it allows users to dynamically toggle between beverage types, directly linking per capita consumption levels with alcohol-attributable fractions (AAF).

By enabling this interactive exploration, the dashboard uncovers interesting trends -- such as clusters of countries where higher spirit consumption aligns with elevated AAF percentages -- providing a more intuitive starting point for deeper public health analysis.

## Features
-  **World choropleth map**: Geographic patterns in per capita alcohol consumption.
-  **Bar chart**: Country-level comparisons
-  **Scatter plot**: Alcohol consumption vs. Alcohol-attributable fractions
-  **Radio filter**: Toggle between beer, wine, spirits

##  Project Structure
```
├── alcohol-consumption.html
├── js/
│ ├── alcohol-consumption.js
│ ├── bar-chart.js
│ ├── choropleth-chart.js
│ ├── scatter-chart.js
│ ├── color-legend.js
│ └── d3.js
├── data/
│ ├── alcohol-attributable-fraction-of-mortality.csv
│ ├── beer-consumption-per-person.csv
│ ├── spirits-consumption-per-person.csv
│ ├── wine-consumption-per-capita.csv
│ ├── population.csv
│ └── world.json
└── output.png # screenshot of the output plot
```

##  How to Run Locally
```bash
git clone https://github.com/YunseoH/data-science-projects.git
cd data-science-projects/Alcohol-Consumption-Viz
python3 -m http.server 8000
```
Then open http://localhost:8000/alcohol-consumption.html in your browser.

## Technologies

- D3.js for visualization
- JavaScript (ES6+)
- Python HTTP Server
