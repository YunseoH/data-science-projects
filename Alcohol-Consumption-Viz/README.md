# Alcohol Consumption Data Visualization 🥂📊

This is a **D3.js-based interactive dashboard** that visualizes alcohol consumption across different countries and explores health impacts.

## Features
-  **World choropleth map**: Geographic patterns
-  **Bar chart**: Country-level comparisons
-  **Scatter plot**: Population vs. mortality
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
└── output/ # output plot
```

##  How to Run Locally
```bash
git clone https://github.com/YunseoH/data-science-projects.git
cd data-science-projects/Alcohol-Consumption-Viz
python3 -m http.server 8000
```
Then open http://localhost:8000/index.html in your browser.

## Technologies

- D3.js for visualization
- JavaScript (ES6+)
- Python HTTP Server
