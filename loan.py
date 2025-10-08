import streamlit as st
import pandas as pd

st.set_page_config(page_title="Tata Capital Loan Chatbot", layout="wide")

# ---------------------------
# Synthetic Customer Data
# ---------------------------
customers_data = [
    {"name": "Amit Sharma", "age": 32, "mobile": "9999991111", "address": "Mumbai",
     "cibil_score": 780, "pre_approved_limit": 500000, "pan": "ABCDE1234F"},
    {"name": "Priya Iyer", "age": 28, "mobile": "8888882222", "address": "Delhi",
     "cibil_score": 720, "pre_approved_limit": 300000, "pan": "PQRS5678K"},
    {"name": "Rohit Gupta", "age": 40, "mobile": "7777773333", "address": "Pune",
     "cibil_score": 650, "pre_approved_limit": 200000, "pan": "LMNO9012T"},
    # ... add all 20 customers ...
]

customers = pd.DataFrame(customers_data)

# ---------------------------
# Worker Agents
# ---------------------------
def sales_agent(customer, loan_amount, tenure, interest):
    return f"Sales Agent: Hello {customer['name']}! Your pre-approved limit is ₹{customer['pre_approved_limit']}. You requested ₹{loan_amount} for {tenure} years at {interest}% p.a."

def verification_agent(customer, entered_pan, entered_mobile):
    pan_check = "✅" if entered_pan==customer["pan"] else "❌"
    mobile_check = "✅" if entered_mobile==customer["mobile"] else "❌"
    if pan_check=="✅" and mobile_check=="✅":
        return f"Verification Agent: KYC Approved ✅"
    else:
        return f"Verification Agent: KYC Failed ❌ (PAN:{pan_check}, Mobile:{mobile_check})"

def underwriting_agent(customer, loan_amount, tenure):
    credit_score = customer["cibil_score"]
    limit = customer["pre_approved_limit"]
    if credit_score < 700:
        return "Underwriting Agent: ❌ Rejected due to low CIBIL score."
    if loan_amount <= limit:
        return "Underwriting Agent: ✅ Approved within pre-approved limit."
    elif loan_amount <= 2*limit:
        return "Underwriting Agent: ✅ Approved after manual check."
    else:
        return "Underwriting Agent: ❌ Loan exceeds 2× pre-approved limit."

# ---------------------------
# Streamlit Chat UI
# ---------------------------
st.title("💬 Tata Capital Loan Chatbot - Interactive Hackathon Demo")

if "chat_history" not in st.session_state:
    st.session_state["chat_history"] = []

# Select customer
customer_name = st.selectbox("Select Customer", customers["name"].tolist())
customer = customers[customers["name"]==customer_name].iloc[0]

# ---- Chat simulation ----
def add_message(sender, message):
    st.session_state.chat_history.append({"sender": sender, "message": message})

# Step 1: Customer says hello
if len(st.session_state.chat_history) == 0:
    add_message("user", "Hello, I want a personal loan.")

# Step 2: Show pre-approved limit + select amount, tenure, interest
with st.form("loan_request_form"):
    loan_amount = st.number_input(f"Enter Loan Amount (max ₹{customer['pre_approved_limit']})",
                                  min_value=10000, max_value=customer['pre_approved_limit'],
                                  value=customer['pre_approved_limit'], step=5000)
    tenure = st.selectbox("Select Tenure (years)", [1,2,3,4,5])
    interest = st.slider("Select Interest Rate (% p.a.)", min_value=16, max_value=24, value=18)
    submitted = st.form_submit_button("Submit Loan Request")
    
    if submitted:
        add_message("bot", sales_agent(customer, loan_amount, tenure, interest))

# Step 3: KYC Verification
with st.form("kyc_form"):
    entered_pan = st.text_input("Enter PAN Number")
    entered_mobile = st.text_input("Enter Mobile Number")
    kyc_submit = st.form_submit_button("Verify KYC")
    
    if kyc_submit:
        kyc_result = verification_agent(customer, entered_pan, entered_mobile)
        add_message("bot", kyc_result)
        if "✅" in kyc_result:
            uw_result = underwriting_agent(customer, loan_amount, tenure)
            add_message("bot", uw_result)

# Display chat messages
for chat in st.session_state.chat_history:
    if chat["sender"] == "user":
        st.chat_message("user").write(chat["message"])
    else:
        st.chat_message("assistant").write(chat["message"])
