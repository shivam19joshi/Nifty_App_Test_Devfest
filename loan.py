import streamlit as st
import pandas as pd

st.set_page_config(page_title="Tata Capital Loan Chatbot", layout="wide")

# ---------------------------
# Customer Data
# ---------------------------
customers_data = [
    {"name": "Amit Sharma", "age": 32, "mobile": "9999991111", "address": "Mumbai",
     "cibil_score": 780, "pre_approved_limit": 500000, "pan": "ABCDE1234F"},
    {"name": "Priya Iyer", "age": 28, "mobile": "8888882222", "address": "Delhi",
     "cibil_score": 720, "pre_approved_limit": 300000, "pan": "PQRS5678K"},
    # Add remaining 18 customers...
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
        return "Verification Agent: KYC Approved ✅"
    else:
        return f"Verification Agent: KYC Failed ❌ (PAN:{pan_check}, Mobile:{mobile_check})"

def underwriting_agent(customer, loan_amount):
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
# Initialize session state
# ---------------------------
if "stage" not in st.session_state:
    st.session_state.stage = "select_customer"
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# ---------------------------
# Chat message handler
# ---------------------------
def add_message(sender, message):
    st.session_state.chat_history.append({"sender": sender, "message": message})

# Display chat
for chat in st.session_state.chat_history:
    if chat["sender"] == "user":
        st.chat_message("user").write(chat["message"])
    else:
        st.chat_message("assistant").write(chat["message"])

# ---------------------------
# Customer selection
# ---------------------------
if st.session_state.stage == "select_customer":
    customer_name = st.selectbox("Select Customer", customers["name"].tolist())
    if st.button("Start Chat"):
        st.session_state.customer = customers[customers["name"]==customer_name].iloc[0]
        add_message("assistant", f"Hello {customer_name}! I am your Loan Assistant. Your pre-approved limit is ₹{st.session_state.customer['pre_approved_limit']}. Please type the amount you want and tenure in years (e.g., 250000 3).")
        st.session_state.stage = "loan_request"

# ---------------------------
# Chat input for interactive typing
# ---------------------------
if st.session_state.stage in ["loan_request", "kyc_pan", "kyc_mobile"]:

    if user_input := st.chat_input("Type your message..."):
        add_message("user", user_input)
        customer = st.session_state.customer

        # Loan request stage
        if st.session_state.stage == "loan_request":
            try:
                parts = user_input.split()
                loan_amount = int(parts[0])
                tenure = int(parts[1])
                interest = 18  # default interest
                st.session_state.loan_amount = loan_amount
                st.session_state.tenure = tenure
                st.session_state.interest = interest
                add_message("assistant", sales_agent(customer, loan_amount, tenure, interest))
                add_message("assistant", "Please enter your PAN number:")
                st.session_state.stage = "kyc_pan"
            except:
                add_message("assistant", "Please enter in format: <amount> <tenure> (e.g., 250000 3)")

        # KYC PAN stage
        elif st.session_state.stage == "kyc_pan":
            st.session_state.entered_pan = user_input
            add_message("assistant", "Now enter your registered Mobile Number:")
            st.session_state.stage = "kyc_mobile"

        # KYC Mobile stage
        elif st.session_state.stage == "kyc_mobile":
            st.session_state.entered_mobile = user_input
            kyc_result = verification_agent(customer, st.session_state.entered_pan, st.session_state.entered_mobile)
            add_message("assistant", kyc_result)
            if "✅" in kyc_result:
                uw_result = underwriting_agent(customer, st.session_state.loan_amount)
                add_message("assistant", uw_result)
                st.session_state.stage = "completed"
            else:
                add_message("assistant", "KYC Failed. Please restart the chat with correct details.")
                st.session_state.stage = "loan_request"
