# Segment Analysis Report

**Executive Analytics Capstone Internship - Step 4**  
Customer Segmentation and Explainable Churn-Risk Prioritization Model

---

## 1. Executive Summary

This report presents the results of customer segmentation and explainable churn-risk scoring for 10,000 telecom customers. Using K-Means clustering on behavioral, financial, and service features (excluding the Churn target), we identified **4 distinct customer segments**. A transparent rule-based risk scoring system (0-100) was developed to prioritize retention efforts without using the actual Churn column.

---

## 2. Segmentation Methodology

### 2.1 Features Used for Clustering

| Feature Type | Features |
|--------------|----------|
| **Financial** | Tenure (months), Monthly Charges ($), Total Charges ($) |
| **Service** | Contract Type, Internet Service, Online Security |
| **Payment** | Payment Method |
| **Demographic** | Senior Citizen, Partner, Dependents |

**Excluded (to prevent data leakage):** CustomerID, Churn, outlier flags, logical flags

### 2.2 Preprocessing

- **Numerical features:** Standardized using StandardScaler (zero mean, unit variance)
- **Categorical features:** Label encoded (Contract, PaymentMethod, Dependents, Partner, OnlineSecurity)
- **No missing values** in the dataset

### 2.3 Cluster Selection

| K | Inertia | Silhouette Score |
|---|---------|------------------|
| 2 | 57,797 | 0.174 |
| 3 | 49,981 | 0.193 |
| **4** | **44,163** | **0.176** |
| 5 | 41,010 | 0.162 |
| 6 | 38,529 | 0.159 |

**Selected K = 4** based on elbow method (clear inflection at K=4) and reasonable silhouette score.

### 2.4 Clustering Algorithm

- **Algorithm:** K-Means (n_init=10, random_state=42)
- **Final Silhouette Score:** 0.176
- **PCA Explained Variance (2 components):** 44.4%

---

## 3. Segment Definitions

| Cluster ID | Segment Name | Customer Count | % of Base |
|------------|--------------|----------------|-----------|
| 0 | **Senior Vulnerable Customers** | 1,546 | 15.5% |
| 1 | **Budget-Conscious Customers** | 3,151 | 31.5% |
| 2 | **High-Value Long-Term Customers** | 2,343 | 23.4% |
| 3 | **New Vulnerable Customers** | 2,960 | 29.6% |

### 3.1 Senior Vulnerable Customers (Cluster 0)
- **Profile:** All senior citizens (100%), Month-to-month contract, Electronic check payment, No online security
- **Tenure:** 34.7 months (moderate)
- **Monthly Charges:** $67.17 (moderate)
- **Total Charges:** $2,283 (moderate)
- **Historical Churn Rate:** 75.0%
- **Avg Risk Score:** 47.0
- **% High Risk:** 25.9%

**Key Risk Factors:** Senior citizen status, month-to-month contract, electronic check, no online security

### 3.2 Budget-Conscious Customers (Cluster 1)
- **Profile:** Non-seniors, Month-to-month contract, Mailed check payment, Has online security
- **Tenure:** 28.8 months (lower)
- **Monthly Charges:** $59.49 (lowest)
- **Total Charges:** $1,510 (lowest)
- **Historical Churn Rate:** 75.3%
- **Avg Risk Score:** 45.1
- **% High Risk:** 23.9%

**Key Risk Factors:** Month-to-month contract, mailed check, lower tenure

### 3.3 High-Value Long-Term Customers (Cluster 2)
- **Profile:** Mostly non-seniors (97%), Month-to-month contract, Electronic check payment, Has online security
- **Tenure:** 56.2 months (highest)
- **Monthly Charges:** $91.76 (highest)
- **Total Charges:** $5,092 (highest)
- **Historical Churn Rate:** 76.2%
- **Avg Risk Score:** 41.6
- **% High Risk:** 13.2%

**Key Risk Factors:** High monthly charges, month-to-month contract, electronic check  
**Mitigating Factors:** Long tenure, online security

### 3.4 New Vulnerable Customers (Cluster 3)
- **Profile:** Non-seniors, Month-to-month contract, Bank transfer (automatic), No online security
- **Tenure:** 28.4 months (lowest)
- **Monthly Charges:** $61.64 (low)
- **Total Charges:** $1,535 (low)
- **Historical Churn Rate:** 74.0%
- **Avg Risk Score:** 38.2
- **% High Risk:** 12.6%

**Key Risk Factors:** Low tenure, month-to-month contract, no online security  
**Mitigating Factors:** Automatic payment method

---

## 4. Risk Scoring Methodology

### 4.1 Scoring Rules (0-100 Scale)

| Risk Factor | Condition | Points | Max Points |
|-------------|-----------|--------|------------|
| **Tenure** | ≤ 6 months | 25 | 25 |
| | 7-12 months | 15 | |
| | 13-24 months | 10 | |
| | 25-48 months | 5 | |
| | 48+ months | 0 | |
| **Monthly Charges** | ≥ $90 | 20 | 20 |
| | $70-89 | 15 | |
| | $50-69 | 10 | |
| | $30-49 | 5 | |
| | < $30 | 0 | |
| **Contract Type** | Month-to-month | 25 | 25 |
| | One year | 10 | |
| | Two year | 0 | |
| **Payment Method** | Electronic check | 10 | 10 |
| | Mailed check | 5 | |
| | Automatic (CC/Bank) | 0 | |
| **Online Security** | No | 10 | 10 |
| | No internet service | 5 | |
| | Yes | 0 | |
| **Senior Citizen** | Yes | 5 | 5 |
| **No Partner/Dependents** | Both No | 5 | 5 |
| **TOTAL** | | | **100** |

### 4.2 Risk Categories

| Category | Score Range | Customer Count | Percentage |
|----------|-------------|----------------|------------|
| **Low Risk** | 0-34 | 2,793 | 27.9% |
| **Medium Risk** | 35-59 | 5,374 | 53.7% |
| **High Risk** | 60-100 | 1,833 | 18.3% |

### 4.3 Risk Score Distribution by Segment

| Segment | Avg Risk Score | % High Risk | Historical Churn Rate |
|---------|----------------|-------------|----------------------|
| Senior Vulnerable | 47.0 | 25.9% | 75.0% |
| Budget-Conscious | 45.1 | 23.9% | 75.3% |
| High-Value Long-Term | 41.6 | 13.2% | 76.2% |
| New Vulnerable | 38.2 | 12.6% | 74.0% |

---

## 5. Key Findings

1. **All segments show high historical churn rates (74-76%)** — This dataset has an overall 75% churn rate, which is unusually high. The segmentation reveals nuances in *why* different groups churn.

2. **Senior Vulnerable Customers have the highest risk scores** — Driven by senior status, month-to-month contracts, electronic check payments, and lack of online security.

3. **High-Value Long-Term Customers have the lowest % High Risk** — Despite highest charges and month-to-month contracts, their long tenure and security adoption mitigate risk.

4. **New Vulnerable Customers have lowest average risk score** — But still show 74% historical churn, suggesting tenure is a dominant factor not fully captured in scoring.

5. **Risk score correlates with historical churn** — Higher risk scores generally align with higher historical churn, validating the heuristic approach.

---

## 6. Model Limitations

1. **Rule-based score is not a predictive model** — The risk score (0-100) is a heuristic based on domain knowledge, not a trained probability. It should not be interpreted as a guaranteed prediction of churn.

2. **No causal claims** — The scoring rules identify correlations from historical data, not causal relationships. Acting on these factors may not directly prevent churn.

3. **Clustering is descriptive, not predictive** — K-Means segments customers based on feature similarity. Cluster assignments do not predict future behavior.

4. **Historical churn rate is retrospective** — The actual churn rates shown are historical observations for segment evaluation only. They were not used to create segments or risk scores.

5. **Feature selection bias** — The segmentation features were chosen based on availability and domain relevance. Other unobserved factors (competitor offers, life events) may drive churn.

6. **Static snapshot** — The analysis uses a single point-in-time dataset. Customer behavior evolves; segments and scores should be refreshed periodically.

7. **Threshold sensitivity** — Risk category thresholds (35, 60) are heuristic. Business context should guide final threshold selection.

8. **Cluster stability** — K-Means results can vary with initialization. The analysis uses n_init=10 and fixed random_state for reproducibility.

9. **No external validation** — The model has not been validated on out-of-time or out-of-sample data. Performance on new customers is unknown.

10. **High overall churn rate (75%)** — The dataset shows an unusually high churn rate, which may not be representative of all telecom populations.

---

## 7. Conclusion

The segmentation and risk scoring framework provides a transparent, explainable approach to customer prioritization. Four distinct segments were identified with actionable characteristics, and a rule-based risk score enables business stakeholders to understand and act on risk factors without requiring ML expertise.

**Next Steps:** Validate on holdout data, A/B test retention interventions by segment, refresh quarterly, and consider supervised modeling for probability calibration.