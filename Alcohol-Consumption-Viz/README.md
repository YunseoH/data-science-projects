# Alcohol Consumption Data Visualization 🥂📊

## About the Project
This project is a **D3.js-based interactive data visualization** that explores alcohol consumption across different countries. It includes:
- A **world choropleth map** to visualize geographic patterns.
- A **bar chart** to compare consumption levels.
- A **scatter plot** to analyze health impacts and population effects.
- A **radio button filter** to toggle between beer, wine, and spirits consumption.

## Project Structure
```
data-science-projects/
├── Alcohol-Consumption-Viz/          # Main project folder
│   ├── alcohol-consumption.html      # Main HTML file (entry point)
│   ├── alcohol-consumption.js        # JavaScript logic for data processing
│   ├── bar-chart.js                  # JavaScript for the bar chart
│   ├── choropleth-chart.js           # JavaScript for the world map
│   ├── scatter-chart.js              # JavaScript for the scatter plot
│   ├── color-legend.js               # JavaScript for color legend
│   ├── d3.js                         # D3.js library
│   ├── alcohol-attributable-fraction-of-mortality.csv
│   ├── beer-consumption-per-person.csv
│   ├── spirits-consumption-per-person.csv
│   ├── wine-consumption-per-capita.csv
│   ├── population.csv
│   ├── world.json
```

## 🚀 How to Run Locally
Since the project relies on **CSV files**, it must be run on a local server.

### **1. Download the Repository**
```sh
git clone https://github.com/YunseoH/data-science-projects.git
```

### **2. Navigate to the Project Folder**
```sh
cd data-science-projects/Alcohol-Consumption-Viz
```

### **3. Start a Local Server**
Since browsers block `d3.csv()` from loading local files directly, you need to run a local server:
**For Python 3 Users:**
```sh
python3 -m http.server 8000
```

### **4.  Open in Your Browser**
Once the server is running, open:
```sh
http://localhost:8000/alcohol-consumption.html
```

## Technologies Used
- **D3.js** for interactive visualizations.
- **JavaScript (ES6+)** for data manipulation.
- **Python HTTP Server** for local file hosting.

## Notes
- This project **requires running a local server** due to browser restrictions on loading CSV files.
- If the visualization doesn't load properly, check your browser's **Console (`F12 > Console`) for errors**.

