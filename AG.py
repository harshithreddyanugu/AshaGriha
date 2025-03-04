import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns


# 📂 Load CSV Data
file_path = "business_expense_income_tracker.csv"
df = pd.read_csv(file_path)

# ✅ Debug: Print actual column names to check for issues
st.write("🔍 Debug: Column Names ->", df.columns.tolist())

# ✅ Standardize column names (strip spaces, fix encoding issues)
df.columns = df.columns.str.strip()
df.rename(columns={"Amount (₹)": "Amount"}, inplace=True)  # Fix incorrect encoding

# ✅ Verify if required columns exist
required_columns = {"Date", "Category", "Amount", "Type", "Description"}
missing_columns = required_columns - set(df.columns)
if missing_columns:
    st.error(f"⚠️ Missing columns in the uploaded CSV: {missing_columns}")
    st.stop()

# ✅ Convert "Date" to datetime format
df["Date"] = pd.to_datetime(df["Date"], errors='coerce')

# ✅ Ensure "Type" column exists and clean its values
df["Type"] = df["Type"].astype(str).str.strip()

# 🎯 App Title
st.title("📊 Business Expense & Income Tracker 💰")
st.write("🚀 **Track your income, expenses, and financial health with insightful visualizations!**")

# 📌 Sidebar - Filters
st.sidebar.header("🔍 Filter Your Transactions")
category_filter = st.sidebar.multiselect("📂 Select Categories:", df["Category"].unique())
type_filter = st.sidebar.radio("🔄 Select Transaction Type:", ["All", "Income", "Expense"], index=0)
date_range = st.sidebar.date_input("📅 Select Date Range:", [df["Date"].min(), df["Date"].max()])

# 🏦 Apply Filters
filtered_df = df.copy()
if category_filter:
    filtered_df = filtered_df[filtered_df["Category"].isin(category_filter)]
if type_filter != "All":
    filtered_df = filtered_df[filtered_df["Type"] == type_filter]
filtered_df = filtered_df[(filtered_df["Date"] >= pd.to_datetime(date_range[0])) & 
                          (filtered_df["Date"] <= pd.to_datetime(date_range[1]))]

# 📜 Display Transaction Table
st.subheader("📄 Transaction History 📑")
st.dataframe(filtered_df, use_container_width=True)

# 📊 Financial Overview
st.subheader("💰 Financial Summary")
income_total = filtered_df[filtered_df["Type"] == "Income"]["Amount"].sum()
expense_total = filtered_df[filtered_df["Type"] == "Expense"]["Amount"].sum()
profit = income_total - expense_total

col1, col2, col3 = st.columns(3)
col1.metric("💵 Total Income", f"₹{income_total:,.2f}")
col2.metric("💸 Total Expenses", f"₹{expense_total:,.2f}")
col3.metric("📈 Net Profit", f"₹{profit:,.2f}", delta=float(profit), delta_color="normal")

# 📉 Income vs Expenses Over Time
st.subheader("📈 Income & Expense Trend Over Time")
fig, ax = plt.subplots(figsize=(10, 5))
sns.lineplot(data=filtered_df, x="Date", y="Amount", hue="Type", marker="o", ax=ax)
plt.xticks(rotation=45)
plt.title("Income vs. Expenses Over Time")
st.pyplot(fig)

# 🍰 Expense Breakdown Chart
st.subheader("📊 Expense Distribution by Category")
expense_data = filtered_df[filtered_df["Type"] == "Expense"].groupby("Category")["Amount"].sum()
if not expense_data.empty:
    fig, ax = plt.subplots()
    expense_data.plot(kind="pie", autopct="%1.1f%%", colors=["red", "blue", "green", "yellow"], ax=ax)
    ax.set_ylabel("")
    st.pyplot(fig)
else:
    st.info("ℹ️ No expenses recorded for the selected filters.")

# 📊 Additional Income & Expense Graphs
st.subheader("📊 Additional Visualizations")

# 1. Bar Chart: Income & Expenses by Category
st.subheader("📊 Income & Expenses by Category")
fig, ax = plt.subplots(figsize=(10, 5))
sns.barplot(data=filtered_df, x="Category", y="Amount", hue="Type", ax=ax)
plt.xticks(rotation=45)
st.pyplot(fig)

# 2. Monthly Trend Analysis
st.subheader("📅 Monthly Trend Analysis")
filtered_df["Month"] = filtered_df["Date"].dt.strftime('%Y-%m')
monthly_trends = filtered_df.groupby(["Month", "Type"])["Amount"].sum().unstack()
fig, ax = plt.subplots(figsize=(10, 5))
monthly_trends.plot(kind="line", marker="o", ax=ax)
plt.xticks(rotation=45)
st.pyplot(fig)

# 3. Boxplot for Income & Expenses
st.subheader("📦 Income & Expense Distribution")
fig, ax = plt.subplots(figsize=(10, 5))
sns.boxplot(data=filtered_df, x="Type", y="Amount", ax=ax)
st.pyplot(fig)

# 📥 Download Button
csv_data = filtered_df.to_csv(index=False).encode('utf-8')
st.download_button("📥 Download Report (CSV)", csv_data, "business_report.csv", "text/csv")

# 💡 Insights & Tips
st.subheader("💡 Business Insights & Recommendations")
st.write("✅ **Monitor High Spending Areas:** Identify categories where you're spending the most.")
st.write("✅ **Analyze Profit Trends:** Track which months have the highest & lowest profits.")
st.write("✅ **Optimize Budgeting:** Compare income and expenses to adjust your business strategy.")
st.write("🚀 **Take control of your business finances and increase profitability!**")











