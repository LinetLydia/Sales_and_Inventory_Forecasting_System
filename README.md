# 📊 Sales and Inventory Forecasting System  
A comprehensive end-to-end machine learning system for forecasting sales, predicting inventory depletion, and identifying stockout risks across 300 products.  
Built with **Python, XGBoost, Streamlit, and a multi-table data architecture**.

---

## 📘 Overview

This project simulates a real-world retail forecasting pipeline designed to help businesses:

- Predict future product demand  
- Forecast inventory levels month-by-month  
- Detect stockout risks before they happen  
- Generate reorder quantities  
- Classify products by inventory risk  
- Provide an interactive dashboard for operational decision-making  

The system is built from scratch using **synthetic but realistic transactional and operational datasets**, mimicking the structure of real retail data (Products, Sales, Inventory, Suppliers).

---

## 🧱 System Architecture

The project follows a **full data science lifecycle**:

### 1. **Data Generation & Preparation**
- 300 products with metadata (category, cost, price, supplier, reorder levels, etc.)
- 18 months of random daily sales transactions
- Supplier-level lead time + reliability scores
- Inventory table with stock levels, safety stock, and logistics attributes

### 2. **Feature Engineering**
Created over 20+ features, including:
- Lag features (1, 2, 3 months)
- Rolling windows (3 & 6 months)
- Seasonality encodings (month, quarter)
- Trend variables
- Promo flags, average discounts
- Supplier performance features

### 3. **Machine Learning**
Model: **XGBoost Regressor**

Predictions:
- Monthly forecast for each product (12 months ahead)
- Forecasted demand becomes input to the inventory simulation

Metrics achieved:
- **MAE:** 0.44  
- **RMSE:** 0.92  
- **MAPE:** 16.85%  

### 4. **Inventory Simulation**
Simulates inventory month-by-month based on forecast:
- Starting stock  
- Forecasted monthly consumption  
- Reorder triggers  
- Lead-time coverage  
- Safety stock buffer  

Outputs:
- Stockout month  
- Reorder month  
- Recommended reorder quantity  

### 5. **Risk Classification**
Each product classified into risk tiers:

| Risk Level | Meaning |
|------------|---------|
| CRITICAL RISK | Stockout already expected or extremely soon |
| HIGH RISK | Inventory will fall below safety threshold |
| MEDIUM RISK | Some risk but within manageable range |
| LOW RISK / HEALTHY | No stockout risk in forecast horizon |

### 6. **Interactive Streamlit Dashboard**
Deployed dashboard includes:

#### **Executive Summary**
- Total products  
- Forecast horizon  
- High/medium/low risk counts  
- Stockout risks  
- Risk distribution chart  
- Top at-risk products  

#### **Product Dashboard**
- Historical vs forecasted demand  
- Inventory projection curve  
- Stockout month  
- Reorder month  
- Recommended reorder quantity  
- Risk classification  

#### **Risk Overview**
- Bar chart of risk categories  
- Filter by risk level  
- View product-level risk details  

#### **Data Explorer**
- View raw modeling table  
- View forecast dataset  
- View inventory plan  
- View risk dataset  

---

## 🚀 Live Demo (Streamlit App)

👉 **Launch App:**  
https://linetlydia-sales-and-inventory-forecasting-system-app-y0kvmm.streamlit.app/

---

## 🗂 Project Structure

Sales_and_Inventory_Forecasting_System/
│── app.py # Streamlit app
│── dfm.csv # Model-ready dataset
│── future_forecast.csv # 12-month forecasted demand
│── inventory_plan.csv # Inventory simulation outputs
│── inventory_risk.csv # Risk classification outputs
│── requirements.txt
│── README.md


---

## 📦 Installation & Running Locally

### 1. Clone the repository
```bash
git clone https://github.com/LinetLydia/Sales_and_Inventory_Forecasting_System/tree/main
cd Sales_and_Inventory_Forecasting_System
```

### 2. Install dependencies
pip install -r requirements.txt

### 3. Run the Streamlit app
streamlit run app.py

## 🧠 **Key Insights from the Model**

- Out of **300 products**, **47 are classified as High-Risk** and require urgent inventory action.
- Only **4 products have an expected stockout** within the next 12 months.
- A large majority (**249 products**) fall into the **Low-Risk / Healthy** category.
- Forecast accuracy metrics show **strong, stable performance** for synthetic demand data.

---

## 🛠 **Technologies Used**

- **Python**
- **Pandas**, **NumPy**
- **XGBoost**
- **Matplotlib**
- **Streamlit**
- **Datetime & Feature Engineering**

---

## 📈 **Future Enhancements**

Planned upgrades include:

- **Revenue & profit forecasting**
- **ABC product classification**
- **Multi-location inventory forecasting**
- **Deep learning demand forecasting (LSTM / Prophet)**
- **Automated monthly reporting (PDF/Excel)**
- **User authentication for restricted dashboards**

---

## 👤 **Author**

**Linet Lydia Kagundu**  
*Data Analyst | Machine Learning | Analytics Engineering*  
📍 Nairobi, Kenya  
🔗 *Portfolio Website (Coming Soon)*  
