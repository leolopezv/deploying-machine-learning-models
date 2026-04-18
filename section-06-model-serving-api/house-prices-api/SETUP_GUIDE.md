# House Price Prediction API - Setup Guide

## Overview
This document provides a comprehensive guide to setting up and running the House Price Prediction API locally.

---

## Prerequisites
- Python 3.13+
- pip (Python package manager)
- Windows PowerShell or Command Prompt

---

## Installation Steps

### Step 1: Install Core FastAPI Dependencies

```powershell
cd "C:\Users\leona\OneDrive\SENECA\COURSE-FASTAPI\mldeploy-projects\deploying-machine-learning-models\section-06-model-serving-api\house-prices-api"

pip install uvicorn fastapi python-multipart pydantic loguru --upgrade
```

**Packages Installed:**
- `uvicorn>=0.20.0` - ASGI web server
- `fastapi>=0.88.0` - Web framework
- `python-multipart>=0.0.5` - Multipart form data support
- `pydantic>=2.13.0` - Data validation using Python type annotations
- `loguru>=0.5.3` - Logging library

### Step 2: Install Pydantic Settings (Required for Pydantic v2)

```powershell
pip install pydantic-settings
```

**Note:** Pydantic v2 moved `BaseSettings` to a separate package. This is required to avoid the following error:
```
pydantic.errors.PydanticImportError: `BaseSettings` has been moved to the `pydantic-settings` package
```

### Step 3: Install Additional Dependencies (Optional)

```powershell
pip install numpy pandas scikit-learn scipy
```

These are used by the API for data processing. Numpy 2.x is already compatible.

---

## Code Changes Made

### Change 1: Update `app/config.py` - Fix Pydantic v2 Import

**File:** `app/config.py`

**Original Code (Lines 7):**
```python
from pydantic import AnyHttpUrl, BaseSettings
```

**Updated Code:**
```python
from pydantic import AnyHttpUrl
from pydantic_settings import BaseSettings
```

**Reason:** Pydantic v2 requires `BaseSettings` to be imported from `pydantic_settings` package.

---

### Change 2: Update `app/api.py` - Handle Missing Regression Model

**File:** `app/api.py`

**Original Code (Lines 8-9):**
```python
from regression_model import __version__ as model_version
from regression_model.predict import make_prediction
```

**Updated Code (Lines 14-21):**
```python
# Temporary workaround for missing regression_model dependency
try:
    from regression_model import __version__ as model_version
    from regression_model.predict import make_prediction
    REGRESSION_MODEL_AVAILABLE = True
except ImportError:
    model_version = "3.2.0 (unavailable)"
    REGRESSION_MODEL_AVAILABLE = False
```

**Reason:** The `tid-regression-model` package requires a C++ compiler to build numpy from source. This try-except block allows the API to start without the regression model installed.

**Updated Predict Endpoint (Lines 37-48):**
```python
@api_router.post("/predict", response_model=schemas.PredictionResults, status_code=200)
async def predict(input_data: schemas.MultipleHouseDataInputs) -> Any:
    """
    Make house price predictions with the TID regression model
    """
    
    if not REGRESSION_MODEL_AVAILABLE:
        raise HTTPException(
            status_code=503,
            detail="Regression model is not available. Please install tid-regression-model package."
        )
    # ... rest of the code
```

**Reason:** Returns a user-friendly 503 error when the regression model is not available, instead of a generic import error.

---

### Change 3: Update `app/schemas/predict.py` - Create Fallback Schema

**File:** `app/schemas/predict.py`

**Original Code (Lines 1-4):**
```python
from typing import Any, List, Optional

from pydantic import BaseModel
from regression_model.processing.validation import HouseDataInputSchema
```

**Updated Code (Lines 1-100):**
```python
from typing import Any, List, Optional

from pydantic import BaseModel

try:
    from regression_model.processing.validation import HouseDataInputSchema
except ImportError:
    # Fallback schema when regression_model is not available
    class HouseDataInputSchema(BaseModel):
        MSSubClass: Optional[int] = None
        MSZoning: Optional[str] = None
        LotFrontage: Optional[float] = None
        LotArea: Optional[int] = None
        # ... (all 81 house feature fields)
        SaleCondition: Optional[str] = None
```

**Reason:** Creates a fallback schema with all house features so the API can validate requests without the regression_model package installed.

---

## Running the Server

### Option 1: Direct Python Command (Recommended)

```powershell
cd "C:\Users\leona\OneDrive\SENECA\COURSE-FASTAPI\mldeploy-projects\deploying-machine-learning-models\section-06-model-serving-api\house-prices-api"

python -c "import sys; sys.path.insert(0, '.'); from app.main import app; import uvicorn; uvicorn.run(app, host='127.0.0.1', port=8000, log_level='info')"
```

### Option 2: Using Uvicorn Directly

```powershell
cd "C:\Users\leona\OneDrive\SENECA\COURSE-FASTAPI\mldeploy-projects\deploying-machine-learning-models\section-06-model-serving-api\house-prices-api"

uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
```

### Option 3: Run Python Main Module

```powershell
cd "C:\Users\leona\OneDrive\SENECA\COURSE-FASTAPI\mldeploy-projects\deploying-machine-learning-models\section-06-model-serving-api\house-prices-api"

python -m uvicorn app.main:app --host 127.0.0.1 --port 8000
```

**Port Binding Error Solution:**
If you get error: `error while attempting to bind on address ('127.0.0.1', 8001): only one usage of each socket address is normally permitted`

This means port 8001 is already in use. Use port 8000 instead or find another available port:

```powershell
# To find which process is using port 8001:
netstat -ano | findstr :8001

# Or use a different port:
uvicorn app.main:app --host 127.0.0.1 --port 8002
```

---

## Testing the API

### Test 1: Access Root Endpoint
```powershell
# In PowerShell:
Invoke-WebRequest -Uri http://localhost:8000 -UseBasicParsing
```

**Expected Response:**
```html
<html><body style='padding: 10px;'><h1>Welcome to the API</h1><div>Check the docs: <a href='/docs'>here</a></div></body></html>
```

### Test 2: Health Check Endpoint
```powershell
Invoke-WebRequest -Uri http://localhost:8000/api/v1/health -UseBasicParsing | Select-Object -ExpandProperty Content
```

**Expected Response:**
```json
{"name":"House Price Prediction API","api_version":"0.0.2","model_version":"3.2.0 (unavailable)"}
```

### Test 3: Interactive API Documentation
Open in browser:
```
http://localhost:8000/docs
```

This opens the Swagger UI where you can test all endpoints interactively.

### Test 4: OpenAPI Schema
```
http://localhost:8000/api/v1/openapi.json
```

---

## API Endpoints

### 1. GET `/`
**Description:** Root endpoint with welcome message

**Response:** HTML content with link to API docs

---

### 2. GET `/api/v1/health`
**Description:** Health check endpoint

**Response:**
```json
{
  "name": "House Price Prediction API",
  "api_version": "0.0.2",
  "model_version": "3.2.0 (unavailable)"
}
```

---

### 3. POST `/api/v1/predict`
**Description:** Make house price predictions

**Request Body:** JSON with house features
```json
{
  "inputs": [
    {
      "MSSubClass": 20,
      "MSZoning": "RH",
      "LotFrontage": 80.0,
      "LotArea": 11622,
      "Street": "Pave",
      "Alley": null,
      "LotShape": "Reg",
      "LandContour": "Lvl",
      "Utilities": "AllPub",
      "LotConfig": "Inside",
      "LandSlope": "Gtl",
      "Neighborhood": "NAmes",
      "Condition1": "Feedr",
      "Condition2": "Norm",
      "BldgType": "1Fam",
      "HouseStyle": "1Story",
      "OverallQual": 5,
      "OverallCond": 6,
      "YearBuilt": 1961,
      "YearRemodAdd": 1961,
      "RoofStyle": "Gable",
      "RoofMatl": "CompShg",
      "Exterior1st": "VinylSd",
      "Exterior2nd": "VinylSd",
      "MasVnrType": "None",
      "MasVnrArea": 0.0,
      "ExterQual": "TA",
      "ExterCond": "TA",
      "Foundation": "CBlock",
      "BsmtQual": "TA",
      "BsmtCond": "TA",
      "BsmtExposure": "No",
      "BsmtFinType1": "Rec",
      "BsmtFinSF1": 468.0,
      "BsmtFinType2": "LwQ",
      "BsmtFinSF2": 144.0,
      "BsmtUnfSF": 270.0,
      "TotalBsmtSF": 882.0,
      "Heating": "GasA",
      "HeatingQC": "TA",
      "CentralAir": "Y",
      "Electrical": "SBrkr",
      "FirstFlrSF": 896,
      "SecondFlrSF": 0,
      "LowQualFinSF": 0,
      "GrLivArea": 896,
      "BsmtFullBath": 0.0,
      "BsmtHalfBath": 0.0,
      "FullBath": 1,
      "HalfBath": 0,
      "BedroomAbvGr": 2,
      "KitchenAbvGr": 1,
      "KitchenQual": "TA",
      "TotRmsAbvGrd": 5,
      "Functional": "Typ",
      "Fireplaces": 0,
      "FireplaceQu": null,
      "GarageType": "Attchd",
      "GarageYrBlt": 1961.0,
      "GarageFinish": "Unf",
      "GarageCars": 1.0,
      "GarageArea": 730.0,
      "GarageQual": "TA",
      "GarageCond": "TA",
      "PavedDrive": "Y",
      "WoodDeckSF": 140,
      "OpenPorchSF": 0,
      "EnclosedPorch": 0,
      "ThreeSsnPortch": 0,
      "ScreenPorch": 120,
      "PoolArea": 0,
      "PoolQC": null,
      "Fence": "MnPrv",
      "MiscFeature": null,
      "MiscVal": 0,
      "MoSold": 6,
      "YrSold": 2010,
      "SaleType": "WD",
      "SaleCondition": "Normal"
    }
  ]
}
```

**Response (When Model Not Available - Current Status):**
```json
{
  "detail": "Regression model is not available. Please install tid-regression-model package."
}
```
Status Code: `503 Service Unavailable`

---

## Current Status

✅ **Working:**
- FastAPI server starts successfully
- Root endpoint (`/`) returns welcome HTML
- Health check endpoint (`/api/v1/health`) works correctly
- Interactive API docs (Swagger UI) at `/docs`
- API request validation using Pydantic schemas
- CORS middleware configured

❌ **Not Working (Intentional - Missing Dependency):**
- Predict endpoint returns 503 error because `tid-regression-model` is not installed
- This is due to missing C++ compiler for building numpy from source

---

## Troubleshooting

### Issue 1: "ModuleNotFoundError: No module named 'app'"
**Solution:** Make sure you're running from the correct directory:
```powershell
cd "C:\Users\leona\OneDrive\SENECA\COURSE-FASTAPI\mldeploy-projects\deploying-machine-learning-models\section-06-model-serving-api\house-prices-api"
```

### Issue 2: "Port already in use" Error
**Solution:** Use a different port:
```powershell
uvicorn app.main:app --host 127.0.0.1 --port 8002
```

Or kill the process using the port:
```powershell
# Find the process ID using port 8001
netstat -ano | findstr :8001

# Kill the process (replace PID with the actual process ID)
taskkill /PID <PID> /F
```

### Issue 3: "pydantic.errors.PydanticImportError: BaseSettings has been moved"
**Solution:** Install pydantic-settings:
```powershell
pip install pydantic-settings
```

### Issue 4: Predict Endpoint Returns 503 Error
**Expected Behavior:** This is intentional. To enable predictions, you need:

1. Install Microsoft Visual Studio Build Tools (for C++ compiler)
2. Then install:
```powershell
pip install "tid-regression-model>=3.2.0" "feature-engine>=1.0.2,<1.6.0"
```

3. Revert the changes to `app/api.py` and `app/schemas/predict.py` to remove the fallback code

---

## Summary of Commands

### Quick Setup (All in One)
```powershell
# Navigate to project directory
cd "C:\Users\leona\OneDrive\SENECA\COURSE-FASTAPI\mldeploy-projects\deploying-machine-learning-models\section-06-model-serving-api\house-prices-api"

# Upgrade pip, setuptools, wheel
python -m pip install --upgrade pip setuptools wheel

# Install core dependencies
pip install uvicorn fastapi python-multipart pydantic loguru --upgrade

# Install pydantic-settings for Pydantic v2
pip install pydantic-settings

# Optional: Install data science packages
pip install numpy pandas scikit-learn scipy

# Start the server
python -c "import sys; sys.path.insert(0, '.'); from app.main import app; import uvicorn; uvicorn.run(app, host='127.0.0.1', port=8000, log_level='info')"
```

### Access the API
- **Web Browser:** http://localhost:8000/docs
- **Health Check:** http://localhost:8000/api/v1/health
- **Root:** http://localhost:8000/

---

## Files Modified

1. **app/config.py** - Updated Pydantic import
2. **app/api.py** - Added regression model availability check
3. **app/schemas/predict.py** - Added fallback schema

---

## Project Structure
```
house-prices-api/
├── app/
│   ├── __init__.py
│   ├── api.py (MODIFIED)
│   ├── config.py (MODIFIED)
│   ├── main.py
│   └── schemas/
│       ├── __init__.py
│       ├── health.py
│       └── predict.py (MODIFIED)
├── tests/
│   ├── __init__.py
│   ├── conftest.py
│   └── test_api.py
├── requirements.txt
├── test_requirements.txt
├── Procfile
├── tox.ini
├── mypy.ini
├── typing_requirements.txt
└── SETUP_GUIDE.md (THIS FILE)
```

---

## Additional Resources

- FastAPI Documentation: https://fastapi.tiangolo.com/
- Pydantic v2 Migration Guide: https://docs.pydantic.dev/2.0/migration/
- Uvicorn Documentation: https://www.uvicorn.org/
- Python Package Index (PyPI): https://pypi.org/

---

## Notes

- The API uses Pydantic v2 (latest version), not v1
- All changes maintain backward compatibility with the original API design
- The fallback mechanisms allow the API to run without the full ML model installed
- CORS is configured to accept requests from localhost:3000, localhost:8000, etc.

---

**Last Updated:** April 18, 2026
**Status:** ✅ Running Successfully

