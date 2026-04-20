# House Prices API - Docker Deployment with Railway

This section demonstrates how to containerize and deploy the FastAPI House Prices API to Railway using CircleCI for CI/CD and Gemfury for private package management.

## Overview

- **Framework**: FastAPI
- **Container**: Docker
- **Deployment**: Railway
- **CI/CD**: CircleCI
- **Package Registry**: Gemfury
- **Python Version**: 3.11

## Architecture

```
┌─────────────┐
│   GitHub    │
│ Repository  │
└──────┬──────┘
       │ Push
       ▼
┌─────────────────┐
│   CircleCI      │
│   Pipeline      │
└──────┬──────────┘
       │
       ├─ Test Job ──────────────────┐
       │  ├─ Install dependencies    │
       │  │  (from Gemfury)          │
       │  ├─ Run unit tests          │
       │  └─ Run linting checks      │
       │                             │
       ├─ Deploy Job ──────────────┐ │
       │  ├─ Build Docker image    │ │
       │  ├─ Push to Registry      │ │
       │  └─ Deploy to Railway     │ │
       │                           │ │
       └─────────────────────────────┘
                      │
                      ▼
           ┌──────────────────────┐
           │     Railway.app      │
           │                      │
           │  house-prices-api   │
           │  (running on Docker)│
           │  Port: 8001          │
           └──────────────────────┘
```

## File Structure

```
section-08-deploying-with-containers/
│
├── Dockerfile                      # Container image definition
├── .dockerignore                   # Files excluded from Docker build
├── run-local.sh                    # Local testing script
├── deploy-railway.sh               # Deployment script
├── .env.template                   # Environment template
├── SETUP_INSTRUCTIONS.md           # Step-by-step setup guide
├── README.md                       # This file
│
└── house-prices-api/              # FastAPI application
    ├── app/
    │   ├── main.py                 # FastAPI app definition
    │   ├── config.py               # Configuration settings
    │   ├── api.py                  # API routes
    │   └── schemas/                # Pydantic schemas
    │       └── predict.py           # Prediction schema
    │
    ├── requirements.txt             # Python dependencies
    │   └── tid-regression-model (from Gemfury)
    │
    ├── test_requirements.txt        # Testing dependencies
    ├── typing_requirements.txt      # Type checking dependencies
    ├── tox.ini                      # Test automation config
    ├── mypy.ini                     # Type checking config
    │
    ├── run.sh                      # Container startup script
    ├── Procfile                    # Process definition
    ├── .env.example                # Example environment variables
    ├── railway.json                # Railway service config
    │
    └── tests/                      # Unit tests
        └── test_*.py                # Test modules
```

## Getting Started

### Prerequisites

- Git
- Docker (for local testing)
- Python 3.11+ (for local development)
- CircleCI account (connected to GitHub)
- Railway account
- Gemfury account

### Quick Setup

1. **Read the setup guide**:
   ```bash
   cat SETUP_INSTRUCTIONS.md
   ```

2. **Configure environment variables** in CircleCI

3. **Push to main branch** to trigger deployment:
   ```bash
   git add .
   git commit -m "Setup Railway deployment"
   git push origin master
   ```

## Deployment Process

### Automatic (Recommended)

1. Push code to `master` or `demo` branch
2. CircleCI automatically:
   - Runs tests
   - Builds Docker image
   - Deploys to Railway
3. Monitor at: https://app.circleci.com/

### Manual

```bash
cd section-08-deploying-with-containers

# Install dependencies
pip install -r house-prices-api/requirements.txt

# Run tests locally
cd house-prices-api
tox

# Or build and test Docker locally
cd ..
bash run-local.sh

# Deploy to Railway
bash deploy-railway.sh
```

## Configuration

### Environment Variables

Set these in CircleCI project settings:

```bash
# Gemfury Configuration
GEMFURY_TOKEN=<your-gemfury-token>
GEMFURY_USERNAME=<your-username>
PIP_EXTRA_INDEX_URL=https://<username>:<token>@gem.fury.io/<username>/

# Railway Configuration
RAILWAY_PROJECT_ID=<your-railway-project-id>
RAILWAY_API_TOKEN=<your-railway-api-token>
```

Set these in Railway dashboard:

```bash
# API Configuration
PROJECT_NAME=House Prices API
API_V1_STR=/api/v1
BACKEND_CORS_ORIGINS=["https://your-domain.railway.app"]

# Python Configuration
PYTHONUNBUFFERED=1
LOGGING_LEVEL=INFO
PORT=8001
```

## Docker

### Build Locally

```bash
# Set your Gemfury URL
export PIP_EXTRA_INDEX_URL="https://<username>:<token>@gem.fury.io/<username>/"

# Build the image
docker build --build-arg PIP_EXTRA_INDEX_URL=$PIP_EXTRA_INDEX_URL \
  -t house-prices-api:local .
```

### Run Locally

```bash
docker run -p 8001:8001 \
  -e PIP_EXTRA_INDEX_URL=$PIP_EXTRA_INDEX_URL \
  house-prices-api:local
```

### Or use the script

```bash
bash run-local.sh
```

## API Testing

### Health Check
```bash
curl https://your-railway-domain.railway.app/
```

### API Documentation
```bash
# Interactive Swagger UI
https://your-railway-domain.railway.app/docs

# ReDoc documentation
https://your-railway-domain.railway.app/redoc
```

### Make a Prediction
```bash
curl -X POST https://your-railway-domain.railway.app/api/v1/predictions/predict \
  -H "Content-Type: application/json" \
  -d '{
    "MSSubClass": 20,
    "LotFrontage": 80,
    "LotArea": 9600,
    ...
  }'
```

## Testing

### Locally

```bash
cd house-prices-api

# Run all tests
tox

# Run specific test file
tox -e test_app -- app/tests/test_prediction.py

# Run with coverage
pip install pytest-cov
pytest --cov=app app/tests/
```

### CircleCI

Tests run automatically on every commit:
- View logs at: https://app.circleci.com/
- Filter by project: "deploying-machine-learning-models"
- Check "section_08_test_app_and_container" job

## Troubleshooting

### CircleCI Build Failures

**Error: PIP_EXTRA_INDEX_URL not set**
- ✅ Add to CircleCI environment variables
- ✅ Verify format: `https://username:token@gem.fury.io/username/`

**Error: Package tid-regression-model not found**
- ✅ Verify package is published on Gemfury
- ✅ Check token has correct permissions
- ✅ Verify token is not expired

**Error: Tests failing**
- ✅ Check test output in CircleCI logs
- ✅ Run tests locally: `cd house-prices-api && tox`
- ✅ Verify all dependencies in requirements.txt

### Railway Deployment Failures

**Error: Build fails with Docker**
- ✅ Check Dockerfile syntax
- ✅ Verify build argument is passed
- ✅ Check Docker image logs: `railway logs`

**Error: Container crashes on startup**
- ✅ Check environment variables are set in Railway dashboard
- ✅ Verify PORT is correctly used in run.sh
- ✅ Check application logs: `railway logs`

**Error: 502 Bad Gateway**
- ✅ Check if application is running: `railway logs`
- ✅ Verify health endpoint responds
- ✅ Check port configuration

### Local Docker Issues

**Error: Package installation fails**
```bash
# Ensure PIP_EXTRA_INDEX_URL is set
export PIP_EXTRA_INDEX_URL="https://user:token@gem.fury.io/user/"

# Rebuild with correct argument
docker build --build-arg PIP_EXTRA_INDEX_URL=$PIP_EXTRA_INDEX_URL \
  -t house-prices-api:local .
```

**Error: Cannot connect to container**
```bash
# Check if container is running
docker ps

# View logs
docker logs <container-id>

# Test connection
curl http://localhost:8001/
```

## Monitoring & Logs

### CircleCI
- **Dashboard**: https://app.circleci.com/
- **View pipeline**: Click on repository
- **View job logs**: Click on failed/successful jobs

### Railway
- **Dashboard**: https://railway.app/
- **View logs**: `railway logs` or Railway dashboard
- **View metrics**: CPU, Memory, Network in dashboard
- **Real-time logs**: `railway logs --follow`

## Security

✅ **Best Practices Implemented**:
- Non-root user in Docker (ml-api-user)
- Environment variables for secrets
- Secrets managed by CircleCI and Railway
- CORS configuration for specific domains
- No hardcoded credentials in code

⚠️ **Important**:
- Never commit .env files
- Rotate tokens regularly
- Use strong passwords
- Enable 2FA on all accounts
- Review CORS origins for your domain

## Performance Optimization

### Caching
- Docker layer caching enabled in CircleCI
- Pip cache for faster builds

### Scaling
- Railway handles auto-scaling
- Configure in Railway dashboard

### Monitoring
- Set up log alerts
- Monitor error rates
- Track response times

## CI/CD Pipeline Details

### Workflow: `deploy_pipeline`

```yaml
section_07_test_app
       ↓
section_07_deploy_app_to_railway
       ↓
section_07_test_and_upload_regression_model
       ↓
section_08_test_app_and_container  ← NEW
       ↓
section_08_deploy_app_container_via_railway  ← NEW
```

### section_08_test_app_and_container Job
- **When**: Every commit
- **What**: Runs tox tests, type checks, style checks
- **Uses**: Python 3.11, Tox
- **Passes**: `PIP_EXTRA_INDEX_URL` to access Gemfury packages

### section_08_deploy_app_container_via_railway Job
- **When**: Only on `master` or `demo` branch, after tests pass
- **What**: Builds Docker image, deploys to Railway
- **Uses**: Docker, Railway CLI
- **Passes**: `PIP_EXTRA_INDEX_URL` to Dockerfile

## Next Steps

1. ✅ Complete SETUP_INSTRUCTIONS.md
2. ✅ Configure CircleCI environment variables
3. ✅ Configure Railway project
4. ✅ Push to master to trigger deployment
5. ✅ Monitor CircleCI and Railway logs
6. ✅ Set up custom domain (optional)
7. ✅ Configure monitoring and alerts
8. ✅ Set up automated backups

## Resources

- [Railway Docs](https://docs.railway.app/) - Deployment platform
- [CircleCI Docs](https://circleci.com/docs/) - CI/CD platform
- [Gemfury Docs](https://gemfury.com/help) - Package registry
- [FastAPI Docs](https://fastapi.tiangolo.com/) - Web framework
- [Docker Docs](https://docs.docker.com/) - Containerization

## Support

If you encounter issues:
1. Check this README
2. Check SETUP_INSTRUCTIONS.md
3. Review CircleCI logs
4. Review Railway logs
5. Check deployment status on CircleCI and Railway dashboards

---

**Last Updated**: 2026-04-19
**Python**: 3.11
**FastAPI**: 0.88.0+
**Status**: ✅ Ready for Production

