# Business KPI Dashboard & Customer Segmentation Analysis

This project provides a comprehensive customer churn analysis platform with:
- **Step 1-3:** Business KPI Dashboard (Streamlit)
- **Step 4:** Customer Segmentation and Explainable Churn-Risk Prioritization Model

---

## Step 1-3: Business KPI Dashboard

Interactive Streamlit dashboard for real-time churn metrics.

### Features
- **KPI Metrics**: Overall Churn Rate, Retention Rate, Revenue at Risk (Monthly), Average Historical Customer Charges
- **Interactive Filtering**: Filter by Contract Type, Tenure range, Monthly Charges
- **Visualizations**: 
  - Churn Rate by Contract Type
  - Churn Distribution by Tenure
  - Revenue at Risk per Contract
  - Customer Segmentation Analysis (Spending vs Tenure)
- **Automatic Insights**: Business insights based on filtered data

### How to Run
```bash
pip install -r requirements.txt
streamlit run app.py
```

---

## Step 4: Customer Segmentation & Explainable Risk Scoring

Advanced analytics moving from descriptive to actionable customer segmentation and churn-risk prioritization.

### Deliverables

| File | Description |
|------|-------------|
| `notebooks/segmentation_and_risk_model.ipynb` | Complete executable notebook with all analysis |
| `data/customer_segmented.csv` | Original data + Cluster ID, Segment Name, Risk Score, Risk Category |
| `reports/segment_summary.csv` | Segment-level summary statistics |
| `reports/segment_analysis.md` | Detailed methodology, segment definitions, limitations |
| `reports/recommendation_memo.md` | Executive recommendation memo with prioritized actions |
| `reports/segmentation_visualizations/` | All generated charts (PNG) |

### Segmentation Approach

**Method:** K-Means clustering (K=4) on 9 features:
- **Financial:** Tenure, Monthly Charges, Total Charges
- **Service:** Contract Type, Online Security
- **Payment:** Payment Method
- **Demographic:** Senior Citizen, Partner, Dependents

**Preprocessing:**
- Numerical features: StandardScaler (zero mean, unit variance)
- Categorical features: Label Encoding
- **Churn target EXCLUDED** — prevents data leakage

**Cluster Selection:** Elbow Method + Silhouette Score (K=4 selected)

### Segment Definitions

| Cluster | Segment Name | Customers | Key Characteristics |
|---------|-------------|-----------|---------------------|
| 0 | Senior Vulnerable | 1,546 (15.5%) | 100% seniors, month-to-month, electronic check, no security |
| 1 | Budget-Conscious | 3,151 (31.5%) | Lowest charges, mailed check, has security |
| 2 | High-Value Long-Term | 2,343 (23.4%) | Highest tenure/charges, has security |
| 3 | New Vulnerable | 2,960 (29.6%) | Lowest tenure, auto-pay, no security |

### Risk Scoring Logic

**Transparent rule-based score (0-100)** — No Churn column used.

| Risk Factor | Conditions | Max Points |
|-------------|------------|------------|
| Tenure | ≤6 mo: 25, 7-12: 15, 13-24: 10, 25-48: 5, 48+: 0 | 25 |
| Monthly Charges | ≥$90: 20, $70-89: 15, $50-69: 10, $30-49: 5, <$30: 0 | 20 |
| Contract | Month-to-month: 25, One year: 10, Two year: 0 | 25 |
| Payment Method | Electronic check: 10, Mailed check: 5, Auto: 0 | 10 |
| Online Security | No: 10, No internet: 5, Yes: 0 | 10 |
| Senior Citizen | Yes: 5 | 5 |
| No Partner/Dependents | Both No: 5 | 5 |
| **TOTAL** | | **100** |

**Risk Categories:**
- **Low Risk:** 0-34 (27.9% of customers)
- **Medium Risk:** 35-59 (53.7%)
- **High Risk:** 60-100 (18.3%)

### How to Run the Notebook

```bash
# Install additional dependencies
pip install matplotlib seaborn scikit-learn

# Run notebook
jupyter notebook notebooks/segmentation_and_risk_model.ipynb
```

Or execute the analysis script:
```bash
python scripts/generate_visualizations.py
```

### Generated Visualizations

All saved to `reports/segmentation_visualizations/`:
1. `segment_distribution.png` — Customer count per segment
2. `avg_risk_by_segment.png` — Average risk score by segment
3. `segmentation_pca.png` — PCA projection of clusters
4. `risk_category_distribution.png` — Overall and by-segment risk distribution
5. `characteristics_comparison.png` — Box plots of tenure, charges, risk by segment
6. `churn_by_segment.png` — Historical churn rate by segment
7. `risk_score_churn_distribution.png` — Risk score distribution for churned vs retained
8. `cluster_selection.png` — Elbow and silhouette analysis

### Business Recommendations Summary

**Priority 1 — Senior Vulnerable:** Dedicated support line, contract upgrade incentives, auto-pay migration, free security bundle

**Priority 2 — Budget-Conscious:** Value tier plan, annual commitment discount, auto-pay nudges, usage alerts

**Priority 3 — High-Value Long-Term:** Loyalty program, price protection, dedicated account managers, premium perks

**Priority 4 — New Vulnerable:** Structured 30/60/90 onboarding, default-on security, first-year contract incentive, early warning system

### Model Limitations

1. **Not a predictive model** — Risk score is heuristic, not a probability
2. **No causal claims** — Correlations only; interventions should be tested
3. **Descriptive clustering** — Segments don't predict future behavior
4. **Static snapshot** — Refresh quarterly with new data
5. **No external validation** — Test on holdout/out-of-time data before production use
6. **Threshold sensitivity** — Business context should guide final thresholds

---

## Project Structure

```
churn_analysis/
├── app.py                          # Streamlit KPI Dashboard
├── requirements.txt                # Python dependencies
├── README.md                       # This file
├── data/
│   ├── churn_clean.csv            # Original cleaned dataset (10,000 rows)
│   └── customer_segmented.csv     # With Cluster ID, Segment, Risk Score
├── notebooks/
│   ├── analysis.ipynb             # Original EDA notebook
│   └── segmentation_and_risk_model.ipynb  # Step 4 complete notebook
├── reports/
│   ├── data_quality_summary.md
│   ├── quality_decision_log.json
│   ├── segment_summary.csv        # Segment-level statistics
│   ├── segment_analysis.md        # Detailed methodology
│   ├── recommendation_memo.md     # Executive memo
│   └── segmentation_visualizations/
│       ├── cluster_selection.png
│       ├── segment_distribution.png
│       ├── avg_risk_by_segment.png
│       ├── segmentation_pca.png
│       ├── risk_category_distribution.png
│       ├── characteristics_comparison.png
│       ├── churn_by_segment.png
│       └── risk_score_churn_distribution.png
└── scripts/
    └── generate_visualizations.py # Standalone visualization script
```

---

## Quick Start

```bash
# 1. Install dependencies
pip install -r requirements.txt
pip install matplotlib seaborn scikit-learn

# 2. Run KPI Dashboard
streamlit run app.py

# 3. Run Segmentation Analysis (generates all deliverables)
jupyter notebook notebooks/segmentation_and_risk_model.ipynb
# OR
python scripts/generate_visualizations.py
```

---

## Requirements

- Python 3.8+
- pandas, numpy
- streamlit, plotly (dashboard)
- matplotlib, seaborn (visualizations)
- scikit-learn (clustering, preprocessing)

Install all:
```bash
pip install pandas numpy streamlit plotly matplotlib seaborn scikit-learn
```