#!/bin/bash

# Loan Default Prediction - Docker Run Script

echo "🏦 Building Loan Default Prediction Docker Image..."

# Clean up any existing container
echo "🧹 Cleaning up existing containers..."
docker stop loan-prediction-container 2>/dev/null || true
docker rm loan-prediction-container 2>/dev/null || true

# Build the Docker image
docker build -t loan-prediction-app .

if [ $? -eq 0 ]; then
    echo "✅ Docker image built successfully!"
    
    echo "🚀 Starting the application..."
    echo "📱 Streamlit will be available at: http://localhost:8503"
    echo "🔧 FastAPI will be available at: http://localhost:8000"
    echo "⏹️  Press Ctrl+C to stop the application"
    
    # Run the container
    docker run -p 8503:8503 -p 8000:8000 \
        -v $(pwd)/data:/app/data:ro \
        -v $(pwd)/logs:/app/logs \
        --name loan-prediction-container \
        loan-prediction-app
else
    echo "❌ Docker build failed!"
    exit 1
fi 