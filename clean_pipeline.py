"""
Reproducible cleaning pipeline for the customer churn dataset.
All functions are deterministic (seeded) and can be re-run from raw data.
"""
import pandas as pd
import numpy as np
from pathlib import Path

RAW_PATH = Path("churn_analysis/data/originals/customer_churn_raw.csv")
CLEAN_PATH = Path("churn_analysis/data/churn_clean.csv")

# ----------------------------------------------------------------------
# STEP 1: LOAD RAW (preserving originals)
# ----------------------------------------------------------------------
def load_raw(path=RAW_PATH):
    """Load raw CSV with all columns as strings to preserve original values."""
    return pd.read_csv(path, dtype=str)

# ----------------------------------------------------------------------
# STEP 2: DEDUPLICATION
# ----------------------------------------------------------------------
def deduplicate(df):
    """
    Remove exact duplicates first, then resolve CustomerID conflicts.
    Strategy: keep the first occurrence for exact duplicates.
    For duplicate CustomerIDs with different data, keep the row with
    the most complete data (fewest NaN/blank), then first occurrence.
    """
    df = df.copy()

    # Exact duplicates
    before = len(df)
    df = df.drop_duplicates(keep="first")
    exact_removed = before - len(df)

    # CustomerID duplicates (non-exact)
    dup_mask = df.duplicated(subset=["CustomerID"], keep=False)
    if dup_mask.any():
        dup_ids = df[dup_mask]["CustomerID"].unique()
        rows_to_keep = []
        for cid in dup_ids:
            subset = df[df["CustomerID"] == cid]
            # Score: fewer missing/blank = better
            missing_count = subset.apply(lambda r: r.isna().sum() + (r.astype(str).str.strip() == "").sum(), axis=1)
            # Keep the row with minimum missing
            best_idx = missing_count.idxmin()
            rows_to_keep.append(best_idx)
        # Keep selected + all non-duplicate rows
        keep_mask = df.index.isin(rows_to_keep) | ~dup_mask
        df = df[keep_mask]

    id_removed = before - exact_removed - len(df)
    return df, {"exact_removed": exact_removed, "id_conflicts_resolved": id_removed}

# ----------------------------------------------------------------------
# STEP 3: MISSING VALUE HANDLING
# ----------------------------------------------------------------------
def handle_missing(df):
    """
    Column-specific missing value strategy with justification.
    """
    df = df.copy()
    log = {}

    # MonthlyCharges: numeric, ~2% missing -> median impute (robust to outliers)
    mc_missing = df["MonthlyCharges"].isna().sum()
    df["MonthlyCharges"] = pd.to_numeric(df["MonthlyCharges"], errors="coerce")
    mc_median = df["MonthlyCharges"].median()
    df["MonthlyCharges"] = df["MonthlyCharges"].fillna(mc_median)
    log["MonthlyCharges"] = {"action": "median_impute", "value": mc_median, "count": int(mc_missing),
                             "rationale": "Numeric, low missingness (~2%), median robust to outliers"}

    # TotalCharges: stored as string, blanks represent 0 (new customers) or missing
    # Convert blanks to NaN, then to numeric
    tc_blank = (df["TotalCharges"].astype(str).str.strip() == "").sum()
    df["TotalCharges"] = df["TotalCharges"].replace(r"^\s*$", np.nan, regex=True)
    df["TotalCharges"] = pd.to_numeric(df["TotalCharges"], errors="coerce")

    # For tenure=0, TotalCharges should be 0 (new customer)
    # For tenure>0 but missing, impute as tenure * MonthlyCharges
    tc_missing = df["TotalCharges"].isna().sum()
    mask_new = df["tenure"].astype(str).str.strip().astype(int) == 0
    df.loc[mask_new & df["TotalCharges"].isna(), "TotalCharges"] = 0
    mask_missing = df["TotalCharges"].isna() & (df["tenure"].astype(str).str.strip().astype(int) > 0)
    df.loc[mask_missing, "TotalCharges"] = df.loc[mask_missing, "tenure"].astype(int) * df.loc[mask_missing, "MonthlyCharges"]
    log["TotalCharges"] = {"action": "contextual_impute", "blanks_as_zero": int(tc_blank),
                           "imputed_from_formula": int(tc_missing - tc_blank) if tc_missing > tc_blank else 0,
                           "rationale": "Blanks = new customers (tenure=0) -> 0; others derived from tenure*MonthlyCharges"}

    # Dependents: categorical, ~1.5% missing -> mode impute (conservative)
    dep_missing = df["Dependents"].isna().sum()
    dep_mode = df["Dependents"].mode()[0] if not df["Dependents"].mode().empty else "No"
    df["Dependents"] = df["Dependents"].fillna(dep_mode)
    log["Dependents"] = {"action": "mode_impute", "value": dep_mode, "count": int(dep_missing),
                         "rationale": "Categorical, low missingness, mode preserves class balance"}

    return df, log

# ----------------------------------------------------------------------
# STEP 4: TYPE CORRECTION
# ----------------------------------------------------------------------
def correct_types(df):
    """Convert columns to appropriate dtypes."""
    df = df.copy()

    # Numeric
    df["tenure"] = pd.to_numeric(df["tenure"], errors="coerce").astype("Int64")
    df["MonthlyCharges"] = pd.to_numeric(df["MonthlyCharges"], errors="coerce").astype("float64")
    df["TotalCharges"] = pd.to_numeric(df["TotalCharges"], errors="coerce").astype("float64")

    # Binary (0/1 int)
    df["SeniorCitizen"] = pd.to_numeric(df["SeniorCitizen"], errors="coerce").astype("Int64")

    # Categorical - strip whitespace, standardize case
    cat_cols = ["Contract", "PaymentMethod", "Dependents", "Partner", "OnlineSecurity", "Churn"]
    for c in cat_cols:
        df[c] = df[c].astype(str).str.strip()

    return df

# ----------------------------------------------------------------------
# STEP 5: CATEGORICAL STANDARDIZATION
# ----------------------------------------------------------------------
def standardize_categoricals(df):
    """Fix inconsistent categories (case, aliases, trailing spaces)."""
    df = df.copy()
    log = {}

    # Churn: Yes/No only
    before = df["Churn"].value_counts().to_dict()
    mapping_churn = {"yes": "Yes", "y": "Yes", "Yes": "Yes", "no": "No", "n": "No", "No": "No"}
    df["Churn"] = df["Churn"].str.lower().map(mapping_churn).fillna(df["Churn"])
    after = df["Churn"].value_counts().to_dict()
    log["Churn"] = {"before": before, "after": after}

    # Contract
    before = df["Contract"].value_counts().to_dict()
    mapping_contract = {"month-to-month": "Month-to-month", "Month-to-month": "Month-to-month",
                        "one year": "One year", "One year": "One year",
                        "two year": "Two year", "Two year": "Two year"}
    df["Contract"] = df["Contract"].str.lower().map(mapping_contract).fillna(df["Contract"])
    after = df["Contract"].value_counts().to_dict()
    log["Contract"] = {"before": before, "after": after}

    # PaymentMethod
    before = df["PaymentMethod"].value_counts().to_dict()
    mapping_pm = {
        "electronic check": "Electronic check", "Electronic check": "Electronic check",
        "mailed check": "Mailed check", "Mailed check": "Mailed check",
        "bank transfer (automatic)": "Bank transfer (automatic)", "Bank transfer (automatic)": "Bank transfer (automatic)",
        "credit card (automatic)": "Credit card (automatic)", "Credit card (automatic)": "Credit card (automatic)"
    }
    df["PaymentMethod"] = df["PaymentMethod"].str.lower().map(mapping_pm).fillna(df["PaymentMethod"])
    after = df["PaymentMethod"].value_counts().to_dict()
    log["PaymentMethod"] = {"before": before, "after": after}

    # Dependents, Partner: Yes/No
    for col in ["Dependents", "Partner"]:
        before = df[col].value_counts().to_dict()
        mapping = {"yes": "Yes", "y": "Yes", "Yes": "Yes", "no": "No", "n": "No", "No": "No"}
        df[col] = df[col].str.lower().map(mapping).fillna(df[col])
        after = df[col].value_counts().to_dict()
        log[col] = {"before": before, "after": after}

    return df, log

# ----------------------------------------------------------------------
# STEP 6: OUTLIER FLAGGING (NOT DELETION)
# ----------------------------------------------------------------------
def flag_outliers(df):
    """
    Flag outliers via IQR method. Add boolean columns, do NOT delete.
    """
    df = df.copy()
    flags = {}

    for col in ["tenure", "MonthlyCharges", "TotalCharges"]:
        s = pd.to_numeric(df[col], errors="coerce")
        q1, q3 = s.quantile(0.25), s.quantile(0.75)
        iqr = q3 - q1
        lower, upper = q1 - 1.5*iqr, q3 + 1.5*iqr
        flag_col = f"{col}_outlier"
        df[flag_col] = (s < lower) | (s > upper)
        flags[col] = {"lower": lower, "upper": upper, "count": int(df[flag_col].sum()),
                      "rationale": "IQR*1.5 rule, flagged for review not removal"}

    # Logical outliers: negative values where impossible
    df["tenure_negative"] = df["tenure"] < 0
    df["MonthlyCharges_negative"] = df["MonthlyCharges"] < 0
    df["TotalCharges_negative"] = df["TotalCharges"] < 0

    flags["tenure_negative"] = {"count": int(df["tenure_negative"].sum()),
                                "rationale": "Tenure cannot be negative"}
    flags["MonthlyCharges_negative"] = {"count": int(df["MonthlyCharges_negative"].sum()),
                                         "rationale": "Charges cannot be negative"}
    flags["TotalCharges_negative"] = {"count": int(df["TotalCharges_negative"].sum()),
                                       "rationale": "Charges cannot be negative"}

    return df, flags

# ----------------------------------------------------------------------
# STEP 7: LOGICAL CONSISTENCY CHECKS
# ----------------------------------------------------------------------
def logical_checks(df):
    """
    Verify TotalCharges ≈ tenure * MonthlyCharges.
    Add deviation column and flag large discrepancies.
    """
    df = df.copy()
    expected = df["tenure"].astype(float) * df["MonthlyCharges"]
    df["TotalCharges_expected"] = expected
    df["TotalCharges_deviation"] = (df["TotalCharges"] - expected).abs()
    df["TotalCharges_ratio"] = df["TotalCharges"] / expected.replace(0, np.nan)
    # Flag if ratio > 2 or < 0.5 (or deviation > 50% of expected)
    df["TotalCharges_logical_flag"] = (df["TotalCharges_ratio"] > 2) | (df["TotalCharges_ratio"] < 0.5)

    log = {
        "flagged_count": int(df["TotalCharges_logical_flag"].sum()),
        "mean_ratio": float(df["TotalCharges_ratio"].mean()),
        "rationale": "TotalCharges should roughly equal tenure * MonthlyCharges; large deviations indicate data entry errors"
    }
    return df, log

# ----------------------------------------------------------------------
# STEP 8: FINAL CLEANUP
# ----------------------------------------------------------------------
def final_cleanup(df):
    """Drop helper columns, ensure final schema."""
    # Keep outlier flags for auditability, but drop intermediate calc columns
    drop_cols = ["TotalCharges_expected", "TotalCharges_deviation", "TotalCharges_ratio"]
    df = df.drop(columns=[c for c in drop_cols if c in df.columns])

    # Ensure column order
    cols = ["CustomerID", "tenure", "MonthlyCharges", "TotalCharges",
            "Contract", "PaymentMethod", "Dependents", "Partner",
            "SeniorCitizen", "OnlineSecurity", "Churn",
            "tenure_outlier", "MonthlyCharges_outlier", "TotalCharges_outlier",
            "tenure_negative", "MonthlyCharges_negative", "TotalCharges_negative",
            "TotalCharges_logical_flag"]
    df = df[cols]

    return df

# ----------------------------------------------------------------------
# MAIN PIPELINE
# ----------------------------------------------------------------------
def run_pipeline(seed=42):
    """Run full cleaning pipeline and return cleaned df + audit logs."""
    np.random.seed(seed)

    print("Loading raw data...")
    df = load_raw()

    print("Deduplicating...")
    df, dedup_log = deduplicate(df)

    print("Handling missing values...")
    df, missing_log = handle_missing(df)

    print("Correcting types...")
    df = correct_types(df)

    print("Standardizing categoricals...")
    df, cat_log = standardize_categoricals(df)

    print("Flagging outliers...")
    df, outlier_log = flag_outliers(df)

    print("Running logical checks...")
    df, logic_log = logical_checks(df)

    print("Final cleanup...")
    df = final_cleanup(df)

    # Save
    CLEAN_PATH.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(CLEAN_PATH, index=False, encoding="utf-8")

    # Compile audit logs
    audit = {
        "deduplication": dedup_log,
        "missing": missing_log,
        "categorical": cat_log,
        "outliers": outlier_log,
        "logical": logic_log,
        "final_shape": df.shape,
        "final_dtypes": df.dtypes.to_dict()
    }

    print(f"\n=== PIPELINE COMPLETE ===")
    print(f"Final shape: {df.shape}")
    print(f"Saved to: {CLEAN_PATH}")
    return df, audit


if __name__ == "__main__":
    df, audit = run_pipeline()
    import json
    with open("churn_analysis/reports/quality_decision_log.json", "w") as f:
        json.dump(audit, f, indent=2, default=str)
    print("Audit log saved.")