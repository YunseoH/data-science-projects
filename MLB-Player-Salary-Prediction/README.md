# MLB Player Salary Prediction ⚾️

This project predicts Major League Baseball (MLB) player salaries using regularized regression models based on performance metrics from Fangraphs.  

It was primarily designed to explore which statistics most influence salary determination and to estimate earnings for players whose salaries are not publicly available.

---

## Highlights

- **Feature Engineering:**  
  Combined advanced metrics (like wOBA, xFIP, WAR) from Fangraphs and salary data into comprehensive datasets for both batters and pitchers.

- **Regularized Regression:**  
  Built separate Ridge and Lasso models for batters and pitchers to handle multicollinearity and improve interpretability, achieving R² scores of ~18.5% for batters and ~36.7% for pitchers after log transformation.

- **Minimum Salary Cap:**  
  Incorporated MLB’s minimum salary rule ($720,000) directly into predictions to produce realistic outputs.

---

## Data & Tools

- **Data:**  
  - Batters & pitchers performance stats (Fangraphs)  
  - Official MLB payroll data

- **Tech Stack:**  
  - R (`glmnet`, `caret`, `dplyr`, `ggplot2`)  
  - Extensive use of cross-validation for hyperparameter tuning

- **Project Structure:**

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

✅ This project gave me practical experience in applying regularized regression and transformation techniques to tackle multicollinearity and skewed distributions, ultimately deriving meaningful insights into how specific player metrics drive MLB salaries.

📌 For full methodology, residual diagnostics, and discussions on model improvement (like adding team budgets or player branding factors), see `Final_Project_Report.pdf`.
