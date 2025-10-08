import streamlit as st
import pandas as pd
from fpdf import FPDF
import os
import urllib.request

# ---------------------------
# Ensure Unicode Font
# ---------------------------
FONT_URL = "https://github.com/dejavu-fonts/dejavu-fonts/raw/master/ttf/DejaVuSans.ttf"
FONT_FILE = "DejaVuSans.ttf"

if not os.path.exists(FONT_FILE):
    st.info("Downloading font for PDF generation...")
    urllib.request.urlretrieve(FONT_URL, FONT_FILE)
    st.success("Font downloaded ✅")

# ---------------------------
# Synthetic Customer Data
# ---------------------------
customers = pd.DataFrame([
    {"id": 1, "name": "Amit Sharma", "age": 32, "city": "Mumbai", "phone": "9999991111",
     "credit_score": 780, "pre_approved_limit": 500000, "salary": 60000},
    {"id": 2, "name": "Priya Iyer", "age": 28, "city": "Delhi", "phone": "8888882222",
     "credit_score": 720, "pre_approved_limit": 300000, "salary": 45000},
    {"id": 3, "name": "Rohit Gupta", "age": 40, "city": "Pune", "phone": "7777773333",
     "credit_score": 650, "pre_approved_limit": 200000, "salary": 35000},
    {"id": 4, "name": "Neha Verma", "age": 35, "city": "Nagpur", "phone": "6666664444",
     "credit_score": 810, "pre_approved_limit": 700000, "salary": 90000},
    {"id": 5, "name": "Karan Mehta", "age": 29, "city": "Bangalore", "phone": "9998887777",
     "credit_score": 690, "pre_approved_limit": 250000, "salary": 40000},
    {"id": 6, "name": "Sneha Nair", "age": 31, "city": "Hyderabad", "phone": "5554443333",
     "credit_score": 760, "pre_approved_limit": 600000, "salary": 75000},
    {"id": 7, "name": "Vikram Singh", "age": 45, "city": "Chennai", "phone": "4443332222",
     "credit_score": 720, "pre_approved_limit": 350000, "salary": 50000},
    {"id": 8, "name": "Ritu Jain", "age": 27, "city": "Kolkata", "phone": "3332221111",
     "credit_score": 840, "pre_approved_limit": 800000, "salary": 100000},
    {"id": 9, "name": "Sanjay Patil", "age": 39, "city": "Ahmedabad", "phone": "2221110000",
     "credit_score": 710, "pre_approved_limit": 400000, "salary": 55000},
    {"id": 10, "name": "Anjali Deshmukh", "age": 34, "city": "Jaipur", "phone": "1110009999",
     "credit_score": 680, "pre_approved_limit": 200000, "salary": 30000}
])

# ---------------------------
# Worker Agents
# ---------------------------
def sales_agent(customer, loan_amount, tenure):
    return f"Sales Agent: {customer['name']}, you requested ₹{loan_amount} for {tenure} years. Let’s check eligibility."

def verification_agent(customer, phone):
    if phone == customer["phone"]:
        return "Verification Agent: ✅ KYC verified."
    return "Verification Agent: ❌ KYC failed. Wrong phone number."

def underwriting_agent(customer, loan_amount, tenure, salary_slip_uploaded=False):
    credit_score = customer["credit_score"]
    pre_limit = customer["pre_approved_limit"]
    salary = customer["salary"]

    if credit_score < 700:
        return "Underwriting Agent: ❌ Rejected due to low credit score."
    
    if loan_amount <= pre_limit:
        return "Underwriting Agent: ✅ Approved instantly (within pre-approved limit)."
    
    elif loan_amount <= 2 * pre_limit:
        if not salary_slip_uploaded:
            return "Underwriting Agent: 📄 Please upload salary slip for verification."
        else:
            emi = (loan_amount / (tenure * 12)) * 1.1  # Simple EMI calculation
            if emi <= 0.5 * salary:
                return "Underwriting Agent: ✅ Approved after salary slip verification."
            return "Underwriting Agent: ❌ Rejected, EMI exceeds 50% of salary."
    
    return "Underwriting Agent: ❌ Rejected, request exceeds 2× pre-approved limit."

# ---------------------------
# Sanction Letter Generator
# ---------------------------
def sanction_letter_generator(customer, loan_amount, tenure):
    pdf = FPDF()
    pdf.add_page()
    pdf.add_font("DejaVu", "", FONT_FILE, uni=True)
    pdf.set_font("DejaVu", size=12)

    text = f"""
Loan Sanction Letter

Dear {customer['name']},

Congratulations! Your personal loan request has been approved.

Loan Amount: ₹{loan_amount}
Tenure: {tenure} years
Pre-Approved Limit: ₹{customer['pre_approved_limit']}
Credit Score: {customer['credit_score']}

Thank you for choosing Tata Capital.

Sincerely,
Tata Capital Loan Team
"""
    pdf.multi_cell(0, 10, text)
    file_name = f"Sanction_Letter_{customer['name'].replace(' ', '_')}.pdf"
    pdf.output(file_name)
    return file_name

# ---------------------------
# Master Agent Orchestration (Streamlit)
# ---------------------------
st.title("💬 Tata Capital - Agentic AI Loan Assistant")

customer_name = st.selectbox("Select Customer", customers["name"].tolist())
customer = customers[customers["name"] == customer_name].iloc[0]

st.write("### 👤 Customer Profile")
st.json(customer.to_dict())

loan_amount = st.number_input("Enter Loan Amount (₹)", 50000, 1000000, 200000, 5000)
tenure = st.slider("Select Tenure (years)", 1, 10, 3)
phone_input = st.text_input("Enter Phone for KYC Verification")

if st.button("Start Loan Process"):
    st.write(sales_agent(customer, loan_amount, tenure))

    verify_msg = verification_agent(customer, phone_input)
    st.write(verify_msg)

    if "❌" in verify_msg:
        st.error("Process stopped due to KYC failure.")
    else:
        uw_msg = underwriting_agent(customer, loan_amount, tenure)
        st.write(uw_msg)

        if "📄" in uw_msg:
            uploaded_file = st.file_uploader("Upload Salary Slip (PDF)", type=["pdf"])
            if uploaded_file and st.button("Recheck with Salary Slip"):
                uw_msg2 = underwriting_agent(customer, loan_amount, tenure, salary_slip_uploaded=True)
                st.write(uw_msg2)
                if "✅" in uw_msg2:
                    file_name = sanction_letter_generator(customer, loan_amount, tenure)
                    with open(file_name, "rb") as f:
                        st.download_button("⬇️ Download Sanction Letter", f, file_name=file_name)
                    st.success("Sanction letter generated successfully ✅")

        elif "✅" in uw_msg:
            file_name = sanction_letter_generator(customer, loan_amount, tenure)
            with open(file_name, "rb") as f:
                st.download_button("⬇️ Download Sanction Letter", f, file_name=file_name)
            st.success("Sanction letter generated successfully ✅")
