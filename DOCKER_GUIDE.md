# Docker Guide for Loan Default Prediction

This guide will help you run the Loan Default Prediction application using Docker.

## Prerequisites

- Docker installed on your system
- Docker Compose (usually comes with Docker Desktop)

## Quick Start

### Option 1: Simple Docker Run (Recommended for testing)

```bash
# Make the script executable (if not already done)
chmod +x docker-run.sh

# Run the application
./docker-run.sh
```

This will:
- Build the Docker image
- Start the container
- Make Streamlit available at http://localhost:8503
- Make FastAPI available at http://localhost:8000

### Option 2: Docker Compose (Recommended for production)

```bash
# Start all services
docker-compose up --build

# Or run in background
docker-compose up -d --build
```

This will start:
- FastAPI backend on port 8000
- Streamlit frontend on port 8503

## Available Services

### 1. Streamlit Frontend
- **URL**: http://localhost:8503
- **Description**: Web interface for loan prediction
- **Features**: Interactive form, real-time predictions, visual results

### 2. FastAPI Backend
- **URL**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/health
- **Description**: REST API for loan predictions

## Docker Commands Reference

### Building the Image
```bash
# Build production image
docker build -t loan-prediction-app .

# Build development image
docker build --target development -t loan-prediction-dev .
```

### Running Containers
```bash
# Run Streamlit only
docker run -p 8503:8503 -v $(pwd)/data:/app/data:ro loan-prediction-app

# Run with both ports
docker run -p 8503:8503 -p 8000:8000 -v $(pwd)/data:/app/data:ro loan-prediction-app

# Run in background
docker run -d -p 8503:8503 -p 8000:8000 -v $(pwd)/data:/app/data:ro --name loan-app loan-prediction-app
```

### Docker Compose Commands
```bash
# Start services
docker-compose up

# Start in background
docker-compose up -d

# Start with rebuild
docker-compose up --build

# Stop services
docker-compose down

# View logs
docker-compose logs -f

# Start development environment
docker-compose --profile dev up
```

### Container Management
```bash
# List running containers
docker ps

# Stop container
docker stop loan-prediction-container

# Remove container
docker rm loan-prediction-container

# View container logs
docker logs loan-prediction-container

# Execute commands in container
docker exec -it loan-prediction-container bash
```

## Development Mode

For development with auto-reload:

```bash
# Build development image
docker build --target development -t loan-prediction-dev .

# Run development container
docker run -p 8503:8503 -p 8000:8000 \
  -v $(pwd)/app:/app/app \
  -v $(pwd)/data:/app/data:ro \
  loan-prediction-dev
```

## Troubleshooting

### Common Issues

1. **Port already in use**
   ```bash
   # Check what's using the port
   lsof -i :8503
   lsof -i :8000
   
   # Stop conflicting services or use different ports
   docker run -p 8504:8503 -p 8001:8000 loan-prediction-app
   ```

2. **Permission denied**
   ```bash
   # Fix script permissions
   chmod +x docker-run.sh
   ```

3. **Container won't start**
   ```bash
   # Check container logs
   docker logs loan-prediction-container
   
   # Check if data files exist
   ls -la data/
   ```

4. **Model loading errors**
   ```bash
   # Verify model files exist
   ls -la data/*.pkl
   
   # Check file permissions
   chmod 644 data/*.pkl
   ```

### Health Checks

- **Streamlit**: http://localhost:8503/_stcore/health
- **FastAPI**: http://localhost:8000/health

## Environment Variables

You can customize the application behavior:

```bash
# Set environment variables
docker run -e ENVIRONMENT=production -e LOG_LEVEL=INFO loan-prediction-app

# Or use .env file with docker-compose
docker-compose --env-file .env up
```

## Data Persistence

The application uses volume mounts for:
- **Data files**: `./data` (read-only)
- **Logs**: `./logs` (read-write)

```bash
# Check logs
tail -f logs/predictions.log

# Backup data
cp -r data/ backup/
```

## Performance Tips

1. **Use multi-stage builds** (already implemented)
2. **Cache dependencies** (requirements.txt copied first)
3. **Use .dockerignore** to exclude unnecessary files
4. **Run as non-root user** (already implemented)

## Security Considerations

- Application runs as non-root user (`appuser`)
- Data volumes are mounted as read-only where appropriate
- Health checks are implemented
- No sensitive data in container layers

## Next Steps

1. Test the application at http://localhost:8503
2. Try the API at http://localhost:8000/docs
3. Check the logs in the `logs/` directory
4. Customize the configuration as needed 