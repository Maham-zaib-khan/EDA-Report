# EDA-Report
This project demonstrates the health risk of heart patients based on their lifestyle, health issues, and many other features using a public survey dataset.
# 🫀 CDC Cardiovascular Risk Factor Analysis

[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://www.python.org/)
[![Pandas](https://img.shields.io/badge/Pandas-2.0+-green.svg)](https://pandas.pydata.org/)
[![Seaborn](https://img.shields.io/badge/Seaborn-0.12+-orange.svg)](https://seaborn.pydata.org/)

## Executive Summary
An exploratory analysis of 319,795 CDC survey records to pinpoint demographic, behavioral, and comorbidity risk factors associated with heart disease. Designed to inform targeted health interventions and guide downstream predictive modeling strategies.

---

## 💡 Key Business Insights

1. **Age Disparity:** Heart disease prevalence scales exponentially from **1.5%** in adults under 40 to **22.5%** in individuals aged 80+.
2. **Stroke Comorbidity:** Individuals with a history of stroke exhibit a **36.4%** heart disease rate vs. **7.5%** without.
3. **Lifestyle Impact:** Current smokers face **2x the risk** compared to non-smokers (12.1% vs 6.0%), while regular physical activity reduces prevalence by ~43%.
4. **Data Challenge (Class Imbalance):** Only 8.5% of dataset respondents report heart disease—requiring PR-AUC optimization over standard accuracy metrics.

---

## 📊 Visual Highlights

| Risk Factor | Insight Visualization |
|---|---|
| **Age Progression** | *Add a high-resolution screenshot of your Age Category bar chart here* |
| **Comorbidity Heatmap** | *Add a screenshot of your correlation matrix here* |

---

## ⚙️ How to Run

1. Clone the repository:
   ```bash
   git clone [https://github.com/yourusername/cdc-cardiovascular-risk-analysis.git](https://github.com/yourusername/cdc-cardiovascular-risk-analysis.git)
   cd cdc-cardiovascular-risk-analysis
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the notebook in Jupyter:
   ```bash
   jupyter notebook notebooks/01_exploratory_data_analysis.ipynb
   ```
