import streamlit as st
import pandas as pd
import random
import time
from fpdf import FPDF
import base64

st.set_page_config(page_title="Tata Capital Loan Assistant", layout="wide")

# ---------------------------
# Customer Data (20 customers)
# ---------------------------
customers_data = [
    {"name": "Amit Sharma", "dob": "1991-05-12", "mobile": "9999991111", "address": "Mumbai",
     "cibil_score": 780, "pre_approved_limit": 500000, "pan": "ABCDE1234F"},
    {"name": "Priya Iyer", "dob": "1995-08-22", "mobile": "8888882222", "address": "Delhi",
     "cibil_score": 720, "pre_approved_limit": 300000, "pan": "PQRS5678K"},
    {"name": "Rohit Gupta", "dob": "1984-11-05", "mobile": "7777773333", "address": "Pune",
     "cibil_score": 650, "pre_approved_limit": 200000, "pan": "LMNO9012T"},
    {"name": "Neha Verma", "dob": "1988-02-18", "mobile": "6666664444", "address": "Nagpur",
     "cibil_score": 810, "pre_approved_limit": 700000, "pan": "QRST3456U"},
    {"name": "Karan Mehta", "dob": "1994-07-30", "mobile": "9998887777", "address": "Bangalore",
     "cibil_score": 690, "pre_approved_limit": 250000, "pan": "UVWX7890Y"},
    {"name": "Sneha Nair", "dob": "1992-09-10", "mobile": "5554443333", "address": "Hyderabad",
     "cibil_score": 760, "pre_approved_limit": 600000, "pan": "JKLM2345A"},
    {"name": "Vikram Singh", "dob": "1986-03-15", "mobile": "4445556666", "address": "Chennai",
     "cibil_score": 720, "pre_approved_limit": 400000, "pan": "EFGH3456B"},
    {"name": "Anita Desai", "dob": "1996-01-25", "mobile": "3332221111", "address": "Ahmedabad",
     "cibil_score": 770, "pre_approved_limit": 350000, "pan": "IJKL5678C"},
    {"name": "Rajat Kapoor", "dob": "1989-12-12", "mobile": "2223334444", "address": "Kolkata",
     "cibil_score": 800, "pre_approved_limit": 550000, "pan": "MNOP6789D"},
    {"name": "Megha Patil", "dob": "1993-04-03", "mobile": "1112223333", "address": "Surat",
     "cibil_score": 710, "pre_approved_limit": 300000, "pan": "QRST8901E"},
    {"name": "Sandeep Jain", "dob": "1987-10-09", "mobile": "9991112222", "address": "Jaipur",
     "cibil_score": 690, "pre_approved_limit": 280000, "pan": "UVWX2345F"},
    {"name": "Ritu Malhotra", "dob": "1990-06-18", "mobile": "8882221111", "address": "Lucknow",
     "cibil_score": 740, "pre_approved_limit": 500000, "pan": "ABCD3456G"},
    {"name": "Aditya Rao", "dob": "1994-09-05", "mobile": "7771112222", "address": "Bhopal",
     "cibil_score": 730, "pre_approved_limit": 320000, "pan": "EFGH4567H"},
    {"name": "Pooja Sharma", "dob": "1992-11-20", "mobile": "6662221111", "address": "Chandigarh",
     "cibil_score": 780, "pre_approved_limit": 450000, "pan": "IJKL5678I"},
    {"name": "Manish Gupta", "dob": "1986-08-08", "mobile": "5551112222", "address": "Indore",
     "cibil_score": 760, "pre_approved_limit": 480000, "pan": "MNOP6789J"},
    {"name": "Divya Singh", "dob": "1995-02-14", "mobile": "4441112222", "address": "Patna",
     "cibil_score": 720, "pre_approved_limit": 350000, "pan": "QRST7890K"},
    {"name": "Vivek Mehra", "dob": "1989-07-19", "mobile": "3331112222", "address": "Coimbatore",
     "cibil_score": 750, "pre_approved_limit": 400000, "pan": "UVWX8901L"},
    {"name": "Shweta Joshi", "dob": "1993-03-27", "mobile": "2221113333", "address": "Nagpur",
     "cibil_score": 770, "pre_approved_limit": 370000, "pan": "ABCD9012M"},
    {"name": "Aakash Sharma", "dob": "1991-12-11", "mobile": "1113332222", "address": "Delhi",
     "cibil_score": 800, "pre_approved_limit": 600000, "pan": "EFGH0123N"},
    {"name": "Rhea Kapoor", "dob": "1994-05-15", "mobile": "9993332222", "address": "Mumbai",
     "cibil_score": 740, "pre_approved_limit": 320000, "pan": "IJKL1234O"},
]

customers = pd.DataFrame(customers_data)

# ---------------------------
# Worker Agents
# ---------------------------
def sales_agent(customer, loan_amount, tenure, interest, purpose):
    return f"Bank: Hello {customer['name']}! Your pre-approved limit is ₹{customer['pre_approved_limit']}. You requested ₹{loan_amount} for {tenure} years at {interest}% p.a. Purpose: {purpose}"

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
# Session State Initialization
# ---------------------------
if "step" not in st.session_state:
    st.session_state.step = 0
    st.session_state.customer = None
    st.session_state.loan_amount = None
    st.session_state.tenure = None
    st.session_state.interest = random.randint(16,24)
    st.session_state.purpose = None

st.title("💰 Tata Capital Personal Loan Portal")
st.subheader("Transforming aspirations into realities")

# Step 0: PAN + DOB input
if st.session_state.step==0:
    pan_input = st.text_input("Enter PAN Number")
    dob_input = st.text_input("Enter Date of Birth (YYYY-MM-DD)")
    purpose = st.selectbox("Purpose of Loan", ["Travel", "Education", "Shopping", "Healthcare", "Other"])
    
    if st.button("Fetch CIBIL Report"):
        # Validate PAN + DOB
        matched_customer = [c for c in customers_data if c["pan"]==pan_input and c["dob"]==dob_input]
        if matched_customer:
            st.session_state.customer = matched_customer[0]
            st.session_state.purpose = purpose
            st.session_state.step = 1
        else:
            st.warning("No customer found with provided PAN & DOB!")

# Step 1: Loan Request
if st.session_state.step==1:
    customer = st.session_state.customer
    st.write(f"Bank: Hello {customer['name']}! Let's check your pre-approved loan details...")
    
    loan_amount = st.number_input("Enter Loan Amount", min_value=10000, max_value=customer['pre_approved_limit'], step=5000)
    tenure = st.selectbox("Select Tenure (years)", [1,2,3,4,5])
    
    if st.button("Proceed to CIBIL Check"):
        st.session_state.loan_amount = loan_amount
        st.session_state.tenure = tenure
        st.session_state.step = 2

# Step 2: CIBIL Check
if st.session_state.step==2:
    st.write("Bank: Fetching your credit report from CIBIL Bureau...")
    time.sleep(1.5)
    st.write(f"Bank: Credit score fetched ✅ CIBIL Score: {st.session_state.customer['cibil_score']}")
    st.session_state.step = 3

# Step 3: KYC Verification
if st.session_state.step==3:
    customer = st.session_state.customer
    pan = st.text_input("Enter PAN Number for KYC")
    mobile = st.text_input("Enter Mobile Number for KYC")
    
    if st.button("Verify KYC"):
        kyc_result = verification_agent(customer, pan, mobile)
        st.write(f"Bank: {kyc_result}")
        if "Approved" in kyc_result:
            st.session_state.step = 4
        else:
            st.warning("KYC Failed. Please enter correct details.")

# Step 4: Underwriting
if st.session_state.step==4:
    uw_result = underwriting_agent(st.session_state.customer, st.session_state.loan_amount)
    st.write(f"Underwriting Result: {uw_result}")
    
    if "Approved" in uw_result:
        st.success("🎉 Loan approved! Proceed to download sanction letter on next page.")
        if st.button("Generate Sanction Letter"):
            st.session_state.step = 5
    else:
        st.error("Loan Rejected. Process ends here.")

# Step 5: Sanction Letter PDF
if st.session_state.step==5:
    # Safe access
    if not all(k in st.session_state for k in ["loan_amount","tenure","customer","interest","purpose"]):
        st.warning("Some details are missing! Go back and complete the process first.")
        st.stop()
    
    customer = st.session_state.customer
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    
    pdf.multi_cell(0, 8, f"""
TATA CAPITAL FINANCE

Sanction Letter

Dear {customer['name']},

We are pleased to inform you that your personal loan request has been sanctioned.

Loan Details:
PAN: {customer['pan']}
DOB: {customer['dob']}
Mobile: {customer['mobile']}
Address: {customer['address']}
Loan Amount: ₹{st.session_state.loan_amount}
Tenure: {st.session_state.tenure} years
Interest Rate: {st.session_state.interest}% p.a.
Purpose: {st.session_state.purpose}

Please note, this sanction is subject to the terms and conditions of Tata Capital Finance.

Best regards,
Tata Capital Loan Desk
    """)
    
    pdf_output = "sanction_letter.pdf"
    pdf.output(pdf_output)
    
    # Provide download
    with open(pdf_output, "rb") as f:
        bytes_data = f.read()
    b64 = base64.b64encode(bytes_data).decode()
    href = f'<a href="data:application/octet-stream;base64,{b64}" download="sanction_letter.pdf">📄 Download Sanction Letter PDF</a>'
    st.markdown(href, unsafe_allow_html=True)
