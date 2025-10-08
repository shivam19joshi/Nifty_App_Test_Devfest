import streamlit as st
import random
import json
from fpdf import FPDF

# --------------------------
# Dummy Customer Data (CRM + Pre-approved offers)
# --------------------------
customers = {
    "shivam": {
        "name": "Shivam Joshi",
        "age": 25,
        "city": "Nagpur",
        "phone": "9999999999",
        "address": "Nagpur, Maharashtra",
        "pre_approved_limit": 500000,   # 5 Lakhs
        "salary": 60000
    },
    "riya": {
        "name": "Riya Kapoor",
        "age": 29,
        "city": "Mumbai",
        "phone": "8888888888",
        "address": "Mumbai, Maharashtra",
        "pre_approved_limit": 300000,
        "salary": 45000
    }
}

# --------------------------
# Worker Agent: Verification
# --------------------------
def verification_agent(customer_id):
    cust = customers.get(customer_id)
    if cust:
        return f"KYC Verified ✅\nName: {cust['name']}\nCity: {cust['city']}\nPhone: {cust['phone']}"
    return "Customer not found ❌"

# --------------------------
# Worker Agent: Underwriting
# --------------------------
def underwriting_agent(customer_id, loan_amount, tenure, salary_slip_uploaded=False):
    cust = customers.get(customer_id)
    if not cust:
        return "❌ Customer not found", False
    
    credit_score = random.randint(650, 850)  # Mock Credit Bureau
    pre_limit = cust["pre_approved_limit"]
    salary = cust["salary"]
    
    # Simple EMI calc (flat interest assumption for demo)
    emi = loan_amount / tenure  
    
    # Decision Logic
    if credit_score < 700:
        return f"❌ Rejected. Credit Score = {credit_score} (<700)", False
    elif loan_amount <= pre_limit:
        return f"✅ Approved instantly. Credit Score = {credit_score}", True
    elif loan_amount <= 2 * pre_limit:
        if not salary_slip_uploaded:
            return f"📑 Need salary slip for further approval. Credit Score = {credit_score}", None
        else:
            if emi <= 0.5 * salary:
                return f"✅ Approved after salary slip check. Credit Score = {credit_score}", True
            else:
                return f"❌ Rejected. EMI {emi} > 50% of Salary {salary}", False
    else:
        return f"❌ Rejected. Loan amount {loan_amount} > 2x Pre-approved limit {pre_limit}", False

# --------------------------
# Worker Agent: Sanction Letter
# --------------------------
def sanction_letter_generator(customer_id, loan_amount, tenure, rate=12.0):
    cust = customers.get(customer_id)
    if not cust:
        return None
    
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt="Tata Capital - Personal Loan Sanction Letter", ln=True, align="C")
    pdf.ln(10)
    pdf.cell(200, 10, txt=f"Name: {cust['name']}", ln=True)
    pdf.cell(200, 10, txt=f"Loan Amount: {loan_amount}", ln=True)
    pdf.cell(200, 10, txt=f"Tenure: {tenure} months", ln=True)
    pdf.cell(200, 10, txt=f"Rate of Interest: {rate}%", ln=True)
    pdf.cell(200, 10, txt="Status: Approved ✅", ln=True)
    
    file_path = f"sanction_letter_{customer_id}.pdf"
    pdf.output(file_path)
    return file_path

# --------------------------
# Master Agent (Streamlit Chat UI)
# --------------------------
st.title("💬 Tata Capital Loan Sales Chatbot")

# Session State
if "chat" not in st.session_state:
    st.session_state.chat = []
if "verified" not in st.session_state:
    st.session_state.verified = False
if "approved" not in st.session_state:
    st.session_state.approved = None

# Chat input
user_input = st.chat_input("Say something...")

if user_input:
    st.session_state.chat.append(("user", user_input))
    
    # Master Agent Flow
    if "name" not in st.session_state:
        if user_input.lower() in customers:
            st.session_state["name"] = user_input.lower()
            reply = f"Hello {customers[user_input]['name']}! Welcome to Tata Capital. Let's get started with your loan process."
        else:
            reply = "Please enter a valid customer ID (e.g., 'shivam' or 'riya')."
    
    elif not st.session_state.verified:
        reply = verification_agent(st.session_state["name"])
        st.session_state.verified = True
    
    elif st.session_state.approved is None:
        try:
            amount, tenure = map(int, user_input.split())
            decision, status = underwriting_agent(st.session_state["name"], amount, tenure)
            reply = decision
            if status is True:
                st.session_state.approved = (amount, tenure)
            elif status is False:
                st.session_state.approved = False
        except:
            reply = "Please enter loan amount and tenure in months (e.g., '200000 24')."
    
    elif st.session_state.approved is not False and isinstance(st.session_state.approved, tuple):
        amount, tenure = st.session_state.approved
        file_path = sanction_letter_generator(st.session_state["name"], amount, tenure)
        reply = f"🎉 Congratulations! Your loan is approved.\n👉 [Download Sanction Letter]({file_path})"
        st.session_state.approved = "done"
    
    else:
        reply = "Sorry, your loan request could not be approved."
    
    st.session_state.chat.append(("bot", reply))

# Display chat
for role, msg in st.session_state.chat:
    if role == "user":
        st.chat_message("user").markdown(msg)
    else:
        st.chat_message("assistant").markdown(msg)
