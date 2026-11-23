"""
Core analysis logic for the churn data-quality pipeline.
Used to validate the logic before embedding into the notebook.
"""
import pandas as pd
import numpy as np

RAW_PATH = "churn_analysis/data/originals/customer_churn_raw.csv"

def load_raw(path=RAW_PATH):
    return pd.read_csv(path, dtype=str)

def profile(df):
    print("=== SHAPE ===")
    print(df.shape)
    print("\n=== DTYPES ===")
    print(df.dtypes)
    print("\n=== HEAD ===")
    print(df.head())
    print("\n=== MEMORY USAGE ===")
    print(df.memory_usage(deep=True).sum() / 1024**2, "MB")
    print("\n=== MISSING VALUES ===")
    missing = df.isna().sum()
    pct = (missing / len(df)) * 100
    print(pd.DataFrame({"missing": missing, "pct": pct.round(2)}))
    print("\n=== SUMMARY STATS ===")
    print(df.describe(include="all").T)

def audit_duplicates(df):
    exact = df.duplicated().sum()
    id_dups = df.duplicated(subset=["CustomerID"], keep=False).sum() - exact
    print(f"Exact duplicates: {exact}")
    print(f"CustomerID duplicates (non-exact): {id_dups}")

def audit_missing(df):
    for col in df.columns:
        miss = df[col].isna().sum()
        blank = df[col].astype(str).str.strip().eq("").sum()
        print(f"{col}: NaN={miss}, blank/whitespace={blank}")

def audit_types(df):
    for col in ["tenure", "MonthlyCharges", "TotalCharges"]:
        non_numeric = pd.to_numeric(df[col], errors="coerce").isna() & df[col].notna()
        print(f"{col}: non-numeric values = {non_numeric.sum()}")

def audit_outliers(df):
    for col in ["tenure", "MonthlyCharges"]:
        s = pd.to_numeric(df[col], errors="coerce")
        q1, q3 = s.quantile(0.25), s.quantile(0.75)
        iqr = q3 - q1
        lower, upper = q1 - 1.5*iqr, q3 + 1.5*iqr
        n_out = ((s < lower) | (s > upper)).sum()
        print(f"{col}: IQR=({q1:.2f},{q3:.2f}), bounds=({lower:.2f},{upper:.2f}), outliers={n_out}")

def audit_categoricals(df):
    for col in ["Contract", "PaymentMethod", "Churn", "Dependents", "Partner", "OnlineSecurity"]:
        vals = df[col].astype(str).str.strip().str.lower()
        n_norm = vals.nunique()
        print(f"{col}: {n_norm} distinct normalized values")

def audit_logical(df):
    df = df.copy()
    df["tenure_n"] = pd.to_numeric(df["tenure"], errors="coerce")
    df["mc_n"] = pd.to_numeric(df["MonthlyCharges"], errors="coerce")
    df["tc_n"] = pd.to_numeric(df["TotalCharges"], errors="coerce")
    expected = df["tenure_n"] * df["mc_n"]
    ratio = df["tc_n"] / expected.replace(0, np.nan)
    print("TotalCharges / (tenure*MonthlyCharges) distribution:")
    print(ratio.describe())
    print("Rows where ratio > 2 or < 0.5:", ((ratio > 2) | (ratio < 0.5)).sum())
    print("Negative charges:", (df["mc_n"] < 0).sum(), (df["tc_n"] < 0).sum())
    print("Negative tenure:", (df["tenure_n"] < 0).sum())

if __name__ == "__main__":
    df = load_raw()
    profile(df)
    print("\n=== DUPLICATES ===")
    audit_duplicates(df)
    print("\n=== MISSING ===")
    audit_missing(df)
    print("\n=== TYPES ===")
    audit_types(df)
    print("\n=== OUTLIERS ===")
    audit_outliers(df)
    print("\n=== CATEGORICALS ===")
    audit_categoricals(df)
    print("\n=== LOGICAL ===")
    audit_logical(df)