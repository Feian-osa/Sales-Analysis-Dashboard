import streamlit as st 
import pandas as pd # type: ignore
import plotly.express as px # type: ignore


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
st.title("Sales Dashboard")
st.subheader("Performance Insights")
st.table(kpi_data)




# sales_by_month should have columns: Month (1-12), Sales
# Map numbers to month names
month_map = {1:'January', 2:'February', 3:'March', 4:'April', 5:'May', 6:'June',
             7:'July', 8:'August', 9:'September', 10:'October', 11:'November', 12:'December'}
sales_by_month['Month Name'] = sales_by_month['Month'].map(month_map)

# -------------------------
# Display selected graph
# -------------------------

# Create tabs for different graph options (alternative approach)
tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs(["Total Sales by Year", "Sales by Month", "Sales by Sub-Category", 
     "Sales by Region", "All Products", "Top 10 Sub-Categories", "Bottom 10 Sub-Categories"])

with tab1:
    st.subheader("Total Orders by Year")
    fig = px.bar(sales_by_year, x='Year', y='Sales', title="Total Sales by Year", text='Sales')
    fig.update_yaxes(tickformat=",")
    st.plotly_chart(fig, key="total_sales_by_year")

with tab2:
    st.subheader("Sales by Month")
    fig = px.line(sales_by_month, x='Month Name', y='Sales', title="Sales by Month", markers=True, text='Sales')
    fig.update_yaxes(tickformat=",")
    st.plotly_chart(fig, key="sales_by_month")

with tab3:
    st.subheader("Sales by Sub-Category")
    fig = px.bar(sales_by_sub_category, x='Sub Category', y='Sales', title="Sales by Sub-Category", text='Sales')
    fig.update_yaxes(tickformat=",")
    st.plotly_chart(fig, key="sales_by_sub_category")

with tab4:
    st.subheader("Sales by Region")
    fig = px.bar(sales_by_region, x='Region', y='Sales', title="Sales by Region", text='Sales')
    fig.update_yaxes(tickformat=",")
    st.plotly_chart(fig, key="sales_by_region")

with tab5:
    st.subheader("All Products by Sales")
    fig = px.bar(top_products, x='Category', y='Sales', title="All Products by Sales", text='Sales')
    fig.update_yaxes(tickformat=",")
    st.plotly_chart(fig, key="all_products_by_sales")

with tab6:
    st.subheader("Top 10 Sub-Categories by Sales")
    top10_subcats_plot = top10_subcats.sort_values(by='Sales', ascending=True).head(10)  # take only top 10 rows
    fig = px.bar(top10_subcats_plot,
                 x='Sales',
                 y='Sub Category',
                 orientation='h',
                 title="Top 10 Sub-Categories by Sales",
                 text='Sales')

    fig.update_xaxes(tickformat=",")
    st.plotly_chart(fig, key="top10_subcats")

with tab7:
    st.subheader("Bottom 10 Sub-Categories by Sales")
    least10_subcats_plot = least10_subcats.sort_values(by='Sales', ascending=False).head(10)  # take only bottom 10 rows
    fig = px.bar(least10_subcats_plot,
                 x='Sales',
                 y='Sub Category',
                 orientation='h',
                 title="Bottom 10 Sub-Categories by Sales",
                 text='Sales')

    fig.update_xaxes(tickformat=",")
    st.plotly_chart(fig, key="least10_subcats")












