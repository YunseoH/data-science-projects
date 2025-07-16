# Sportipy - Running Performance Analysis 🏃🏻‍♂️

Sportipy is a Python project that analyzes running performance data collected from Runtastic and TicExercise apps.  
It merges multi-source workout data, visualizes running habits, and identifies frequently visited workout zones via GPS clustering.

---

## Features

- **Data Processing:**  
  - Loads and merges workout files into a unified DataFrame.
  - Extracts key metrics like session time, location (longitude & latitude), heart rate, cumulative distance and duration.

- **Data Visualization:**  
  - `plot_distance_per_year` – Total distance run each year.
  - `plot_distance_distribution` – How far most runs typically are.
  - `plot_mean_speed_distribution` – Average speed across workouts.
  - `plot_start_of_run_distribution` – Common start times.
  - `trace_itineraries_with_heatmap` – Heatmap of most frequently visited running zones.

- **Clustering Workout Zones:**  
  - `get_clusters(df)` groups GPS coordinates to discover common running areas.

---

## Usage Example
```python
from sportipy import load_data, plot_distance_per_year, get_clusters

df = load_data("data/")
plot_distance_per_year(df, "distance_by_year.png")

clusters = get_clusters(df)
print(clusters.head())
```
---
## Project Structure
```
Sportipy/
├── data/           # Workout datasets from Runtastic & TicExercise
├── sportipy.py     # Core script: processing, visualization, clustering
├── output_plots/   # Generated plots
└── README.md
```
---

## Tech Stack
- Python: pandas, numpy, matplotlib, seaborn
- scikit-learn: For clustering GPS coordinates
- Folium / heatmap: To visualize most frequently visited locations

---

✅ This project helped me combine multi-source activity data into a unified analysis pipeline, revealing not just how much and how fast I run, but also where and when — providing a deeper understanding of my personal workout patterns.

📌 You can explore the plots in output_plots/ or customize the clustering parameters in sportipy.py to match your own running habits.
