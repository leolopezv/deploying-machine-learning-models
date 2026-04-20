# Quick Reference Card

## One-Command Setup

```powershell
cd "C:\Users\leona\OneDrive\SENECA\COURSE-FASTAPI\mldeploy-projects\deploying-machine-learning-models\section-06-model-serving-api\house-prices-api"; python -m pip install --upgrade pip setuptools wheel; pip install uvicorn fastapi python-multipart pydantic loguru pydantic-settings --upgrade; python -c "import sys; sys.path.insert(0, '.'); from app.main import app; import uvicorn; uvicorn.run(app, host='127.0.0.1', port=8000, log_level='info')"
```

## Step-by-Step Commands

### 1. Navigate to Project
```powershell
cd "C:\Users\leona\OneDrive\SENECA\COURSE-FASTAPI\mldeploy-projects\deploying-machine-learning-models\section-06-model-serving-api\house-prices-api"
```

### 2. Upgrade pip
```powershell
python -m pip install --upgrade pip setuptools wheel
```

### 3. Install Dependencies
```powershell
pip install uvicorn fastapi python-multipart pydantic loguru pydantic-settings --upgrade
```

### 4. Start Server (Port 8000)
```powershell
python -c "import sys; sys.path.insert(0, '.'); from app.main import app; import uvicorn; uvicorn.run(app, host='127.0.0.1', port=8000, log_level='info')"
```

**OR using uvicorn directly:**
```powershell
uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
```

## API URLs

| Endpoint | URL | Method |
|----------|-----|--------|
| Welcome | http://localhost:8000 | GET |
| API Docs (Swagger) | http://localhost:8000/docs | GET |
| ReDoc | http://localhost:8000/redoc | GET |
| OpenAPI Schema | http://localhost:8000/api/v1/openapi.json | GET |
| Health Check | http://localhost:8000/api/v1/health | GET |
| Predict | http://localhost:8000/api/v1/predict | POST |

## Test Commands

### Test Root Endpoint
```powershell
Invoke-WebRequest -Uri http://localhost:8000 -UseBasicParsing
```

### Test Health Endpoint
```powershell
Invoke-WebRequest -Uri http://localhost:8000/api/v1/health -UseBasicParsing | Select-Object -ExpandProperty Content
```

## Code Changes Summary

| File | Change | Reason |
|------|--------|--------|
| `app/config.py` | Import `BaseSettings` from `pydantic_settings` | Pydantic v2 compatibility |
| `app/api.py` | Add try-except for regression_model import | Handle missing ML model gracefully |
| `app/api.py` | Check REGRESSION_MODEL_AVAILABLE flag in predict | Return 503 instead of import error |
| `app/schemas/predict.py` | Add fallback HouseDataInputSchema | Support validation without regression_model |

## Installed Packages

```
uvicorn>=0.20.0      # ASGI server
fastapi>=0.88.0      # Web framework
python-multipart     # Form data support
pydantic>=2.13.0     # Data validation
loguru>=0.5.3        # Logging
pydantic-settings    # Settings for Pydantic v2
```

## Troubleshooting

### Port 8000 in use?
```powershell
# Use different port
uvicorn app.main:app --host 127.0.0.1 --port 8002

# OR find & kill process
netstat -ano | findstr :8000
taskkill /PID <PID> /F
```

### Import Error for BaseSettings?
```powershell
pip install pydantic-settings
```

### Module 'app' not found?
- Make sure you're in the correct directory
- Current working directory should be: `house-prices-api/`

### Predict endpoint returns 503?
- This is expected (ML model not installed)
- To enable: Install Visual Studio Build Tools, then `pip install tid-regression-model`

## Server Status

When started successfully, you should see:
```
INFO:     Started server process [PID]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
```

## Stop Server
```powershell
CTRL + C
```

## Browser Access
```
http://localhost:8000/docs
```

---

**Status:** ✅ API Running
**Last Test:** April 18, 2026

