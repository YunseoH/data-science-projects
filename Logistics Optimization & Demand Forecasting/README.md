# Logistics Optimization & Demand Forecasting 📦

This project was carried out during my internship at LOGISALL (Seoul, South Korea) to improve the efficiency of warehouse operations and inventory management.  

It focuses on two main challenges:
1. Optimizing warehouse locations based on actual GPS delivery patterns.
2. Forecasting short-term vendor-specific demand to minimize inventory risks.
   
---

## 1. Optimal Warehouse Location 🚚 

**Why?**  
The placement of warehouses is crucial to minimize transportation costs and delivery times. Existing warehouse sites were not necessarily aligned with the true delivery paths, leading to avoidable expenses.

**How?**  
- Processed over **32,000 GPS records** of delivery vehicles.
- Applied **K-Means clustering** to find natural delivery hubs from frequent routes.
- Used **OpenStreetMap (OSM) road network data** with `OSMnx` to calculate realistic travel distances and accessibility.

**Impact:**  
This approach identified an optimal warehouse relocation that could reduce average delivery distances by ~15%, translating into tangible cost savings.

**Data Schema (GPS)**

### Data Schema (GPS)

|    Column    |          Description           |
|--------------|--------------------------------|
| `vehicle_id` | Delivery vehicle ID            |
| `timestamp`  | Time of GPS record             |
| `move_x`     | X coordinate of movement       |
| `move_y`     | Y coordinate of movement       |
| `speed_km_s` | Speed in km/s                  |
| `center_x`   | Current warehouse X coordinate |
| `center_y`   | Current warehouse Y coordinate |

---

## 2. Demand Forecasting 📈 

**Why?**  
Accurate demand forecasts are critical to prevent costly overstock or stockouts. The goal was to build lightweight models suitable for operational environments.

**How?**  
- Developed per-vendor time series models using **ARIMA** (with log transforms & seasonality) and **Prophet** (daily trends).
- Applied outlier detection (IQR & Z-score) to stabilize data.
- Forecasted 30-day demand to support procurement planning.

**Impact:**  
The new models improved forecast accuracy by approximately **20%** compared to previous naive approaches.

### Data Schema (Quantity)
|     Column    | Description |
|---------------|--------------------------|
| `date`        | Year/Month of order      |
| `vendor_id`   | Vendor id                |
| `device_type` | Type of logistics device |
| `quantity`    | Units ordered            |

---

## Tech Stack
- **Python** (Pandas, Scikit-learn, Statsmodels, FbProphet)
- **OpenStreetMap / OSMnx** for realistic routing
- **Matplotlib, Seaborn** for analysis & plots
- **Jupyter Notebooks**

---

##  Data Privacy
>  Due to company confidentiality, no raw data is shared here.  
> Only summary results and sanitized schema information are provided.  

--

✅ This project gave me practical experience in applying clustering, geospatial analysis, and time series forecasting to solve real operational problems.
