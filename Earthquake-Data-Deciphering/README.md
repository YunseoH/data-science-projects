# Earthquake Hazard Data Deciphering & Analysis 🏔️📊  

This project focuses on **deciphering a proprietary earthquake hazard data format**, parsing it into a structured **pandas.DataFrame**, and generating **visualizations**.

## Project Overview  
- **Deciphers** and **extracts** numerical earthquake data from a non-standard binary format.  
- Converts extracted data into a **structured tabular format** using Python and Pandas.  
- Analyzes key ground motion metrics, including **SS (0.2-sec ground motion intensity)** and **S1 (1.0-sec ground motion intensity)**.  
- Generates **visualizations** to identify trends, distributions, and correlations in the dataset.  

## Files in this Repository  
- **Decipher_code.py** – Python script to parse, process, and visualize the earthquake hazard data.  
- **Decipher.pdf** – Detailed report explaining the deciphering approach, analysis, and findings.  

## Technologies Used  
- **Python** (for data parsing and analysis)  
- **Pandas & NumPy** (for structuring data)  
- **Matplotlib & Seaborn** (for visualizations)  

## Key Visualizations & Insights  
### **1. Histograms of SS and S1**  
- The **SS (0.2-sec ground motion intensity)** values are more spread out than **S1 (1.0-sec ground motion intensity)**.  
- Higher intensity values (**>100**) appear frequently in SS but rarely in S1.  

### **2. Boxplots of SS and S1**  
- The **median SS** value (~20) is significantly higher than the **median S1** (~10).  
- Both distributions contain **outliers**, suggesting extreme seismic activity in some locations.  

### **3. Correlation Matrix Heatmap**  
- Strong **positive correlation** between SS and S1: areas with high SS tend to have high S1.  
- No significant correlation is observed between **latitude/longitude** and ground motion intensities.  

### **4. Scatter Plots Colored by SS and S1**  
- Each point represents a geographic location (latitude/longitude).  
- **SS and S1 exhibit a similar spatial gradient**, reinforcing their correlation.  
