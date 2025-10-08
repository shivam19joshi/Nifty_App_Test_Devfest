import streamlit as st
import pandas as pd
from fpdf import FPDF
import os

st.set_page_config(page_title="Tata Capital Loan Assistant", layout="wide")

# ---------------------------
# Font setup (local)
# ---------------------------
FONT_FILE = "DejaVuSans.ttf"
if not os.path.exists(FONT_FILE):
    st.warning("Font file 'DejaVuSans.ttf' not found. Please add it to project folder.")
    st.stop()

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
])

# ---------------------------
# Worker Agents
# ---------------------------
def sales_agent(customer, loan_amount, tenure):
    return f"Sales Agent: {customer['name']}, your requested loan is ₹{loan_amount} for {tenure} years."

def verification_agent(customer):
    return f"Verification Agent: ✅ KYC Verified for {customer['name']}."

def underwriting_agent(customer, loan_amount, tenure):
    credit_score = customer["credit_score"]
    limit = customer["pre_approved_limit"]
    salary = customer["salary"]
    if credit_score < 700:
        return "Underwriting Agent: ❌ Rejected due to low credit score."
    if loan_amount <= limit:
        return "Underwriting Agent: ✅ Approved within pre-approved limit."
    elif loan_amount <= 2*limit:
        emi = (loan_amount / (tenure*12))*1.1
        if emi <= 0.5*salary:
            return "Underwriting Agent: ✅ Approved after salary check."
        return "Underwriting Agent: ❌ EMI exceeds 50% of salary."
    return "Underwriting Agent: ❌ Loan exceeds 2× pre-approved limit."

# ---------------------------
# Sanction Letter Generator
# ---------------------------
def generate_sanction_letter(customer, loan_amount, tenure):
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
    file_name = f"Sanction_Letter_{customer['name'].replace(' ','_')}.pdf"
    pdf.output(file_name)
    return file_name

# ---------------------------
# Streamlit Pages
# ---------------------------
page = st.sidebar.selectbox("Select Page", ["Chatbot Loan Process", "Sanction Letter"])

if page == "Chatbot Loan Process":
    st.title("💬 Tata Capital Loan Assistant - Chatbot")
    
    # Select customer
    customer_name = st.selectbox("Select Customer", customers["name"].tolist())
    customer = customers[customers["name"]==customer_name].iloc[0]
    
    # Loan details (preset for demo)
    loan_amount = customer["pre_approved_limit"]  # auto fetch
    tenure = 3
    
    st.write("### Chatbot Conversation")
    st.write(sales_agent(customer, loan_amount, tenure))
    st.write(verification_agent(customer))
    uw_result = underwriting_agent(customer, loan_amount, tenure)
    st.write(uw_result)
    
    # Store info in session_state for next page
    st.session_state['customer'] = customer
    st.session_state['loan_amount'] = loan_amount
    st.session_state['tenure'] = tenure
    st.session_state['underwriting'] = uw_result

elif page == "Sanction Letter":
    st.title("📝 Sanction Letter Generation")
    
    # Fetch details from session_state
    if 'customer' not in st.session_state:
        st.warning("Go to 'Chatbot Loan Process' page first to process a loan.")
    else:
        customer = st.session_state['customer']
        loan_amount = st.session_state['loan_amount']
        tenure = st.session_state['tenure']
        uw_result = st.session_state['underwriting']
        
        st.write(f"Customer: {customer['name']}")
        st.write(f"Loan Amount: ₹{loan_amount}")
        st.write(f"Tenure: {tenure} years")
        st.write(f"Underwriting Result: {uw_result}")
        
        if "✅" in uw_result:
            file_name = generate_sanction_letter(customer, loan_amount, tenure)
            with open(file_name, "rb") as f:
                st.download_button("⬇️ Download Sanction Letter", f, file_name=file_name)
            st.success("Sanction letter generated successfully ✅")
        else:
            st.error("Loan not approved, cannot generate sanction letter.")
