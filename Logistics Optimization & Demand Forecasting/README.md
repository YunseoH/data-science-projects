# Logistics Optimization & Demand Forecasting 📦

This project was conducted during my internship at **LOGISALL** (Seoul, South Korea).  
It consists of two separate objectives:

1. **Optimizing logistics center locations** using GPS delivery data.
2. **Forecasting short-term vendor demand** to improve inventory planning.

---

## 1. Optimal Warehouse Location 🚚 

### Goal
Identify the most cost-efficient warehouse locations to minimize transportation distance and delivery costs.

### Approach
- Processed over **32,000+ GPS delivery data points**.
- Applied **K-Means clustering** to determine ideal central locations based on actual delivery patterns.
- Integrated **OpenStreetMap road network data** to compute realistic travel distances, estimating ~15% cost savings by relocating warehouses.

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

### Goal
Build lightweight models to predict short-term vendor-specific demand, enabling more precise procurement and reducing inventory risk.

### Approach
- Used **ARIMA & Prophet models** on vendor time series data.
- Improved forecast accuracy by ~20% vs. prior naive estimates.

### 📊 Data Schema (Quantity)
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
