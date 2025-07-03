# 🏦 Loan Default Prediction

A machine learning application that predicts whether a loan applicant will default on their loan. Built with FastAPI and Streamlit, containerized with Docker, and deployable to AWS ECS.

---

## 🚀 Project Overview

- **Input:** Loan application details (12 fields)
- **Output:** Prediction of "Default" or "No Default"
- **Model:** Support Vector Machine (SVM)
- **Frontend:** Streamlit
- **API:** FastAPI
- **Deployment:** Docker (local), AWS ECS Fargate (cloud)

---

## 📁 Project Structure

```
loan_default_prediction/
├── app/
│   ├── __init__.py
│   ├── inference.py
│   ├── main.py
│   └── streamlit_app.py
├── data/
│   └── .gitkeep
├── notebooks/
│   └── sas-challenge.ipynb
├── requirements.txt
├── Dockerfile
├── .dockerignore
├── .gitignore
├── README.md
└── LICENSE
```

---

## 🛠️ Local Development

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Start the API Server
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### 3. Start the Streamlit Web App
```bash
streamlit run app/streamlit_app.py
```

---

## 🐳 Docker Usage

### Build and Run Locally
```bash
docker build -t loan-prediction-app .
docker run -d -p 8503:8503 --name test-streamlit loan-prediction-app
# Visit http://localhost:8503
```

---

## ☁️ AWS Deployment (ECS Fargate)

1. **Build and Push Docker Image to ECR**
   ```bash
   docker tag loan-prediction-app:latest <your-account-id>.dkr.ecr.<region>.amazonaws.com/loan-prediction-app:latest
   docker push <your-account-id>.dkr.ecr.<region>.amazonaws.com/loan-prediction-app:latest
   ```

2. **Deploy to ECS**
   - Use the provided `deploy-aws.sh` script or follow the AWS Console steps.
   - Ensure your ECS service uses a public subnet and security group allows inbound TCP on port 8503.

3. **Access the App**
   - Find your ECS task's public IP.
   - Visit: `http://<public-ip>:8503`

---

## 📋 API Usage

### Health Check
```bash
curl http://localhost:8000/health
```

### Make a Prediction
```bash
curl -X POST "http://localhost:8000/predict" \
  -H "Content-Type: application/json" \
  -d '{ ... }'
```

---

## 📝 Model Input Fields

| Field                | Example   | Description                        |
|----------------------|-----------|------------------------------------|
| loan_amount          | 20000     | Loan amount in dollars             |
| mortgage_amount      | 140000    | Mortgage amount in dollars         |
| property_value       | 200000    | Property value in dollars          |
| loan_reason          | "DebtCon" | "DebtCon" or "HomeImp"             |
| occupation_length    | 5         | Years in current job               |
| derogatory_reports   | 0         | Number of bad credit reports       |
| late_payments        | 0         | Number of late payments            |
| oldest_credit_line   | 120       | Age of oldest credit (months)      |
| recent_credit        | 1         | Recent credit inquiries            |
| credit_number        | 20        | Number of credit accounts          |
| ratio                | 35.5      | Debt-to-income ratio (%)           |
| occupation           | "ProfExe" | Job type (see options below)       |

---

## 🧑‍💻 Development & Deployment Workflow

1. **Develop and test locally** (with or without Docker).
2. **Build Docker image** and verify locally.
3. **Push image to AWS ECR**.
4. **Deploy to AWS ECS Fargate** using the latest image.
5. **Configure security group** for public access on port 8503.
6. **Access your app** via the public IP and port 8503.

---

## ⚠️ Notes

- This is a demonstration model; not for real loan decisions.
- Do **not** commit large data/model files to GitHub.
- All predictions are logged (without personal data).

---

