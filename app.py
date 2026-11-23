import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# --- Page Config ---
st.set_page_config(page_title="Business KPI Dashboard", layout="wide")

# --- Load Data ---
@st.cache_data
def load_data():
    df = pd.read_csv('data/churn_clean.csv')
    return df

df = load_data()

# --- Sidebar Filters ---
st.sidebar.header("Interactive Filters")

contract_options = st.sidebar.multiselect(
    "Contract Type",
    options=df['Contract'].unique(),
    default=df['Contract'].unique()
)

tenure_min, tenure_max = int(df['tenure'].min()), int(df['tenure'].max())
tenure_range = st.sidebar.slider(
    "Tenure Range",
    min_value=tenure_min,
    max_value=tenure_max,
    value=(tenure_min, tenure_max)
)

monthly_min, monthly_max = float(df['MonthlyCharges'].min()), float(df['MonthlyCharges'].max())
monthly_range = st.sidebar.slider(
    "Monthly Charges Range",
    min_value=monthly_min,
    max_value=monthly_max,
    value=(monthly_min, monthly_max)
)

# --- Apply Filters ---
filtered_df = df[
    (df['Contract'].isin(contract_options)) &
    (df['tenure'].between(tenure_range[0], tenure_range[1])) &
    (df['MonthlyCharges'].between(monthly_range[0], monthly_range[1]))
]

# --- Main Dashboard ---
st.title("📊 Business KPI Dashboard")
st.markdown("---")

# --- KPI Metrics ---
churn_rate = (filtered_df['Churn'] == 'Yes').mean() * 100
retention_rate = 100 - churn_rate
revenue_at_risk = filtered_df[filtered_df['Churn'] == 'Yes']['TotalCharges'].sum()
avg_clv = filtered_df['TotalCharges'].mean()

col1, col2, col3, col4 = st.columns(4)
col1.metric("Overall Churn Rate", f"{churn_rate:.2f}%")
col2.metric("Retention Rate", f"{retention_rate:.2f}%")
col3.metric("Revenue at Risk", f"${revenue_at_risk:,.2f}")
col4.metric("Avg. Customer LTV", f"${avg_clv:,.2f}")

st.markdown("---")

# --- Visualizations ---
row1_col1, row1_col2 = st.columns(2)

with row1_col1:
    st.subheader("Churn Rate by Contract Type")
    churn_by_contract = filtered_df.groupby('Contract')['Churn'].value_counts(normalize=True).unstack().fillna(0) * 100
    fig1 = px.bar(churn_by_contract, x=churn_by_contract.index, y='Yes', title="Percentage of Customers Churning by Contract", labels={'Yes': 'Churn Rate (%)'})
    st.plotly_chart(fig1, use_container_width=True)

with row1_col2:
    st.subheader("Churn vs Tenure Distribution")
    fig2 = px.histogram(filtered_df, x='tenure', color='Churn', nbins=50, title="Customer Churn by Tenure")
    st.plotly_chart(fig2, use_container_width=True)

row2_col1, row2_col2 = st.columns(2)

with row2_col1:
    st.subheader("Revenue at Risk by Contract")
    rev_at_risk = filtered_df[filtered_df['Churn'] == 'Yes'].groupby('Contract')['TotalCharges'].sum().reset_index()
    fig3 = px.bar(rev_at_risk, x='Contract', y='TotalCharges', title="Revenue at Risk by Contract Type", labels={'TotalCharges': 'Sum of Total Charges ($)'})
    st.plotly_chart(fig3, use_container_width=True)

with row2_col2:
    st.subheader("Customer Segmentation")
    fig4 = px.scatter(filtered_df, x='tenure', y='MonthlyCharges', color='Churn', title="Spending vs Tenure by Churn Status", opacity=0.7)
    st.plotly_chart(fig4, use_container_width=True)

# --- Business Insights ---
st.markdown("## 💡 Business Insights")
st.write(f"""
- **Churn Dynamics**: Currently, the churn rate is {churn_rate:.2f}%. This suggests that for every 100 customers, {churn_rate:.2f} are expected to churn under the current filters.
- **Retention**: {retention_rate:.2f}% of customers are being retained. High-churn segments often correlate with specific contract types (e.g., month-to-month).
- **Revenue at Risk**: We have identified ${revenue_at_risk:,.2f} in Total Charges potentially lost to churned customers. Prioritize retention efforts for high-value customers with upcoming contract renewals.
- **Segmentation**: The scatter plot reveals patterns between monthly spend and tenure. Younger customers (low tenure) with high monthly charges might be at higher risk of churning early.
""")
