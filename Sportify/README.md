# Sportipy - Running Performance Analysis 🏃🏻‍♂️

**Sportipy** is a Python project that analyzes running performance data collected from **Runtastic** and **TicExercise** applications.  
It focuses on **data processing, visualization, clustering**, and building predictive insights into running habits.

---

## Features

### Data Processing
- Merges workouts from multiple fitness apps into a unified DataFrame.
- Extracts key metrics:
  - `session`, `time`, `longitude`, `latitude`
  - `heart_rate_bpm`, `cumul_distance_m`, `cumul_time_sec`

### Data Visualization
Provides insightful plots to explore running behavior:
- `plot_distance_per_year(df, filename)` – Total distance per year.
- `plot_distance_distribution(df, filename)` – Distribution of distances run.
- `plot_mean_speed_distribution(df, filename)` – Speed across runs.
- `plot_start_of_run_distribution(df, filename)` – When runs typically start.
- `trace_itineraries_with_heatmap(df, filename)` – Heatmap of visited locations.

### Clustering Workout Zones
- `get_clusters(df)` identifies common workout zones based on GPS data using clustering algorithms.

---

## 📁 Project Structure
```
Sportipy/
├── data/ # Workout datasets from Runtastic & TicExercise
├── sportipy.py # Core script for processing, visualization & clustering
└── README.md
```

---

## Tech Stack
- **Python**: pandas, numpy, matplotlib, seaborn
- **scikit-learn**: For clustering GPS coordinates
- **Folium / heatmap**: To visualize frequent running zones

---

## Usage Example
```python
from sportipy import load_data, plot_distance_per_year, get_clusters

df = load_data("data/")
plot_distance_per_year(df, "distance_by_year.png")

clusters = get_clusters(df)
print(clusters.head())
```
