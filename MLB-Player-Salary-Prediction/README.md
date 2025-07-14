# MLB Player Salary Prediction ⚾️

This project predicts MLB player salaries using **regularized regression models** on player performance metrics.  
Separate models were built for batters and pitchers to capture their unique characteristics.

---

## Highlights
- Developed **Ridge and Lasso regression models** to predict salaries for batters and pitchers.
- Selected top features via `varImp` and correlation analysis to avoid multicollinearity.
- Applied **log transformation** to stabilize variance in salaries.
- Final **Lasso models** explained:
  - ~18.5% variance for batters
  - ~36.7% variance for pitchers
- Enforced MLB **minimum salary ($720k)** during prediction to realistically handle outliers and low projections.

---

## Tools & Libraries
- **R**: glmnet, caret, ggplot2, dplyr

---

## Project Structure
```
MLB-Player-Salary-Prediction/
├── MLB_Salary_Analysis.Rmd # R Markdown notebook with code & outputs
├── Final_Project_Report.pdf # Detailed methodology & results write-up
├── data/
│ ├── fangraphs-batter.csv
│ ├── fangraphs-pitcher.csv
│ ├── statcast-batter.csv
│ ├── statcast-pitcher.csv
│ └── mlb_salary_data.csv
└── README.md
```


---

## How It Works
- **Feature Engineering:** Combined Fangraphs & Statcast metrics with salary data to build comprehensive datasets for batters and pitchers.
- **Regularized Regression:** 
  - Used `glmnet` to train Ridge and Lasso models.
  - Compared RMSE and R² across models to pick the best.
- **Interpretation:** Identified most influential performance metrics on salaries.

---

## Results Snapshot
| Model    | Batters (R²) | Pitchers (R²) |
|----------|--------------|---------------|
| Lasso    | ~0.185       | ~0.367        |
| Ridge    | Slightly lower performance |

*Full detailed plots and residual diagnostics are available in `Final_Project_Report.pdf`.*
