# Data Quality Audit Summary - Customer Churn Dataset

## Executive Summary
This report documents the data quality audit and cleaning process applied to the customer churn dataset. The raw dataset contained 10,100 records and suffered from common issues: missing values, exact/logical duplicates, incorrect dtypes (e.g., numeric charges stored as strings), outliers, and inconsistent categorical labels.

Following the cleaning pipeline, the final dataset contains 10,000 clean records.

## Issue Audit & Decisions

| Column | Issue | Action | Rationale |
| :--- | :--- | :--- | :--- |
| `MonthlyCharges` | Missing values, outliers | Median Impute, Flag outliers | Median is robust; IQR-based flags provide transparency. |
| `TotalCharges` | Wrong type (str), blanks, logical mismatches | Contextual Impute | Blanks=New (0); else tenure*monthly. |
| `Dependents` | Missing values | Mode Impute | Preserves class balance for low missingness. |
| `Churn`/`Contract` | Inconsistent categories | Standardize | Eliminates aliases ("yes", "y", "Month-to-month") |

## Summary Stats Before/After
- **Original Rows:** 10,100
- **Final Rows:** 10,000 (after removing duplicates)
- **Missing Values:** 0 (after imputation)
- **Data Types:** All columns now adhere to strict numeric/categorical standards.

## Assumptions & Limitations
- Imputation methods were conservative.
- Outliers were flagged but not removed, as they might be legitimate (high usage) or need domain-specific review.
- Logical flags capture data-entry errors but do not auto-correct to avoid bias.

## Reproducibility
The cleaning process is deterministic. Running `scripts/clean_pipeline.py` or the provided notebook will regenerate `data/churn_clean.csv` from `data/originals/customer_churn_raw.csv`.
