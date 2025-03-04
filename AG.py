import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
# 🏡 Streamlit Page Configuration
st.set_page_config(page_title="Mortgage Calculator (INR)", page_icon="🏠", layout="centered")

# 🔄 Conversion Rate (1 USD to INR)
USD_TO_INR = 83  # Update as per latest exchange rate

# 🎨 Header
st.markdown("<h1 style='text-align: center; color: darkblue;'>🏡 Mortgage Repayment Calculator (₹)</h1>", unsafe_allow_html=True)
st.write("🔹 This tool helps you estimate **monthly mortgage payments**, visualize your **loan repayment progress**, and understand **how much interest you will pay over time**.")

# 📌 Sidebar - User Inputs
st.sidebar.header("🔧 Adjust Your Loan Details")

loan_amount = st.sidebar.number_input("💰 Home Loan Amount (₹)", min_value=1000, value=250000 * USD_TO_INR, step=50000, format="%.0f")
interest_rate = st.sidebar.slider("📈 Interest Rate (%)", min_value=0.0, max_value=15.0, value=5.0, step=0.1)
loan_term = st.sidebar.slider("📅 Loan Term (Years)", min_value=1, max_value=40, value=30, step=1)
extra_payment = st.sidebar.number_input("💸 Extra Monthly Payment (₹)", min_value=0, value=0, step=5000, format="%.0f")

# 🏦 Function to calculate mortgage payment
def calculate_mortgage(P, annual_rate, years, extra_payment=0):
    r = (annual_rate / 100) / 12  # Monthly interest rate
    n = years * 12  # Total number of payments
    if r > 0:
        M = (P * r * (1 + r) ** n) / ((1 + r) ** n - 1)  # Monthly payment formula
    else:
        M = P / n  # If interest rate is 0
    return M + extra_payment

# 📊 Function to generate amortization schedule
def amortization_schedule(P, annual_rate, years, extra_payment=0):
    r = (annual_rate / 100) / 12  
    n = years * 12  
    balance = P
    schedule = []
    for month in range(1, n + 1):
        interest = balance * r if r > 0 else 0  
        principal = calculate_mortgage(P, annual_rate, years, extra_payment) - interest  
        balance -= principal  

        if balance < 0:
            balance = 0  
            principal += balance  

        schedule.append([month, principal, interest, balance])
        if balance == 0:
            break  

    return pd.DataFrame(schedule, columns=["Month", "Principal", "Interest", "Balance"])

# 🔢 Calculate mortgage details
monthly_payment = calculate_mortgage(loan_amount, interest_rate, loan_term, extra_payment)
schedule = amortization_schedule(loan_amount, interest_rate, loan_term, extra_payment)

# 📌 Loan Summary
st.markdown("## 📌 Loan Summary")
st.write("### 🔹 Key Takeaways:")
st.success(f"💵 **Your Monthly Payment:** ₹{monthly_payment:,.2f} per month")
st.info(f"💰 **Total Amount Paid Over {loan_term} Years:** ₹{schedule[['Principal', 'Interest']].sum().sum():,.2f}")
st.warning(f"📉 **Total Interest Paid:** ₹{schedule['Interest'].sum():,.2f}")

# 💡 Insightful Explanation
st.write("💡 **Understanding Your Mortgage:**")
st.write("- Your **monthly payment** is divided into two parts: **principal (loan amount) and interest**.")
st.write("- Over time, you pay **less interest** and **more principal**, reducing your debt.")
st.write("- Extra payments **reduce the interest paid** and help **pay off the loan faster**.")

# 📅 Amortization Schedule
st.markdown("## 📅 Amortization Schedule (Loan Payment Breakdown)")
st.dataframe(schedule.style.format({"Principal": "₹{:,.2f}", "Interest": "₹{:,.2f}", "Balance": "₹{:,.2f}"}))

# 📊 Loan Balance Over Time
st.markdown("## 📉 Loan Balance Over Time")
fig, ax = plt.subplots(figsize=(8, 4))
ax.plot(schedule["Month"], schedule["Balance"], label="Remaining Loan Balance", color="red", linewidth=2)
ax.set_xlabel("Month")
ax.set_ylabel("Loan Balance (₹)")
ax.grid(True, linestyle="--", alpha=0.6)
ax.legend()
st.pyplot(fig)

# 🍰 Payment Breakdown Pie Chart
st.markdown("## 📊 Where Your Money Goes")
fig, ax = plt.subplots()
ax.pie(
    [schedule["Principal"].sum(), schedule["Interest"].sum()],
    labels=["Principal (Your Loan)", "Interest (Bank's Profit)"],
    autopct="%1.1f%%",
    colors=["green", "orange"],
    wedgeprops={"edgecolor": "black"},
)
st.pyplot(fig)

# 📊 Loan Repayment Progress
progress = 1 - (schedule["Balance"].iloc[-1] / loan_amount)
st.markdown("## 📊 Loan Repayment Progress")
st.progress(progress)

# 📢 Mortgage FAQs
st.markdown("## 🤔 Frequently Asked Questions")

with st.expander("📌 What is a mortgage?"):
    st.write("A mortgage is a loan used to purchase a home. You borrow money from a bank and repay it over time with interest.")

with st.expander("📌 How does interest affect my payments?"):
    st.write("Interest is what the bank charges you for borrowing money. A higher interest rate means higher monthly payments.")

with st.expander("📌 Can I save money by making extra payments?"):
    st.write("Yes! Extra payments reduce the loan balance faster, lowering interest costs and shortening the loan term.")

with st.expander("📌 What happens if I pay off my loan early?"):
    st.write("Paying off your loan early saves you interest. Some banks charge a prepayment fee, so check with your lender.")

# 🎯 Final Message
st.markdown("🔹 **This calculator helps you make smarter mortgage decisions by understanding your payments, loan term, and interest impact.**")







# 🎨 Header
st.markdown("<h1 style='text-align: center; color: darkblue;'>💰 Loan Eligibility & EMI Calculator</h1>", unsafe_allow_html=True)
st.write("🔹 This tool helps you understand if you qualify for a loan and how much you need to pay every month.")
st.write("🔹 **Step 1:** Enter your loan details and financial information.")
st.write("🔹 **Step 2:** The app will check if you are eligible for the loan.")
st.write("🔹 **Step 3:** You will see the **EMI breakdown, total interest paid, and loan summary** in an easy-to-understand format.")

# 📌 Sidebar - User Inputs
st.sidebar.header("🔧 Customize Your Loan Details")

monthly_income = st.sidebar.number_input("💵 Monthly Income (₹)", min_value=10000, value=50000, step=5000, format="%.0f")
credit_score = st.sidebar.slider("📊 Credit Score (300-900)", min_value=300, max_value=900, value=750, step=10)
existing_emi = st.sidebar.number_input("💳 Existing EMI Payments (₹)", min_value=0, value=0, step=5000, format="%.0f")
loan_amount = st.sidebar.number_input("🏠 Desired Loan Amount (₹)", min_value=50000, value=1000000, step=50000, format="%.0f")
interest_rate = st.sidebar.slider("📈 Interest Rate (%)", min_value=1.0, max_value=20.0, value=10.0, step=0.1)
loan_tenure = st.sidebar.slider("📅 Loan Tenure (Years)", min_value=1, max_value=30, value=20, step=1)

# 📌 Loan Eligibility Calculation
max_emi = 0.4 * monthly_income  # 40% rule
emi_affordable = max_emi - existing_emi

def calculate_emi(P, r, n):
    r = (r / 100) / 12  # Convert annual interest rate to monthly rate
    n = n * 12  # Convert tenure to months
    if r == 0:
        return P / n  # If 0% interest, simple division
    return (P * r * (1 + r) ** n) / ((1 + r) ** n - 1)

emi = calculate_emi(loan_amount, interest_rate, loan_tenure)

# 📊 Display Loan Eligibility
st.markdown("## 🏦 Loan Eligibility Result")
if emi <= emi_affordable:
    st.success(f"✅ **Congratulations!** You are eligible for this loan. Your EMI will be **₹{emi:,.2f} per month**.")
    st.write("💡 **What this means:** You can afford this loan comfortably based on your monthly income.")
else:
    st.error(f"❌ **Oops!** Your EMI (₹{emi:,.2f}) is higher than what you can afford (₹{emi_affordable:,.2f}).")
    st.write("💡 **What you can do:**")
    st.write("- Reduce the loan amount.")
    st.write("- Increase the loan tenure to lower monthly payments.")
    st.write("- Improve your credit score for better loan offers.")

# 📌 Loan Summary
st.markdown("## 📋 Loan Summary")
total_payment = emi * loan_tenure * 12
total_interest = total_payment - loan_amount
st.info(f"💰 **Total Interest Paid:** ₹{total_interest:,.2f}")
st.success(f"🏦 **Total Amount Paid (Principal + Interest):** ₹{total_payment:,.2f}")
st.write("💡 **Understanding this:** This is the total amount you will pay over the loan period, including interest.")

# 📊 Loan Balance Over Time (Amortization Table)
st.markdown("## 📉 Loan Balance Over Time")
def generate_amortization_schedule(P, r, n):
    r = (r / 100) / 12  # Monthly interest rate
    n = n * 12  # Total months
    balance = P
    schedule = []
    for month in range(1, n + 1):
        interest = balance * r if r > 0 else 0
        principal = emi - interest
        balance -= principal
        if balance < 0:
            balance = 0
        schedule.append([month, principal, interest, balance])
        if balance == 0:
            break
    return pd.DataFrame(schedule, columns=["Month", "Principal Paid", "Interest Paid", "Remaining Balance"])

schedule = generate_amortization_schedule(loan_amount, interest_rate, loan_tenure)
st.dataframe(schedule.style.format({"Principal Paid": "₹{:,.2f}", "Interest Paid": "₹{:,.2f}", "Remaining Balance": "₹{:,.2f}"}))

# 📊 Loan Balance Graph
fig, ax = plt.subplots(figsize=(8, 4))
ax.plot(schedule["Month"], schedule["Remaining Balance"], label="Loan Balance", color="red", linewidth=2)
ax.set_xlabel("Month")
ax.set_ylabel("Loan Balance (₹)")
ax.legend()
st.pyplot(fig)

# 🍰 Interest vs. Principal Pie Chart
st.markdown("## 📊 Loan Payment Breakdown")
fig, ax = plt.subplots()
ax.pie([total_interest, loan_amount], labels=["Interest", "Principal"], autopct="%1.1f%%", colors=["orange", "green"], wedgeprops={"edgecolor": "black"})
st.pyplot(fig)

# 📢 Loan Insights
st.markdown("## 🔍 Smart Loan Tips")
st.write("💡 **Tips to Improve Loan Approval:**")
st.write("- Pay off existing debts to **increase eligibility**.")
st.write("- Improve your **credit score** for better interest rates.")
st.write("- Choose a **longer tenure** to reduce EMI, but beware of higher interest paid!")
st.write("- Try making **extra payments** to save on interest.")
st.write("💡 **Final Advice:** A well-planned loan can help you achieve your financial goals while keeping repayments manageable.")

st.markdown("🔹 **Use this tool to plan your loan better and make smart financial decisions!** 🚀")

 
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import os

# 🏦 Streamlit Page Configuration
st.set_page_config(page_title="📊 Business Expense Tracker", page_icon="💰", layout="wide")

# 🎨 Header
st.markdown("<h1 style='text-align: center; color: darkblue;'>📊 Business Expense Tracker</h1>", unsafe_allow_html=True)
st.write("🚀 **Track your business expenses, analyze spending trends, and manage your budget effectively!**")
st.write("💡 **Why use this app?**")
st.write("- 📌 **Record all your expenses in one place.**")
st.write("- 📊 **Visualize where your money is going.**")
st.write("- 📉 **Identify areas where you can save costs.**")
st.write("- 💰 **Download reports for tax and business planning.**")

# 📂 Load or Create Expense Data
csv_file = "business_expenses.csv"
if os.path.exists(csv_file):
    df = pd.read_csv(csv_file)
else:
    df = pd.DataFrame(columns=["Date","Category","Amount (â‚¹)","Payment Method","Description"])


# 📌 Sidebar - User Inputs for Adding Expenses
st.sidebar.header("📝 Add a New Expense")
date = st.sidebar.date_input("📅 Date of Expense")
category = st.sidebar.selectbox("📂 Expense Category", ["Rent", "Salaries", "Marketing", "Utilities", "Office Supplies", "Travel", "Internet", "Software", "Maintenance", "Food & Beverages"])
amount = st.sidebar.number_input("💵 Amount Spent (₹)", min_value=1, step=100, format="%.2f")
payment_method = st.sidebar.selectbox("💳 Payment Method", ["Cash", "Credit Card", "Debit Card", "UPI", "Bank Transfer"])
description = st.sidebar.text_input("📝 Short Description")

if st.sidebar.button("💾 Add Expense"):
    new_data = pd.DataFrame([[date, category, amount, payment_method, description]], columns=df.columns)
    df = pd.concat([df, new_data], ignore_index=True)
    df.to_csv(csv_file, index=False)
    st.sidebar.success("✅ Expense added successfully! Check the table below.")
    st.experimental_rerun()

# 📌 Display Expense Data
st.markdown("## 📋 Your Expense Records")
st.dataframe(df, use_container_width=True)

# 📊 Expense Summary
st.markdown("## 📊 Summary of Expenses")
if not df.empty:
    total_spent = df["Amount (₹)"].sum()
    st.success(f"💰 **Total Money Spent:** ₹{total_spent:,.2f}")
    
    # 📊 Category-wise Expense Breakdown
    st.markdown("### 📌 Breakdown by Category")
    category_summary = df.groupby("Category")["Amount (₹)"].sum().sort_values(ascending=False)
    fig, ax = plt.subplots(figsize=(8,4))
    category_summary.plot(kind="bar", color="skyblue", ax=ax)
    ax.set_ylabel("Amount (₹)")
    ax.set_xlabel("Category")
    ax.set_title("Expense Breakdown by Category")
    st.pyplot(fig)
    
    # 🍰 Expense Pie Chart
    st.markdown("### 🍰 Expense Distribution")
    fig, ax = plt.subplots()
    category_summary.plot(kind="pie", autopct="%1.1f%%", colors=["orange", "green", "blue", "purple", "red"], wedgeprops={"edgecolor": "black"}, ax=ax)
    ax.set_ylabel("")
    st.pyplot(fig)

# 📌 Download Expense Report
st.markdown("## 📥 Download Your Expense Report")
st.download_button(label="📥 Download Report (CSV)", data=df.to_csv(index=False), file_name="business_expense_report.csv", mime="text/csv")

# 🎯 Insights & Recommendations
st.markdown("## 💡 Smart Business Insights")
st.write("🔍 **What this data tells you:**")
st.write("- 📢 **Are you overspending on rent or salaries?**")
st.write("- 📊 **Is your marketing budget bringing returns?**")
st.write("- 💰 **Can you cut down unnecessary spending?**")
st.write("- 🚀 **What areas need more investment for growth?**")
st.write("💡 **Tip:** Regularly tracking your expenses helps you make smarter financial decisions and grow your business sustainably! 🚀")
