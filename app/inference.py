import joblib
import pandas as pd
import os
from typing import Dict, Any, Tuple, List
from sklearn.preprocessing import LabelEncoder, StandardScaler, OneHotEncoder

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


def load_model() -> Any:
    """Load the trained model from disk."""
    model_path = os.path.join(BASE_DIR, 'data', 'loan_prediction_model.pkl')
    return joblib.load(model_path)


def load_preprocessing_components() -> Tuple[LabelEncoder, StandardScaler, OneHotEncoder]:
    """Load preprocessing components (label encoder, scaler, one-hot encoder) from disk."""
    components_path = os.path.join(
        BASE_DIR, 'data', 'preprocessing_components.pkl')
    components_dict = joblib.load(components_path)
    return (
        components_dict['label_encoder'],
        components_dict['standard_scaler'],
        components_dict['one_hot_encoder']
    )


def load_feature_names() -> List[str]:
    """Load the list of feature names used by the model."""
    feature_names_path = os.path.join(BASE_DIR, 'data', 'feature_names.pkl')
    with open(feature_names_path, 'rb') as f:
        return joblib.load(f)


def preprocess_input(data: Dict[str, Any], scaler: StandardScaler, feature_names: List[str]) -> pd.DataFrame:
    """
    Preprocess input data for prediction.
    - Maps alternate field names to standard ones.
    - Encodes categorical variables.
    - Applies one-hot encoding for occupation.
    - Applies scaling to numeric features.
    - Returns a DataFrame in the correct feature order.

    Expected input fields:
        loan_amount, mortgage_amount, property_value, loan_reason, occupation_length,
        derogatory_reports, late_payments, oldest_credit_line, recent_credit, credit_number, ratio, occupation
    """
    # Map alternate field names
    field_mapping = {
        'job': 'occupation',
        'years_employed': 'occupation_length'
    }
    for old_name, new_name in field_mapping.items():
        if old_name in data and new_name not in data:
            data[new_name] = data.pop(old_name)

    # Encode loan_reason
    if 'loan_reason' in data and isinstance(data['loan_reason'], str):
        loan_reason_mapping = {'DebtCon': 0, 'HomeImp': 1}
        data['loan_reason'] = loan_reason_mapping.get(data['loan_reason'], 0)

    # One-hot encode occupation
    if 'occupation' in data:
        occupation = data['occupation']
        occupation_cols = {
            'occupation_Mgr': 1 if occupation == 'Mgr' else 0,
            'occupation_Office': 1 if occupation == 'Office' else 0,
            'occupation_Other': 1 if occupation == 'Other' else 0,
            'occupation_ProfExe': 1 if occupation == 'ProfExe' else 0,
            'occupation_Sales': 1 if occupation == 'Sales' else 0,
            'occupation_Self': 1 if occupation == 'Self' else 0
        }
        data = {k: v for k, v in data.items() if k != 'occupation'}
        data.update(occupation_cols)

    # Create DataFrame and reindex
    input_df = pd.DataFrame([data])
    input_df = input_df.reindex(columns=feature_names, fill_value=0)

    # Apply scaling to the features that were scaled during training
    cols_to_scale = ['loan_amount', 'mortgage_amount', 'property_value',
                     'oldest_credit_line', 'ratio', 'occupation_length', 'derogatory_reports']
    input_df[cols_to_scale] = scaler.transform(input_df[cols_to_scale])

    return input_df


def predict(data: Dict[str, Any], model: Any, components: Tuple[LabelEncoder, StandardScaler, OneHotEncoder]) -> int:
    """
    Predict loan default (1=Default, 0=No Default) for a single input.
    Args:
        data: Input dictionary with required fields (see preprocess_input docstring).
        model: Trained model (GridSearchCV or estimator).
        components: Tuple of (label_encoder, scaler, one_hot_encoder).
    Returns:
        int: 1 for Default, 0 for No Default
    """
    _, scaler, _ = components
    feature_names = load_feature_names()
    input_df = preprocess_input(data, scaler, feature_names)
    if hasattr(model, 'best_estimator_'):
        best_model = model.best_estimator_
        prediction = best_model.predict(input_df)[0]
    else:
        prediction = model.predict(input_df)[0]
    return prediction
