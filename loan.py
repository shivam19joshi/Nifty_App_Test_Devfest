import streamlit as st
import pandas as pd

st.set_page_config(page_title="Tata Capital Loan Assistant", layout="wide")

# ---------------------------
# Customer Data
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
    return f"Hello {customer['name']}! Your pre-approved limit is ₹{customer['pre_approved_limit']}. You requested ₹{loan_amount} for {tenure} years at {interest}% p.a."

def verification_agent(customer, pan, mobile):
    pan_check = "✅" if pan==customer["pan"] else "❌"
    mobile_check = "✅" if mobile==customer["mobile"] else "❌"
    if pan_check=="✅" and mobile_check=="✅":
        return "KYC Approved ✅"
    return f"KYC Failed ❌ (PAN:{pan_check}, Mobile:{mobile_check})"

def underwriting_agent(customer, loan_amount):
    if customer["cibil_score"] < 700:
        return "Loan Rejected ❌ due to low CIBIL score."
    limit = customer["pre_approved_limit"]
    if loan_amount <= limit:
        return "Loan Approved ✅ within pre-approved limit."
    elif loan_amount <= 2*limit:
        return "Loan Approved ✅ after manual check."
    else:
        return "Loan Rejected ❌ exceeds 2× pre-approved limit."

# ---------------------------
# Session State
# ---------------------------
if "step" not in st.session_state:
    st.session_state.step = 0

st.title("💰 Tata Capital Loan Assistant")

# Step 0: Select Customer
if st.session_state.step==0:
    customer_name = st.selectbox("Select Customer", customers["name"].tolist())
    if st.button("Start Loan Process"):
        st.session_state.customer = customers[customers["name"]==customer_name].iloc[0]
        st.session_state.step = 1

# Step 1: Show pre-approved limit & choose loan
if st.session_state.step==1:
    customer = st.session_state.customer
    st.write(f"Hello {customer['name']}! Your pre-approved limit is ₹{customer['pre_approved_limit']}.")
    loan_amount = st.number_input("Enter Loan Amount", min_value=10000, max_value=customer['pre_approved_limit'], step=5000)
    tenure = st.selectbox("Select Tenure (years)", [1,2,3,4,5])
    if st.button("Next: Interest Rate"):
        st.session_state.loan_amount = loan_amount
        st.session_state.tenure = tenure
        st.session_state.step = 2

# Step 2: Interest Rate Selection
if st.session_state.step==2:
    interest = st.slider("Select Interest Rate (%)", 16, 24, 18)
    if st.button("Next: KYC"):
        st.session_state.interest = interest
        st.session_state.step = 3

# Step 3: KYC Verification
if st.session_state.step==3:
    pan = st.text_input("Enter PAN Number")
    mobile = st.text_input("Enter Mobile Number")
    if st.button("Verify KYC"):
        kyc_result = verification_agent(st.session_state.customer, pan, mobile)
        st.write(kyc_result)
        if "Approved" in kyc_result:
            st.session_state.step = 4
        else:
            st.warning("KYC Failed. Please enter correct details.")

# Step 4: Underwriting
if st.session_state.step==4:
    uw_result = underwriting_agent(st.session_state.customer, st.session_state.loan_amount)
    st.write(f"Underwriting Result: {uw_result}")
    if "Approved" in uw_result:
        st.success("🎉 Loan is ready to be sanctioned on next page!")
    else:
        st.error("Loan Rejected. Process ends here.")
