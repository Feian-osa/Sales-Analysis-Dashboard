import streamlit as st 
import pandas as pd # type: ignore
import plotly.express as px # type: ignore
import json


# -------------------------
# Load Linear Regression metrics
# -------------------------
with open('metrics.json') as f:
    metrics = json.load(f)

r2_train = metrics['r2_train']
r2_test = metrics['r2_test']
mae_value = metrics['Mean_Absolute_Error(MAE)']
mse_value = metrics['Mean_Squared_Error(MSE)']
rmse_value = metrics['Root_Mean_Squared_Error(RMSE)']
overfit = metrics['overfit']

# -------------------------
# Load graph data from Excel
# -------------------------
excel_file = 'sales_dashboard_dataexel.xlsx'  
sales_by_year = pd.read_excel(excel_file, sheet_name='Sales_by_Year')
sales_by_month = pd.read_excel(excel_file, sheet_name='Sales_by_Month')
sales_by_sub_category = pd.read_excel(excel_file, sheet_name='Sales_by_Sub_Category')
sales_by_region = pd.read_excel(excel_file, sheet_name='Sales_by_Region')
top_products = pd.read_excel(excel_file, sheet_name='Top_Products')
top10_subcats=pd.read_excel(excel_file, sheet_name='Top_Sub_Products')
least10_subcats=pd.read_excel(excel_file, sheet_name='Bottom_Sub_Products')
kpi_data = pd.read_excel(excel_file, sheet_name='KPI_DATA')
# -------------------------
# Dashboard Header
# -------------------------
st.title("Sales Dashboard & Linear Regression Metrics")

st.subheader("Linear Regression Model Metrics")
st.write(f"Train R²: {r2_train:.4f}")
st.write(f"Test R²: {r2_test:.4f}")
st.write(f"Mean_Absolute_Error(MAE): ${mae_value:.2f}")
st.write(f"Mean_Squared_Error(MSE): ${mse_value:.2f}")
st.write(f"Root_Mean_Squared_Error(RMSE): ${rmse_value:.2f}")
st.write(overfit)

st.subheader("Key Performance Indicators")
st.table(kpi_data)

# -------------------------
# Sidebar: Select graph
# -------------------------
graph_option = st.sidebar.selectbox(
    "Select Graph",
    ["Total Sales by Year", "Sales by Month", "Sales by Sub-Category", 
     "Sales by Region", "All Products", "Top 10 Sub-Categories", "Bottom 10 Sub-Categories"]
)

# sales_by_month should have columns: Month (1-12), Sales
# Map numbers to month names
month_map = {1:'January', 2:'February', 3:'March', 4:'April', 5:'May', 6:'June',
             7:'July', 8:'August', 9:'September', 10:'October', 11:'November', 12:'December'}
sales_by_month['Month Name'] = sales_by_month['Month'].map(month_map)

# -------------------------
# Display selected graph
# -------------------------
if graph_option == "Total Sales by Year":
    fig = px.bar(sales_by_year, x='Year', y='Sales', title="Total Sales by Year", text='Sales')
    fig.update_yaxes(tickformat=",")
elif graph_option == "Sales by Month":
    fig = px.line(sales_by_month, x='Month Name', y='Sales', title="Sales by Month", markers=True, text='Sales')
    fig.update_yaxes(tickformat=",")
elif graph_option == "Sales by Sub-Category":
    fig = px.bar(sales_by_sub_category, x='Sub Category', y='Sales', title="Sales by Sub-Category", text='Sales')
    fig.update_yaxes(tickformat=",")
 
elif graph_option == "Sales by Region":
    fig = px.bar(sales_by_region, x='Region', y='Sales', title="Sales by Region", text='Sales')
    fig.update_yaxes(tickformat=",")
elif graph_option == "All Products":
    fig = px.bar(top_products, x='Category', y='Sales', title="All Products by Sales", text='Sales')
    fig.update_yaxes(tickformat=",")
# Top 10 Sub-Categories
elif graph_option == "Top 10 Sub-Categories":
    top10_subcats_plot = top10_subcats.sort_values(by='Sales', ascending=True).head(10)  # take only top 10 rows
    fig = px.bar(top10_subcats_plot,
                 x='Sales',
                 y='Sub Category',
                 orientation='h',
                 title="Top 10 Sub-Categories by Sales",
                 text='Sales')

    fig.update_xaxes(tickformat=",")

# Bottom 10 Sub-Categories
else:  # Bottom 10 Sub-Categories
    least10_subcats_plot = least10_subcats.sort_values(by='Sales', ascending=False).head(10)  # take only bottom 10 rows
    fig = px.bar(least10_subcats_plot,
                 x='Sales',
                 y='Sub Category',
                 orientation='h',
                 title="Bottom 10 Sub-Categories by Sales",
                 text='Sales')

    fig.update_xaxes(tickformat=",")

st.plotly_chart(fig)




##open terminal and run the following command to start the Streamlit app:
# pip install streamlit 
# pip install plotly
#venv\Scripts\activate (create venv and activate it if you haven't already)
# streamlit run "app.py"(the terminal should be in the same directory as app.py)
#install streamlit and plotly if you haven't already:
