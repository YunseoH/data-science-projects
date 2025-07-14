# MLB Player Salary Prediction ⚾️

Predicts MLB player salaries using regularized regression on performance metrics.

## Highlights
- Built Ridge and Lasso models to predict salaries separately for batters and pitchers.
- Selected top features based on varImp and correlation analysis.
- Applied log transformation to stabilize variance; final Lasso models explained ~18.5% variance for batters, ~36.7% for pitchers.
- Enforced MLB minimum salary ($720k) to realistically impute low salaries.

## Tools
- R (glmnet, caret, ggplot2, dplyr)

## Files
- `Final_Project_Report.pdf`: Detailed write-up of methodology & results
- `MLB_Salary_Analysis.Rmd`: R Markdown analysis
- `data/`: Fangraphs, Statcast, and salary datasets
