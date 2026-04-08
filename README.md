# 🎓 Sales Dashboard with Profit Prediction
## 📌 Overview

This project is an interactive Sales Dashboard built using Streamlit.
It provides insights into sales performance across different categories, regions, and time periods, and includes a profit prediction system using a machine learning model.

It includes:

Data preprocessing & visualization,

KPI calculations,

Interactive charts using Plotly,

Machine learning model for profit prediction


## 🎯 Objectives

Visualize sales data for actionable insights,

Track KPIs like Total Sales, Orders, Profit, and Average Order Value,

Analyze trends by year, month, sub-category, and region,

Predict profit based on sales, discount, category, and region.



## 📊 Dataset

The Excel dataset sales_dashboard_dataexel.xlsx contains multiple sheets:

Sales_by_Year – Total sales per year,

Sales_by_Month – Monthly sales data,

Sales_by_Sub_Category – Sales per sub-category,

Sales_by_Region – Sales per region,

Top_Products – Product-level sales,

Top_Sub_Products – Top 10 sub-categories,

Bottom_Sub_Products – Bottom 10 sub-categories,

KPI_DATA – Key performance indicators.


## 🛠️ Technologies Used
Python,
Pandas,
NumPy,
Plotly,
Scikit-learn,
Streamlit


## 🔍 Project Workflow

### 1. Data Preprocessing
   
  Loading Excel sheets into Pandas DataFrames
  Mapping numeric months to month names
  Cleaning KPI columns

  
### 2. KPI Calculation
   
  Total Sales,
  
  Total Orders,
  
  Total Profit,
  
  Average Order Value.
  
Displayed at the top of the dashboard for quick insights.

### 3. Exploratory Data Analysis (EDA)
   
Interactive charts made using Plotly for these:
   
Total Sales by Year,
Sales by Month,
Sales by Sub-Category,
Sales by Region,
Top & Bottom Sub-Categories,
Tables and metrics for deeper insights.

### 4. Machine Learning Model

Model is trained using following features:

Sales,
Discount,
Profit Margin,
Category (encoded), and
Region (encoded)

### Label Encoders:

le_category.pkl – for Product Category

le_region.pkl – for Region

### Prediction Input - Following features are used in prediction:


Sales, 
Discount,	
Profit Margin,
Category and	
Region	


### 5. Streamlit Dashboard
   

## 📊 Dashboard Tabs
Total Sales by Year – Bar chart of yearly sales,

Sales by Month – Line chart of monthly sales,

Sales by Sub-Category – Bar chart,

Sales by Region – Bar chart,

All Products – Product-wise sales,

Top 10 Sub-Categories – Horizontal bar chart,

Bottom 10 Sub-Categories – Horizontal bar chart, and

Prediction – Profit prediction form



## 🤖 Prediction Tab
Users input :  Sales, Discount, Category, Region, and Profit Margin

Model predicts expected profit


## How to Run the Project

### 1. Clone Repository

  git clone https://github.com/Feian-osa/Sales-Analysis-Dashboard.git
  
  cd Sales-Analysis-Dashboard

### 2. Create Virtual Environment
python -m venv venv

### Windows
venv\Scripts\activate

### 3. Install Dependencies
pip install -r requirements.txt

### 4. Run Streamlit App
streamlit run app.py




## 📁 Project Structure

sales-dashboard/


├── app.py                              # Main Streamlit app

├── model.pkl                           # Trained profit prediction model

├── le_category.pkl                     # Label encoder for Category

├── le_region.pkl                       # Label encoder for Region

├── sales_dashboard_dataexel.xlsx       # Excel file with sales data

├── requirements.txt                    # Python dependencies

└── README.md                           # Project documentation
