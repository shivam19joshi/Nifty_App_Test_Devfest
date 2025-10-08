import streamlit as st
import pandas as pd

st.set_page_config(page_title="Tata Capital Loan Chatbot", layout="wide")

# ---------------------------
# Synthetic Customer Data (20 customers)
# ---------------------------
customers_data = [
    {"name": "Amit Sharma", "age": 32, "mobile": "9999991111", "address": "Mumbai",
     "cibil_score": 780, "pre_approved_limit": 500000, "pan": "ABCDE1234F"},
    {"name": "Priya Iyer", "age": 28, "mobile": "8888882222", "address": "Delhi",
     "cibil_score": 720, "pre_approved_limit": 300000, "pan": "PQRS5678K"},
    {"name": "Rohit Gupta", "age": 40, "mobile": "7777773333", "address": "Pune",
     "cibil_score": 650, "pre_approved_limit": 200000, "pan": "LMNO9012T"},
    {"name": "Neha Verma", "age": 35, "mobile": "6666664444", "address": "Nagpur",
     "cibil_score": 810, "pre_approved_limit": 700000, "pan": "QRST3456U"},
    {"name": "Karan Mehta", "age": 29, "mobile": "9998887777", "address": "Bangalore",
     "cibil_score": 690, "pre_approved_limit": 250000, "pan": "UVWX7890Y"},
    {"name": "Sneha Nair", "age": 31, "mobile": "5554443333", "address": "Hyderabad",
     "cibil_score": 760, "pre_approved_limit": 600000, "pan": "JKLM2345A"},
    {"name": "Vikram Singh", "age": 38, "mobile": "4445556666", "address": "Chennai",
     "cibil_score": 720, "pre_approved_limit": 400000, "pan": "EFGH3456B"},
    {"name": "Anita Desai", "age": 27, "mobile": "3332221111", "address": "Ahmedabad",
     "cibil_score": 770, "pre_approved_limit": 350000, "pan": "IJKL5678C"},
    {"name": "Rajat Kapoor", "age": 34, "mobile": "2223334444", "address": "Kolkata",
     "cibil_score": 800, "pre_approved_limit": 550000, "pan": "MNOP6789D"},
    {"name": "Megha Patil", "age": 30, "mobile": "1112223333", "address": "Surat",
     "cibil_score": 710, "pre_approved_limit": 300000, "pan": "QRST8901E"},
    {"name": "Sandeep Jain", "age": 36, "mobile": "9991112222", "address": "Jaipur",
     "cibil_score": 690, "pre_approved_limit": 280000, "pan": "UVWX2345F"},
    {"name": "Ritu Malhotra", "age": 33, "mobile": "8882221111", "address": "Lucknow",
     "cibil_score": 740, "pre_approved_limit": 500000, "pan": "ABCD3456G"},
    {"name": "Aditya Rao", "age": 29, "mobile": "7771112222", "address": "Bhopal",
     "cibil_score": 730, "pre_approved_limit": 320000, "pan": "EFGH4567H"},
    {"name": "Pooja Sharma", "age": 31, "mobile": "6662221111", "address": "Chandigarh",
     "cibil_score": 780, "pre_approved_limit": 450000, "pan": "IJKL5678I"},
    {"name": "Manish Gupta", "age": 37, "mobile": "5551112222", "address": "Indore",
     "cibil_score": 760, "pre_approved_limit": 480000, "pan": "MNOP6789J"},
    {"name": "Divya Singh", "age": 28, "mobile": "4441112222", "address": "Patna",
     "cibil_score": 720, "pre_approved_limit": 350000, "pan": "QRST7890K"},
    {"name": "Vivek Mehra", "age": 35, "mobile": "3331112222", "address": "Coimbatore",
     "cibil_score": 750, "pre_approved_limit": 400000, "pan": "UVWX8901L"},
    {"name": "Shweta Joshi", "age": 30, "mobile": "2221113333", "address": "Nagpur",
     "cibil_score": 770, "pre_approved_limit": 370000, "pan": "ABCD9012M"},
    {"name": "Aakash Sharma", "age": 32, "mobile": "1113332222", "address": "Delhi",
     "cibil_score": 800, "pre_approved_limit": 600000, "pan": "EFGH0123N"},
    {"name": "Rhea Kapoor", "age": 29, "mobile": "9993332222", "address": "Mumbai",
     "cibil_score": 740, "pre_approved_limit": 320000, "pan": "IJKL1234O"},
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
# Session state initialization
# ---------------------------
if "stage" not in st.session_state:
    st.session_state.stage = "select_customer"
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# ---------------------------
# Chat helper
# ---------------------------
def add_message(sender, message):
    st.session_state.chat_history.append({"sender": sender, "message": message})

for chat in st.session_state.chat_history:
    if chat["sender"]=="user":
        st.chat_message("user").write(chat["message"])
    else:
        st.chat_message("assistant").write(chat["message"])

# ---------------------------
# Customer selection
# ---------------------------
st.title("💬 Tata Capital Loan Chatbot")

if st.session_state.stage == "select_customer":
    customer_name = st.selectbox("Select Customer", customers["name"].tolist())
    if st.button("Start Chat"):
        st.session_state.customer = customers[customers["name"]==customer_name].iloc[0]
        add_message("assistant", f"Hello {customer_name}! I am your Loan Assistant. Please type 'Hello' to start your loan request.")
        st.session_state.stage = "greet"

# ---------------------------
# Chat input
# ---------------------------
if st.session_state.stage in ["greet", "loan_request", "interest_rate", "kyc_pan", "kyc_mobile"]:
    if user_input := st.chat_input("Type your message..."):
        add_message("user", user_input)
        customer = st.session_state.customer

        # Greeting stage
        if st.session_state.stage=="greet":
            if "hello" in user_input.lower():
                add_message("assistant", f"Great! Your pre-approved limit is ₹{customer['pre_approved_limit']}. Please enter loan amount and tenure in years (e.g., 250000 3).")
                st.session_state.stage = "loan_request"
            else:
                add_message("assistant", "Please type 'Hello' to start the loan request.")

        # Loan request stage
        elif st.session_state.stage=="loan_request":
            try:
                parts = user_input.split()
                loan_amount = int(parts[0])
                tenure = int(parts[1])
                st.session_state.loan_amount = loan_amount
                st.session_state.tenure = tenure
                add_message("assistant", "Please choose an interest rate between 16% - 24% p.a. (e.g., 18)")
                st.session_state.stage = "interest_rate"
            except:
                add_message("assistant", "Enter in format: <amount> <tenure> (e.g., 250000 3)")

        # Interest rate stage
        elif st.session_state.stage=="interest_rate":
            try:
                interest = float(user_input)
                if 16 <= interest <= 24:
                    st.session_state.interest = interest
                    add_message("assistant", sales_agent(customer, st.session_state.loan_amount, st.session_state.tenure, interest))
                    add_message("assistant", "Please enter your PAN number:")
                    st.session_state.stage = "kyc_pan"
                else:
                    add_message("assistant", "Interest must be between 16% - 24%. Try again.")
            except:
                add_message("assistant", "Please enter a valid number for interest rate.")

        # KYC PAN stage
        elif st.session_state.stage=="kyc_pan":
            st.session_state.entered_pan = user_input
            add_message("assistant", "Now enter your registered Mobile Number:")
            st.session_state.stage = "kyc_mobile"

        # KYC Mobile stage
        elif st.session_state.stage=="kyc_mobile":
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
