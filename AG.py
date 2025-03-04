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
st.markdown("<h1 style='text-align: center; color: darkblue;'>🏦 Indian Bank Loan Finder</h1>", unsafe_allow_html=True)
st.write("🔹 Find the best Indian bank for your loan needs based on interest rates and eligibility criteria.")

# 📂 Load Dataset (You should replace this with the actual file path)
@st.cache_data
def load_data():
    df = pd.read_csv("loan_data_train.csv")  # Replace with actual dataset
    return df

df = load_data()

# 🎯 User Input Section
st.sidebar.header("🔧 Customize Your Loan Requirements")
loan_amount = st.sidebar.number_input("💰 Loan Amount (INR)", min_value=10000, value=500000, step=10000)
loan_purpose = st.sidebar.selectbox("🎯 Loan Purpose", df["Loan.Purpose"].unique())
credit_score = st.sidebar.slider("📊 Your Credit Score (FICO Range)", min_value=300, max_value=900, value=750, step=10)
monthly_income = st.sidebar.number_input("💵 Monthly Income (INR)", min_value=10000, value=50000, step=5000)
debt_to_income_ratio = st.sidebar.slider("💳 Debt-to-Income Ratio (%)", min_value=0, max_value=100, value=20, step=1)
loan_length = st.sidebar.selectbox("📅 Loan Tenure", df["Loan.Length"].unique())

# 📌 Filter Banks Based on User Input
filtered_banks = df[(df["Loan.Purpose"] == loan_purpose) & (df["Amount.Requested"] >= loan_amount)]

# 📊 Sorting Banks by Interest Rate
filtered_banks = filtered_banks.sort_values(by=["Interest.Rate"], ascending=True)

# 🏆 Suggest Best Bank
def recommend_best_bank():
    best_bank = filtered_banks.iloc[0] if not filtered_banks.empty else None
    return best_bank

best_bank = recommend_best_bank()

# 📌 Loan Recommendation
st.markdown("## 🏦 Best Bank Recommendation")
if best_bank is not None:
    st.success(f"✅ **Best Bank for Your Loan:** {best_bank['State']} (Interest Rate: {best_bank['Interest.Rate']}%)")
    st.write(f"- **Loan Amount Approved:** ₹{best_bank['Amount.Funded.By.Investors']:,.2f}")
    st.write(f"- **Loan Tenure:** {best_bank['Loan.Length']}")
    st.write(f"- **Debt-to-Income Ratio Requirement:** {best_bank['Debt.To.Income.Ratio']}%")
else:
    st.error("❌ No banks found matching your criteria. Try adjusting the filters.")

# 📌 Show All Bank Options
st.markdown("## 📋 List of Indian Banks Offering Loans")
st.dataframe(filtered_banks[['State', 'Interest.Rate', 'Loan.Length', 'Debt.To.Income.Ratio']].reset_index(drop=True))

# 📊 Visualization - Interest Rate Distribution
st.markdown("## 📊 Interest Rate Distribution Across Banks")
fig, ax = plt.subplots()
ax.hist(df["Interest.Rate"], bins=20, color='blue', alpha=0.7)
ax.set_xlabel("Interest Rate (%)")
ax.set_ylabel("Number of Banks")
ax.set_title("Distribution of Loan Interest Rates")
st.pyplot(fig)

# 🎯 Final Insights
st.markdown("🔹 **Compare banks based on interest rates, tenure, and eligibility to make the best financial decision.**")
