import logging
import sys
import os
import streamlit as st
from inference import load_model, load_preprocessing_components, predict

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Configure logging
logging.basicConfig(
    filename='predictions.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# Page configuration
st.set_page_config(
    page_title="Loan Default Prediction",
    page_icon="🏦",
    layout="wide"
)

# App title and description
st.title("🏦 Loan Default Prediction")
st.markdown("""
This application predicts whether a loan applicant is likely to default on their loan.
Enter the loan details below to get a prediction.
""")

# Load model and components


@st.cache_resource
def load_model_and_components():
    """Load the trained model and preprocessing components."""
    try:
        model = load_model()
        components = load_preprocessing_components()
        return model, components
    except Exception as e:
        st.error(f"Failed to load model: {str(e)}")
        return None, None


model, components = load_model_and_components()

if model is None or components is None:
    st.stop()

# Input form
with st.form("loan_prediction_form"):
    st.header("📋 Enter Loan Details")

    # Create two columns for better layout
    col1, col2 = st.columns(2)

    with col1:
        loan_amount = st.number_input(
            "Loan Amount ($)",
            min_value=0.0,
            value=20000.0,
            step=1000.0,
            help="Total amount of the loan"
        )
        mortgage_amount = st.number_input(
            "Mortgage Amount ($)",
            min_value=0.0,
            value=140000.0,
            step=1000.0,
            help="Amount of the mortgage"
        )
        property_value = st.number_input(
            "Property Value ($)",
            min_value=0.0,
            value=200000.0,
            step=1000.0,
            help="Value of the property"
        )
        loan_reason = st.selectbox(
            "Loan Reason",
            ["DebtCon", "HomeImp"],
            help="DebtCon = Debt Consolidation, HomeImp = Home Improvement"
        )
        occupation_length = st.number_input(
            "Occupation Length (years)",
            min_value=0.0,
            value=5.0,
            step=0.5,
            help="Years in current occupation"
        )
        derogatory_reports = st.number_input(
            "Derogatory Reports",
            min_value=0.0,
            value=0.0,
            step=1.0,
            help="Number of derogatory reports"
        )

    with col2:
        late_payments = st.number_input(
            "Late Payments",
            min_value=0.0,
            value=0.0,
            step=1.0,
            help="Number of late payments"
        )
        oldest_credit_line = st.number_input(
            "Oldest Credit Line (months)",
            min_value=0.0,
            value=120.0,
            step=1.0,
            help="Age of oldest credit line in months"
        )
        recent_credit = st.number_input(
            "Recent Credit",
            min_value=0.0,
            value=1.0,
            step=1.0,
            help="Recent credit inquiries"
        )
        credit_number = st.number_input(
            "Credit Number",
            min_value=0.0,
            value=20.0,
            step=1.0,
            help="Number of credit lines"
        )
        ratio = st.number_input(
            "Debt-to-Income Ratio (%)",
            min_value=0.0,
            value=35.0,
            step=1.0,
            help="Debt-to-income ratio percentage"
        )
        occupation = st.selectbox(
            "Occupation",
            ["Manager", "Office", "Other",
                "Professional/Executive", "Sales", "Self-employed"],
            index=2,  # Default to "Other"
            help="Applicant's occupation"
        )

    # Submit button
    submitted = st.form_submit_button("🔮 Predict Loan Default", type="primary")

# Handle form submission
if submitted:
    try:
        # Prepare input data
        input_data = {
            "loan_amount": loan_amount,
            "mortgage_amount": mortgage_amount,
            "property_value": property_value,
            "loan_reason": loan_reason,
            "occupation_length": occupation_length,
            "derogatory_reports": derogatory_reports,
            "late_payments": late_payments,
            "oldest_credit_line": oldest_credit_line,
            "recent_credit": recent_credit,
            "credit_number": credit_number,
            "ratio": ratio,
            "occupation": occupation
        }

        # Make prediction
        with st.spinner("Analyzing loan application..."):
            prediction = predict(input_data, model, components)

        # Display result
        st.header("📊 Prediction Result")

        if prediction == 1:
            st.error("🚨 **HIGH RISK: Loan Default Predicted**")
            st.markdown("""
            **Recommendation:** This application shows a high risk of default.
            Consider additional verification or higher interest rates.
            """)
        else:
            st.success("✅ **LOW RISK: No Default Predicted**")
            st.markdown("""
            **Recommendation:** This application shows a low risk of default.
            Standard loan terms may be appropriate.
            """)

        # Log prediction (without sensitive data)
        logging.info(
            f"Streamlit prediction: {'Default' if prediction == 1 else 'No Default'}")

    except Exception as e:
        st.error(f"❌ **Prediction Error:** {str(e)}")
        logging.error(f"Streamlit prediction error: {str(e)}")

# Add sidebar with information
with st.sidebar:
    st.header("ℹ️ About")
    st.markdown("""
    This application uses a machine learning model trained on historical loan data
    to predict the likelihood of loan default.
    
    **Model Features:**
    - Loan amount and terms
    - Property and mortgage details
    - Credit history and reports
    - Employment information
    - Debt-to-income ratio
    
    **Disclaimer:** This is a demonstration model and should not be used
    for actual loan decisions without proper validation.
    """)

    st.header("📈 Model Performance")
    st.markdown("""
    - **Accuracy:** ~95%
    - **Weighted F1 Score:** ~94%
    - **Model Type:** Support Vector Machine (SVM)
    - **Training Data:** Historical loan applications
    """)
