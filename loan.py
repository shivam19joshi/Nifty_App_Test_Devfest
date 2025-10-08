import streamlit as st
from fpdf import FPDF
import os

# Ensure letters folder exists
if not os.path.exists("letters"):
    os.makedirs("letters")

# Function to generate sanction letter
def sanction_letter_generator(name, amount, tenure):
    pdf = FPDF()
    pdf.add_page()

    # Add a Unicode font (DejaVuSans supports ₹ and other symbols)
    pdf.add_font("DejaVu", "", fname="/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", uni=True)
    pdf.set_font("DejaVu", size=12)

    # Title
    pdf.cell(200, 10, txt="Loan Sanction Letter", ln=True, align='C')
    pdf.ln(10)

    # Content
    pdf.multi_cell(0, 10, f"""
Dear {name},

We are pleased to inform you that your loan has been sanctioned.

Loan Details:
- Sanctioned Amount: ₹{amount:,}
- Loan Tenure: {tenure} months

Kindly contact our branch for further formalities.

Regards,
Loan Department
    """)

    # Save file
    file_path = f"letters/Sanction_Letter_{name.replace(' ', '_')}.pdf"
    pdf.output(file_path)
    return file_path

# ---------------- Streamlit UI ---------------- #
st.set_page_config(page_title="Loan Sanction Letter", page_icon="🏦")

st.title("🏦 Loan Sanction Letter Generator")

# Inputs
name = st.text_input("Enter Applicant Name")
amount = st.number_input("Enter Loan Amount (₹)", min_value=1000, step=1000)
tenure = st.number_input("Enter Tenure (in months)", min_value=1, step=1)

# Generate button
if st.button("Generate Sanction Letter"):
    if name and amount and tenure:
        file_path = sanction_letter_generator(name, amount, tenure)

        with open(file_path, "rb") as f:
            st.download_button(
                label="📥 Download Sanction Letter",
                data=f,
                file_name=os.path.basename(file_path),
                mime="application/pdf"
            )

        st.success("✅ Sanction letter generated successfully!")

    else:
        st.error("⚠️ Please enter all details to generate the letter.")
