from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import Dict, Any
import logging
from inference import load_model, load_preprocessing_components, predict

# Configure logging
logging.basicConfig(
    filename='predictions.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# Initialize FastAPI app
app = FastAPI(
    title="Loan Default Prediction API",
    description="API for predicting loan default risk using machine learning",
    version="1.0.0"
)

# Load model and components at startup
model = load_model()
components = load_preprocessing_components()


class LoanPredictionRequest(BaseModel):
    """Input model for loan prediction requests."""
    loan_amount: float = Field(..., description="Amount of the loan", ge=0)
    mortgage_amount: float = Field(..., description="Amount of mortgage", ge=0)
    property_value: float = Field(...,
                                  description="Value of the property", ge=0)
    loan_reason: str = Field(...,
                             description="Reason for loan: 'DebtCon' or 'HomeImp'")
    occupation_length: float = Field(...,
                                     description="Years in current occupation", ge=0)
    derogatory_reports: float = Field(...,
                                      description="Number of derogatory reports", ge=0)
    late_payments: float = Field(...,
                                 description="Number of late payments", ge=0)
    oldest_credit_line: float = Field(...,
                                      description="Age of oldest credit line", ge=0)
    recent_credit: float = Field(...,
                                 description="Recent credit inquiries", ge=0)
    credit_number: float = Field(...,
                                 description="Number of credit lines", ge=0)
    ratio: float = Field(..., description="Debt-to-income ratio", ge=0)
    occupation: str = Field(
        ..., description="Occupation: 'Mgr', 'Office', 'Other', 'ProfExe', 'Sales', 'Self'")

    # Optional fields for backward compatibility
    job: str = Field(None, description="Alternative field name for occupation")
    years_employed: float = Field(
        None, description="Alternative field name for occupation_length")


class LoanPredictionResponse(BaseModel):
    """Output model for loan prediction responses."""
    prediction: str = Field(...,
                            description="Prediction result: 'Default' or 'No Default'")


@app.get("/")
async def root():
    """Health check endpoint."""
    return {"message": "Loan Default Prediction API is running"}


@app.post("/predict", response_model=LoanPredictionResponse)
async def predict_default(request: LoanPredictionRequest):
    """
    Predict loan default risk.

    Args:
        request: Loan prediction request with required fields

    Returns:
        LoanPredictionResponse: Prediction result

    Raises:
        HTTPException: If prediction fails
    """
    try:
        # Convert Pydantic model to dict
        data = request.dict(exclude_none=True)

        # Make prediction
        prediction = predict(data, model, components)
        result = "Default" if prediction == 1 else "No Default"

        # Log prediction (without sensitive data)
        logging.info(f"Prediction made: {result}")

        return LoanPredictionResponse(prediction=result)

    except Exception as e:
        logging.error(f"Prediction error: {str(e)}")
        raise HTTPException(
            status_code=500, detail=f"Prediction failed: {str(e)}")


@app.get("/health")
async def health_check():
    """Health check endpoint for monitoring."""
    return {"status": "healthy", "model_loaded": model is not None}
