# Section 08: Deploying ML Models with Containers - Complete CI/CD Setup

## Overview

This directory contains everything needed to deploy your machine learning model API using Docker, CircleCI, Gemfury, and Railway. The setup provides **automated continuous integration and deployment** (CI/CD).

## 📋 What's Included

### Configuration Files

- **`.circleci/config.yml`** - CircleCI pipeline definition
  - Automated testing on every push
  - Docker image building and publishing
  - Package publishing to Gemfury
  - Deployment to Railway
  - Runs automatically when you push to GitHub

- **`.dockerignore`** - Excludes unnecessary files from Docker build
  - Reduces image size
  - Improves build speed

- **`Dockerfile`** - Container definition
  - Based on Python 3.11
  - Non-root user for security
  - Installs dependencies from pip and Gemfury
  - Exposes port 8001

### Application Code

- **`house-prices-api/`** - Your FastAPI application
  - `app/main.py` - FastAPI application
  - `app/api.py` - API routes
  - `requirements.txt` - Python dependencies
  - `test_requirements.txt` - Testing dependencies
  - `run.sh` - Container startup script
  - `Procfile` - Heroku/Railway deployment config

### Documentation

- **`DEPLOYMENT_SETUP.md`** - Comprehensive setup guide (11 steps)
  - Service-by-service setup instructions
  - Environment variable configuration
  - Troubleshooting guide
  - Monitoring and logging

- **`README.md`** (this file) - Quick overview

### Root Directory Documentation

From the project root, also check:

- **`IMPLEMENTATION_STEPS.md`** - Step-by-step walkthrough (10 phases)
  - Practical, numbered steps
  - What to do at each stage
  - Checkpoints to verify progress

- **`SETUP_SUMMARY.md`** - Executive summary
  - What's been created
  - How the pipeline works
  - 5-step quick start
  - FAQ section

- **`QUICK_REFERENCE.md`** - Commands and troubleshooting
  - Common commands
  - Workflow examples
  - Emergency procedures

- **`ARCHITECTURE_OVERVIEW.md`** - Visual diagrams
  - System architecture
  - Data flow
  - Component interactions
  - Timeline for deployments

- **`.env.example`** - Environment variables template

---

## 🚀 Quick Start (< 30 minutes)

### 1. Push Code to GitHub
```bash
cd C:\Users\leona\OneDrive\SENECA\COURSE-FASTAPI\mldeploy-projects\deploying-machine-learning-models

git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/YOUR_USERNAME/deploying-machine-learning-models.git
git branch -M main
git push -u origin main
```

### 2. Create Service Accounts (in order)

**Docker Hub** (https://hub.docker.com)
- Create account
- Generate access token
- Save: `DOCKER_USERNAME` and `DOCKER_PASSWORD`

**Gemfury** (https://gemfury.com)
- Create account
- Get API token
- Publish model package:
  ```bash
  cd section-05-production-model-package
  python -m build
  fury push dist/*.whl --as=YOUR_USERNAME
  ```
- Save: `PIP_EXTRA_INDEX_URL`, `GEMFURY_USERNAME`, `GEMFURY_TOKEN`

**Railway** (https://railway.app)
- Create account with GitHub
- Generate API token
- Save: `RAILWAY_TOKEN`

**CircleCI** (https://circleci.com)
- Sign up with GitHub
- Link this repository
- Add environment variables to CircleCI (from above)

### 3. Test the Pipeline
```bash
# Make a small change
echo "# Pipeline Test" >> README.md

# Push to trigger deployment
git add README.md
git commit -m "Test pipeline"
git push origin main
```

Wait ~10 minutes, then check:
- CircleCI dashboard: All jobs should pass (green)
- Railway dashboard: Service should be "Online"
- Your API should be live at Railway URL!

---

## 📊 Pipeline Flow

```
Your Change
    ↓
git push main
    ↓
CircleCI Triggered
    ├─ Test (2-3 min)
    ├─ Build Docker (3-5 min)
    ├─ Push to Docker Hub (2-3 min)
    ├─ Publish to Gemfury (1-2 min)
    └─ Deploy to Railway (2-3 min)
    ↓
API Live! (Total: ~10 minutes)
```

---

## 📁 Project Structure

```
section-08-deploying-with-containers/
│
├── .circleci/
│   └── config.yml                    ← CircleCI pipeline
│
├── .dockerignore                     ← Files to exclude from Docker
├── Dockerfile                        ← Container definition
│
├── house-prices-api/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py                  ← FastAPI app
│   │   ├── api.py                   ← Routes
│   │   ├── config.py                ← Config
│   │   └── schemas/
│   │       └── __init__.py
│   │
│   ├── requirements.txt              ← Dependencies
│   ├── test_requirements.txt         ← Test dependencies
│   ├── typing_requirements.txt       ← Type hints
│   ├── run.sh                        ← Startup script
│   ├── Procfile                      ← Railway config
│   ├── mypy.ini                      ← Type checking
│   └── tox.ini                       ← Testing config
│
├── DEPLOYMENT_SETUP.md               ← Comprehensive guide
└── README.md                         ← This file
```

---

## 🔄 Workflow

### Automated Flow (Default)

1. **Code Change** - Make changes to your API
2. **Git Push** - `git push origin main`
3. **CircleCI Tests** - Automatically runs pytest
4. **Docker Build** - Automatically builds image
5. **Docker Push** - Automatically uploads to Docker Hub
6. **Gemfury Publish** - Automatically publishes package
7. **Railway Deploy** - Automatically deploys on Railway
8. **Live** - Your API is updated!

### Manual Deployment (If Needed)

```bash
cd section-08-deploying-with-containers

# Set environment variables
export DOCKER_USERNAME="..."
export DOCKER_PASSWORD="..."
export PIP_EXTRA_INDEX_URL="..."
export RAILWAY_TOKEN="..."

# Run deployment script
./deploy.sh all
```

---

## 📚 Documentation Guide

**For different needs, read different docs:**

| Document | Best For |
|----------|----------|
| **DEPLOYMENT_SETUP.md** | Complete setup guide, reference guide |
| **IMPLEMENTATION_STEPS.md** | Step-by-step walkthrough, first-time setup |
| **SETUP_SUMMARY.md** | Quick overview, what's been done, FAQs |
| **QUICK_REFERENCE.md** | Commands, examples, troubleshooting |
| **ARCHITECTURE_OVERVIEW.md** | Understanding the system, diagrams |
| **README.md** (this) | Quick overview of this directory |

---

## 🔑 Key Environment Variables

These must be set in **CircleCI Project Settings → Environment Variables**:

```
DOCKER_USERNAME       = Your Docker Hub username
DOCKER_PASSWORD       = Your Docker Hub access token
PIP_EXTRA_INDEX_URL   = https://TOKEN@push.fury.io/USERNAME/
GEMFURY_USERNAME      = Your Gemfury username
GEMFURY_TOKEN         = Your Gemfury API token
RAILWAY_TOKEN         = Your Railway API token
```

**⚠️ Never commit these to GitHub!**

---

## 🧪 Testing Locally

### Run Tests
```bash
cd house-prices-api
pip install -r test_requirements.txt
pytest
```

### Build Docker Image
```bash
cd ..
docker build \
  --build-arg PIP_EXTRA_INDEX_URL='https://TOKEN@push.fury.io/USERNAME/' \
  -t house-prices-api .
```

### Run Docker Container
```bash
docker run -p 8001:8001 house-prices-api

# In another terminal:
curl http://localhost:8001/docs
```

---

## 🐛 Troubleshooting

### Tests Failing?
```bash
cd house-prices-api
pip install -r test_requirements.txt
pytest -v

# Check for import errors or missing dependencies
```

### Docker Build Failing?
- Check `PIP_EXTRA_INDEX_URL` is correct
- Verify Gemfury package is published
- Test locally: `docker build --build-arg ...`

### Deployment Not Triggering?
- Check CircleCI sees your push (Dashboard → Workflows)
- Verify `.circleci/config.yml` exists in repository
- Check CircleCI has access to GitHub repo

### API Not Responding on Railway?
- Check Railway logs: Dashboard → Logs
- Verify PORT=8001 is set
- Check environment variables are configured

---

## 📖 API Documentation

Once deployed, visit:
```
https://your-railway-url/docs
```

This provides interactive API documentation where you can:
- See all endpoints
- View request/response models
- Test endpoints directly
- Download OpenAPI schema

---

## ✅ Deployment Checklist

- [ ] GitHub repository created
- [ ] Code pushed to main/master
- [ ] Docker Hub account created with token
- [ ] Gemfury account created with package published
- [ ] Railway account created with API token
- [ ] CircleCI linked to GitHub repo
- [ ] Environment variables added to CircleCI
- [ ] First deployment triggered
- [ ] Tests pass in CircleCI
- [ ] Docker image pushed to Docker Hub
- [ ] API deployed on Railway
- [ ] API responding to requests

---

## 📖 Complete Documentation

For complete, detailed instructions, see:

### Main Documentation
- **`DEPLOYMENT_SETUP.md`** - Full 11-step setup guide
- **`IMPLEMENTATION_STEPS.md`** - Step-by-step walkthrough
- **`ARCHITECTURE_OVERVIEW.md`** - System diagrams

### Quick References  
- **`SETUP_SUMMARY.md`** - Overview and FAQ
- **`QUICK_REFERENCE.md`** - Commands and troubleshooting

### Configuration
- **`.env.example`** - Environment variable template

---

## 🔗 External Links

- **CircleCI**: https://circleci.com/dashboard
- **GitHub**: https://github.com/your-username/deploying-machine-learning-models
- **Docker Hub**: https://hub.docker.com/r/your-username/house-prices-api
- **Gemfury**: https://gemfury.com/me/dashboard
- **Railway**: https://railway.app/dashboard

---

## 🆘 Support

1. **Check the FAQs** - See `SETUP_SUMMARY.md`
2. **Review troubleshooting** - See `QUICK_REFERENCE.md`
3. **Read detailed guide** - See `DEPLOYMENT_SETUP.md`
4. **Check logs**:
   - CircleCI: Dashboard → Build logs
   - Railway: Dashboard → Logs
   - Docker: Local terminal output

---

## 🎯 Next Steps

1. Follow **IMPLEMENTATION_STEPS.md** for setup
2. Once live, follow **QUICK_REFERENCE.md** for daily operations
3. For deep understanding, read **ARCHITECTURE_OVERVIEW.md**
4. Use **DEPLOYMENT_SETUP.md** as reference for any issues

---

## Summary

This setup provides:
- ✅ Automated testing on every push
- ✅ Automated Docker image building
- ✅ Automated deployment to Railway
- ✅ Package management via Gemfury
- ✅ CI/CD orchestration via CircleCI
- ✅ Public API accessible 24/7
- ✅ Scalable infrastructure
- ✅ Comprehensive monitoring

**Your workflow becomes:** Code → Push → Auto-Deploy ✨

---

**Last Updated:** April 2026
**Version:** 1.0
**Status:** Production Ready

