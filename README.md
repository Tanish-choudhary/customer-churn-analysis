# Business KPI Dashboard

This dashboard provides a comprehensive overview of customer churn metrics for analysis and decision-making.

## Features
- **KPI Metrics**: Real-time display of Overall Churn Rate, Retention Rate, Revenue at Risk, and Average Customer Lifetime Value.
- **Interactive Filtering**: Filter data dynamically by Contract Type, Tenure range, and Monthly Charges.
- **Visualizations**: 
  - Churn Rate by Contract Type
  - Churn Distribution by Tenure
  - Revenue at Risk per Contract
  - Customer Segmentation Analysis (Spending vs Tenure)
- **Automatic Insights**: Insights section summarizing the state of retention and risk based on the filtered data.

## How to Run
1. Ensure you have installed the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Run the Streamlit application:
   ```bash
   streamlit run app.py
   ```
3. Open the URL provided in your terminal in your web browser.

## Metrics Explanation
- **Churn Rate**: The percentage of customers who have churned.
- **Retention Rate**: The percentage of customers who have stayed.
- **Revenue at Risk**: Total sum of lifetime value charges for customers identified as "Churned".
- **Average Customer Lifetime Value**: Mean of the Total Charges across the current filtered dataset.
