# Sportipy - Running Performance Analysis 🏃🏻‍♂️

## Project Overview
Sportipy is a Python-based project that analyzes running performance data collected from **Runtastic** and **TicExercise** applications. The project focuses on **data processing, visualization, clustering, and predictive modeling** to gain insights into running patterns.

## Project Structure
- **data/** - Includes workout datasets from Runtastic and TicExercise.
- **sportipy.py** - The main Python script implementing data processing and analysis functions.
  
## Features
### 1. Data Processing
- **Merging workout data** from different applications into a single DataFrame.
- Extracting key variables: `session`, `time`, `longitude`, `latitude`, `heart_rate_bpm`, `cumul_distance_m`, `cumul_time_sec`.

### 2. Data Visualization
Includes functions to generate key insights:
- `plot_distance_per_year(df, filename)` - Total distance per year.
- `plot_distance_distribution(df, filename)` - Distance run distribution.
- `plot_mean_speed_distribution(df, filename)` - Speed distribution per run.
- `plot_start_of_run_distribution(df, filename)` - Running start time distribution.
- `trace_itineraries_with_heatmap(df, filename)` - Heatmap of visited locations.

### 3. Clustering
- `get_clusters(df)`: Identifies workout zones based on GPS data.

