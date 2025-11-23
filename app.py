import pandas as pd
import numpy as np
import streamlit as st
import matplotlib.pyplot as plt

# Load data
@st.cache_data
def load_data():
    dfm = pd.read_csv("dfm.csv", parse_dates=["year_month"])
    future_forecast = pd.read_csv("future_forecast.csv", parse_dates=["year_month"])
    inventory_plan = pd.read_csv("inventory_plan.csv", parse_dates=False)
    inventory_risk = pd.read_csv("inventory_risk.csv", parse_dates=False)

    # If stockout_month / reorder_month were saved as strings, convert to datetime where possible
    for col in ["stockout_month", "reorder_month"]:
        if col in inventory_plan.columns:
            inventory_plan[col] = pd.to_datetime(inventory_plan[col], errors="coerce")
    for col in ["stockout_month", "reorder_month"]:
        if col in inventory_risk.columns:
            inventory_risk[col] = pd.to_datetime(inventory_risk[col], errors="coerce")

    return dfm, future_forecast, inventory_plan, inventory_risk

dfm, future_forecast, inventory_plan, inventory_risk = load_data()

st.set_page_config(
    page_title="Sales and Inventory Forecasting System",
    layout="wide"
)

st.title("Sales and Inventory Forecasting System")


# Sidebar navigation
page = st.sidebar.selectbox(
    "Navigation",
    [
        "Product Dashboard",
        "Inventory Risk Overview",
        "Data Explorer"
    ]
)


# Helper to compute inventory depletion for a product
def compute_inventory_depletion(product_id):
    hist_info = dfm[dfm["product_id"] == product_id].iloc[0]
    current_stock = hist_info["current_stock"]

    prod_future = future_forecast[future_forecast["product_id"] == product_id].copy()
    prod_future = prod_future.sort_values("year_month")

    stock = current_stock
    inventory_levels = []
    for qty in prod_future["monthly_qty"]:
        stock -= qty
        inventory_levels.append(stock)

    return prod_future["year_month"], inventory_levels, current_stock


# Page 1: Product Dashboard
if page == "Product Dashboard":
    st.subheader("Product-Level Demand and Inventory View")

    product_ids = sorted(dfm["product_id"].unique().tolist())
    selected_pid = st.sidebar.selectbox("Select Product ID", product_ids)

    col1, col2 = st.columns(2)

    # Historical vs Forecasted demand
    with col1:
        st.markdown("**Historical vs Forecasted Monthly Demand**")

        hist = dfm[dfm["product_id"] == selected_pid].copy()
        fut = future_forecast[future_forecast["product_id"] == selected_pid].copy()

        hist = hist.sort_values("year_month")
        fut = fut.sort_values("year_month")

        fig, ax = plt.subplots(figsize=(8, 4))
        ax.plot(hist["year_month"], hist["monthly_qty"], marker="o", label="Historical")
        ax.plot(fut["year_month"], fut["monthly_qty"], marker="o", linestyle="--", label="Forecast")

        ax.set_xlabel("Month")
        ax.set_ylabel("Quantity")
        ax.set_title(f"Product {selected_pid} — Historical vs Forecasted Demand")
        ax.legend()
        ax.grid(True)
        st.pyplot(fig)

    # Inventory depletion
    with col2:
        st.markdown("**Projected Inventory Depletion**")

        dates, inventory_levels, start_stock = compute_inventory_depletion(selected_pid)
        reorder_level = dfm[dfm["product_id"] == selected_pid]["reorder_level"].iloc[0]

        fig2, ax2 = plt.subplots(figsize=(8, 4))
        ax2.plot(dates, inventory_levels, marker="o", label="Projected Inventory")
        ax2.axhline(y=reorder_level, linestyle="--", label="Reorder Level")

        ax2.set_xlabel("Month")
        ax2.set_ylabel("Inventory Level")
        ax2.set_title(f"Product {selected_pid} — Inventory Projection")
        ax2.legend()
        ax2.grid(True)
        st.pyplot(fig2)

    st.markdown("---")

    # Stockout and reorder information
    st.markdown("**Stockout and Reorder Summary**")

    prod_inv = inventory_plan[inventory_plan["product_id"] == selected_pid]
    prod_risk = inventory_risk[inventory_risk["product_id"] == selected_pid]

    if not prod_inv.empty:
        row = prod_inv.iloc[0]
        col_a, col_b, col_c, col_d = st.columns(4)

        col_a.metric("Current Stock", f"{row['current_stock']:.0f}")
        col_b.metric("Stockout Month", str(row["stockout_month"]) if pd.notna(row["stockout_month"]) else "None")
        col_c.metric("Reorder Month", str(row["reorder_month"]) if pd.notna(row["reorder_month"]) else "None")
        col_d.metric("Recommended Reorder Qty", f"{row['recommended_reorder_qty']:.0f}")

    if not prod_risk.empty:
        st.markdown("**Risk Classification**")
        st.write(prod_risk[["product_id", "risk_level"]])


# Page 2: Inventory Risk Overview
elif page == "Inventory Risk Overview":
    st.subheader("Inventory Risk Overview")

    # Risk distribution bar chart
    risk_counts = inventory_risk["risk_level"].value_counts()

    fig, ax = plt.subplots(figsize=(8, 4))
    ax.bar(risk_counts.index, risk_counts.values)
    ax.set_xlabel("Risk Level")
    ax.set_ylabel("Number of Products")
    ax.set_title("Inventory Risk Distribution")
    ax.grid(axis="y")
    plt.xticks(rotation=20)
    st.pyplot(fig)

    st.markdown("---")

    # Filter by risk level
    risk_choice = st.selectbox(
        "Filter products by risk level",
        options=["All"] + risk_counts.index.tolist()
    )

    if risk_choice == "All":
        filtered = inventory_risk.copy()
    else:
        filtered = inventory_risk[inventory_risk["risk_level"] == risk_choice]

    st.write("Products in selected risk category:")
    st.dataframe(filtered)


# Page 3: Data Explorer
elif page == "Data Explorer":
    st.subheader("Data Explorer")

    tab1, tab2, tab3, tab4 = st.tabs(
        ["Historical Modeling Data", "Future Forecasts", "Inventory Plan", "Inventory Risk"]
    )

    with tab1:
        st.markdown("**Historical Modeling Data (dfm)**")
        st.dataframe(dfm.head(200))

    with tab2:
        st.markdown("**Future Forecasts**")
        st.dataframe(future_forecast.head(200))

    with tab3:
        st.markdown("**Inventory Plan**")
        st.dataframe(inventory_plan.head(200))

    with tab4:
        st.markdown("**Inventory Risk**")
        st.dataframe(inventory_risk.head(200))
