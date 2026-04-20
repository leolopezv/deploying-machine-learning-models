# Architecture Overview

## System Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────────────┐
│                           YOUR LOCAL MACHINE                             │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                           │
│  ┌──────────────────────┐                                               │
│  │   Your Code Changes  │                                               │
│  │   (git push origin   │                                               │
│  │    main/master)      │                                               │
│  └──────────────┬───────┘                                               │
│                 │                                                        │
└─────────────────┼────────────────────────────────────────────────────────┘
                  │
                  ↓
┌─────────────────────────────────────────────────────────────────────────┐
│                         GITHUB.COM                                       │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                           │
│  ┌───────────────────────────────────────────────────────────────┐      │
│  │  Your Repository (deploying-machine-learning-models)         │      │
│  │                                                               │      │
│  │  📁 section-08-deploying-with-containers/                   │      │
│  │    ├── Dockerfile                                            │      │
│  │    ├── house-prices-api/                                     │      │
│  │    └── .circleci/config.yml                                  │      │
│  │                                                               │      │
│  │  🔔 Webhook triggers on push                                 │      │
│  └──────────────────────┬──────────────────────────────────────┘      │
│                         │                                                │
└─────────────────────────┼────────────────────────────────────────────────┘
                          │
                          ↓
┌─────────────────────────────────────────────────────────────────────────┐
│                      CIRCLECI.COM (CI/CD Pipeline)                      │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                           │
│  ┌──────────────────────────────────────────────────────────────┐       │
│  │  JOB 1: TEST                                                 │       │
│  │  ✓ Checkout code                                             │       │
│  │  ✓ Install dependencies (pytest, requests, etc)             │       │
│  │  ✓ Run pytest                                                │       │
│  │  ✓ Output: Pass/Fail                                         │       │
│  └────────────────────┬─────────────────────────────────────────┘       │
│                       │                                                   │
│                       ↓ (if tests pass)                                 │
│                                                                           │
│  ┌──────────────────────────────────────────────────────────────┐       │
│  │  JOB 2: BUILD & PUSH TO DOCKER HUB                           │       │
│  │  ✓ Build Docker image with PIP_EXTRA_INDEX_URL              │       │
│  │  ✓ Tag: house-prices-api:COMMIT_SHA                         │       │
│  │  ✓ Tag: house-prices-api:latest                             │       │
│  │  ✓ Push to docker.io/YOUR_USERNAME/house-prices-api         │       │
│  └────────────────────┬─────────────────────────────────────────┘       │
│                       │                                                   │
│                       ↓                                                  │
│                                                                           │
│  ┌──────────────────────────────────────────────────────────────┐       │
│  │  JOB 3: PUBLISH TO GEMFURY                                   │       │
│  │  ✓ Build Python package (tid-regression-model)              │       │
│  │  ✓ Push to gemfury.com/YOUR_USERNAME/                       │       │
│  │  ✓ Package available via pip                                │       │
│  └────────────────────┬─────────────────────────────────────────┘       │
│                       │                                                   │
│                       ↓                                                  │
│                                                                           │
│  ┌──────────────────────────────────────────────────────────────┐       │
│  │  JOB 4: DEPLOY TO RAILWAY                                    │       │
│  │  ✓ Trigger Railway deployment                                │       │
│  │  ✓ Pass: Dockerfile path, PIP_EXTRA_INDEX_URL               │       │
│  │  ✓ Railway builds and deploys container                     │       │
│  └────────────────────┬─────────────────────────────────────────┘       │
│                       │                                                   │
└───────────────────────┼────────────────────────────────────────────────────┘
                        │
        ┌───────────────┴─────────────┐
        │                             │
        ↓                             ↓
┌──────────────────────┐    ┌───────────────────────────────┐
│  DOCKER HUB          │    │  GEMFURY                      │
├──────────────────────┤    ├───────────────────────────────┤
│                      │    │                               │
│ Image Registry:      │    │ Package Registry:             │
│ house-prices-api     │    │ tid-regression-model-4.0.5    │
│ └─ latest            │    │ └─ Available via pip          │
│ └─ commit-abc1234    │    │                               │
│                      │    │ URL:                          │
│ Public, pulls from:  │    │ https://push.fury.io/YOUR..../
│ ├─ Docker official   │    │                               │
│ ├─ Gemfury (pip pkg) │    └───────────────────────────────┘
│ └─ Python:3.11       │
│                      │
└──────────────────────┘
        ↑
        │ Docker pulls image
        │
        ↓
┌──────────────────────────────────────────────────────────────┐
│                   RAILWAY.APP                                │
├──────────────────────────────────────────────────────────────┤
│                                                              │
│  ┌───────────────────────────────────────────────────────┐ │
│  │  Service: house-prices-api                            │ │
│  │  ├─ Status: Online ✓                                 │ │
│  │  ├─ Container: Running                               │ │
│  │  ├─ Port: 8001                                       │ │
│  │  ├─ URL: https://house-prices-api-xyz.railway.app   │ │
│  │  ├─ Logs: View in dashboard                          │ │
│  │  ├─ Metrics: CPU, Memory, Requests                   │ │
│  │  └─ Auto-scaling: Enabled                            │ │
│  └──────────────────────┬────────────────────────────────┘ │
│                         │                                    │
│  Environment Variables: │                                    │
│  ├─ PORT=8001           │                                    │
│  └─ PIP_EXTRA_INDEX_URL │                                    │
│                         │                                    │
└─────────────────────────┼────────────────────────────────────┘
                          │
                          ↓
                   ┌───────────────────┐
                   │   YOUR API LIVE   │
                   │  🌍 Public URL   │
                   │   /docs          │
                   │   /api/v1/predict│
                   │   /api/v1/health │
                   └───────────────────┘
```

## Data Flow Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                 DEPLOYMENT WORKFLOW                         │
├─────────────────────────────────────────────────────────────┤

Step 1: Developer Action
┌────────────────────────┐
│ git push origin main   │
└──────────┬─────────────┘
           │
           ↓
Step 2: GitHub Webhook
┌────────────────────────────────────┐
│ GitHub detects push                │
│ Sends webhook to CircleCI         │
└──────────┬─────────────────────────┘
           │
           ↓
Step 3: CircleCI Pipeline Starts
┌────────────────────────────────────┐
│ Checkout code from GitHub          │
│ Read .circleci/config.yml          │
└──────────┬─────────────────────────┘
           │
           ↓
Step 4: Run Tests
┌────────────────────────────────────┐
│ Install test_requirements.txt       │
│ Execute: pytest                    │
│ Result: PASS/FAIL                  │
└──────────┬─────────────────────────┘
           │
           ├─ FAIL: Build stops, email sent
           │
           └─ PASS: Continue
             │
             ↓
Step 5: Build Docker Image
┌────────────────────────────────────┐
│ Execute: docker build              │
│ Pass: PIP_EXTRA_INDEX_URL          │
│ Tag: latest, commit-sha            │
│ Result: Image ready                │
└──────────┬─────────────────────────┘
           │
           ↓
Step 6: Push to Docker Hub
┌────────────────────────────────────┐
│ Login with credentials             │
│ Push: docker push                  │
│ Tags: latest, commit-sha           │
│ Destination: docker.io             │
└──────────┬─────────────────────────┘
           │
           ↓
Step 7: Publish Package to Gemfury
┌────────────────────────────────────┐
│ Build Python package               │
│ Run: fury push                     │
│ Package: tid-regression-model      │
│ Destination: gemfury.com           │
└──────────┬─────────────────────────┘
           │
           ↓
Step 8: Deploy to Railway
┌────────────────────────────────────┐
│ Trigger Railway deployment         │
│ Pass Dockerfile path               │
│ Pass build args (Gemfury URL)      │
│ Railway pulls Docker image         │
│ Railway starts container           │
└──────────┬─────────────────────────┘
           │
           ↓
Step 9: API Live
┌────────────────────────────────────┐
│ Service online and accepting       │
│ requests at public URL             │
│ Health checks passing              │
└────────────────────────────────────┘
```

## Component Interaction Diagram

```
┌──────────────────────────────────────────────────────────────────┐
│                    EXTERNAL SERVICES                             │
├──────────────────────────────────────────────────────────────────┤

  GitHub                  Docker Hub              Gemfury         Railway
  ┌────────┐             ┌──────────┐           ┌────────┐       ┌──────┐
  │ Source │             │ Registry │           │Package │       │Cloud │
  │  Code  │             │ Storage  │           │Storage │       │Run   │
  └────────┘             └──────────┘           └────────┘       └──────┘
     ▲  ▲                    ▲                       ▲              ▲
     │  │                    │                       │              │
     │  └────────┬───────────┼───────────┬───────────┘              │
     │           │           │           │                         │
     │      GET repo      PUSH image   PUSH package                │
     │      PUSH webhook   (docker)     (fury)                     │
     │           │           │           │                         │
     └───────────┴───────────┼───────────┴─────────────────────────┤
                 │           │                                     │
                 └─────────────────────────────────────────────────┘
                             ▲
                             │
                     CircleCI Pipeline
                  (Orchestrates all actions)

---

  Your Local Machine
  ┌──────────────────┐
  │  Your Code       │
  │  Editor/IDE      │
  │  Terminal        │
  └────────┬─────────┘
           │
           │ git push
           ▼
        GitHub ──webhook──▶ CircleCI ──▶ [Build, Test, Deploy]
                                │
                    ┌───────────┼───────────┐
                    ▼           ▼           ▼
               Docker Hub   Gemfury     Railway
                    │           │           │
                    └───────────┼───────────┘
                                ▼
                           Your API Live!
```

## Configuration Files Overview

```
deploying-machine-learning-models/
│
├── .circleci/
│   └── config.yml                          ← CircleCI pipeline definition
│       ├── Defines 5 jobs (test, build, push, publish, deploy)
│       ├── Specifies when each job runs
│       ├── Sets up environment variables
│       └── Chains jobs: test → build → push → publish → deploy
│
├── .github/workflows/
│   └── deploy.yml                          ← GitHub Actions alternative
│       ├── Same functionality as CircleCI
│       ├── Uses native GitHub workflow
│       └── Optional backup CI/CD
│
├── section-08-deploying-with-containers/
│   ├── Dockerfile                          ← Container definition
│   │   ├── Base: Python 3.11
│   │   ├── Non-root user (ml-api-user)
│   │   ├── Installs dependencies from pip
│   │   ├── Runs via house-prices-api/run.sh
│   │   └── Exposes port 8001
│   │
│   ├── house-prices-api/
│   │   ├── requirements.txt                ← pip dependencies
│   │   │   ├── fastapi, uvicorn
│   │   │   ├── --extra-index-url (Gemfury)
│   │   │   └── tid-regression-model (from Gemfury)
│   │   │
│   │   ├── run.sh                          ← Startup command
│   │   │   └── uvicorn app.main:app --port $PORT
│   │   │
│   │   └── app/
│   │       ├── main.py                     ← FastAPI app
│   │       ├── api.py                      ← Routes
│   │       └── schemas/                    ← Input/output models
│   │
│   └── .circleci/
│       └── config.yml                      ← This project's CI/CD
│
├── .env.example                            ← Environment variables template
├── DEPLOYMENT_SETUP.md                     ← Comprehensive guide
├── IMPLEMENTATION_STEPS.md                 ← Step-by-step walkthrough
├── SETUP_SUMMARY.md                        ← Quick overview
├── QUICK_REFERENCE.md                      ← Commands & troubleshooting
└── ARCHITECTURE_OVERVIEW.md                ← This file
```

## Service Responsibilities

```
┌─────────────┐
│   GitHub    │ ← Version control, webhooks
└─────────────┘
       │
       └─ Stores: Source code, config files
       └─ Triggers: Webhooks on push
       └─ Provides: Read access to CircleCI

┌─────────────┐
│  CircleCI   │ ← CI/CD orchestration
└─────────────┘
       │
       ├─ Tests: Runs pytest
       ├─ Builds: Docker image
       ├─ Publishes: To Docker Hub & Gemfury
       └─ Deploys: Triggers Railway

┌─────────────┐
│ Docker Hub  │ ← Container image registry
└─────────────┘
       │
       ├─ Stores: Docker images
       └─ Serves: To Railway for deployment

┌─────────────┐
│  Gemfury    │ ← Python package repository
└─────────────┘
       │
       ├─ Stores: tid-regression-model package
       └─ Serves: To Docker during build

┌─────────────┐
│  Railway    │ ← Application hosting
└─────────────┘
       │
       ├─ Pulls: Docker image from Docker Hub
       ├─ Builds: Docker image on their servers
       ├─ Runs: Container with your API
       ├─ Exposes: Public URL
       ├─ Monitors: Logs, metrics, health
       └─ Scales: Auto-scales based on traffic
```

## Network Flow

```
Internet User
    │
    ├─ https://your-railway-url
    │   (Domain managed by Railway)
    │
    ↓
Railway Load Balancer
    │
    ├─ Routes to running container
    │
    ↓
Your API Container (8001)
    │
    ├─ GET / (Hello endpoint)
    ├─ GET /docs (Swagger UI)
    ├─ GET /api/v1/docs (API docs)
    ├─ POST /api/v1/predict (ML prediction)
    └─ GET /health (Health check)
    │
    ├─ Uses: Loaded from pip
    │   └─ tid-regression-model (from Gemfury)
    │
    └─ Returns: JSON response
```

## Timeline for New Deployment

```
Time  Event                       Status          Where
────────────────────────────────────────────────────────
0:00  git push origin main        ✓ Pushed        GitHub
      GitHub sends webhook
      
0:05  CircleCI receives webhook   ✓ Received      CircleCI
      Checks out code
      Installs dependencies
      
0:10  Tests run                   ✓ Pass/Fail     CircleCI
      If FAIL: Build stops
      If PASS: Continue to build
      
0:15  Docker image builds         ⏳ In progress  CircleCI
      Downloads base image
      Installs Python packages
      
0:20  Docker image ready          ✓ Built         CircleCI
      
0:25  Push to Docker Hub          ⏳ In progress  Docker Hub
      Uploads image                                 CircleCI
      
0:30  Image on Docker Hub         ✓ Uploaded      Docker Hub
      Publish to Gemfury starts   ⏳ In progress  Gemfury
      
0:35  Package published           ✓ Published     Gemfury
      Deploy to Railway starts    ⏳ In progress  Railway
      
0:40  Railway pulls Docker image  ⏳ Pulling       Railway
      
0:45  Railway builds container    ⏳ Building      Railway
      
0:50  Container starts            ⏳ Starting      Railway
      Health checks run
      
1:00  API goes live               ✓ Online        Railway
      Public URL accessible
```

---

**Note:** This is a visual overview. Actual times may vary based on:
- Docker image size
- Network speed
- Railway queue
- Gemfury package size

Typical total time: **8-12 minutes**

