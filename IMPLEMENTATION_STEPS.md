# Step-by-Step Implementation Guide

## Overview
This guide walks you through the **exact steps** to set up your CI/CD pipeline. Follow them in order.

---

## Phase 1: Initial Repository Setup (15 minutes)

### Step 1.1: Initialize Git (if not already done)
```bash
cd C:\Users\leona\OneDrive\SENECA\COURSE-FASTAPI\mldeploy-projects\deploying-machine-learning-models

# Initialize git
git init

# Add all files
git add .

# Create initial commit
git commit -m "Initial commit: ML Model Deployment Pipeline"
```

### Step 1.2: Create GitHub Repository
1. Go to https://github.com/new
2. Repository name: `deploying-machine-learning-models`
3. Description: `Machine Learning Model Deployment with FastAPI`
4. Click "Create repository"

### Step 1.3: Push to GitHub
```bash
# Copy the HTTPS URL from GitHub repository page
# Then run:

git remote add origin https://github.com/YOUR_USERNAME/deploying-machine-learning-models.git
git branch -M main
git push -u origin main
```

✅ **Checkpoint:** Your code is now on GitHub!

---

## Phase 2: Docker Hub Setup (10 minutes)

### Step 2.1: Create Docker Hub Account
1. Go to https://hub.docker.com
2. Click "Sign up"
3. Fill in details (use your GitHub username for simplicity)
4. Verify email address

### Step 2.2: Create Access Token
1. Log into Docker Hub
2. Click your profile icon → Account Settings
3. Go to "Security" tab
4. Click "New Access Token"
5. Name it: `circleci-deployment`
6. Copy the token and save it somewhere safe
   ```
   Token: [SAVE THIS]
   ```

✅ **Checkpoint:** You have Docker credentials ready!

---

## Phase 3: Gemfury Setup (15 minutes)

### Step 3.1: Create Gemfury Account
1. Go to https://gemfury.com
2. Sign up
3. Verify email

### Step 3.2: Get Gemfury Credentials
1. Log into Gemfury
2. Click "Dashboard"
3. Copy your API Token and username
   ```
   Username: [SAVE THIS]
   API Token: [SAVE THIS]
   ```

### Step 3.3: Build and Publish Model Package
```bash
# Navigate to model package
cd section-05-production-model-package

# Ensure build tools are installed
pip install --upgrade pip
pip install build twine

# Build the package
python -m build

# Install gemfury CLI
pip install gemfury  # or gem install gemfury

# Publish to Gemfury
# 1. Build your wheel
# 2.Go to Gemfury dashboard
# 3.Upload the .whl file manually
```

**Expected output:**
```
Uploading tid-regression-model-4.0.5-py3-none-any.whl...
Successfully uploaded package
```

### Step 3.4: Get Your Gemfury URL
```
PIP_EXTRA_INDEX_URL: https://YOUR_TOKEN@push.fury.io/YOUR_USERNAME/
```

Save this - you'll need it in CircleCI!

✅ **Checkpoint:** Your model package is on Gemfury!

---

## Phase 4: Railway Setup (15 minutes)

### Step 4.1: Create Railway Account
1. Go to https://railway.app
2. Sign up (recommend using GitHub)
3. Authorize Railway to access your GitHub account
4. Verify email if needed

### Step 4.2: Create New Project
1. Go to https://railway.app/dashboard
2. Click "New Project"
3. Select "Dockerfile" deployment
4. Configure:
   - Service name: `house-prices-api`
   - GitHub repo: Select your repo
   - Dockerfile path: `section-08-deploying-with-containers/Dockerfile`

### Step 4.3: Generate API Token
1. Click your profile icon (bottom left)
2. Go to "Account Settings"
3. Click "API Tokens"
4. Click "Generate Token"
5. Copy the token
   ```
   RAILWAY_TOKEN: [SAVE THIS]
   ```

### Step 4.4: Set Environment Variables in Railway
1. In Railway dashboard, click your project
2. Click the service "house-prices-api"
3. Go to "Variables" tab
4. Add:
   ```
   PORT=8001
   PIP_EXTRA_INDEX_URL=https://YOUR_TOKEN@push.fury.io/YOUR_USERNAME/
   ```
5. Click "Save"

✅ **Checkpoint:** Railway is configured and ready!

---

## Phase 5: CircleCI Setup (20 minutes)

### Step 5.1: Create CircleCI Account
1. Go to https://circleci.com/signup
2. Click "Sign up with GitHub"
3. Authorize CircleCI
4. Choose "Free" plan

### Step 5.2: Link GitHub Repository
1. Go to https://circleci.com/dashboard
2. Click "Create Project"
3. Find your `deploying-machine-learning-models` repo
4. Click "Set Up Project"
5. Select "Fastest: Use the .circleci/config.yml in my repo"
6. Click "Set Up Project"

CircleCI will find your `.circleci/config.yml` automatically!

### Step 5.3: Add Environment Variables
1. Go to Project Settings (gear icon)
2. Click "Environment Variables"
3. Add each variable:

| Variable | Value | Source |
|----------|-------|--------|
| `DOCKER_USERNAME` | Your Docker Hub username | Docker Hub Profile |
| `DOCKER_PASSWORD` | Your Docker Hub token | Docker Hub → Account Settings → Security |
| `PIP_EXTRA_INDEX_URL` | `https://TOKEN@push.fury.io/USERNAME/` | Gemfury Dashboard |
| `GEMFURY_USERNAME` | Your Gemfury username | Gemfury Dashboard |
| `GEMFURY_TOKEN` | Your Gemfury API token | Gemfury Settings |
| `RAILWAY_TOKEN` | Your Railway token | Railway → Account Settings → API Tokens |

**Add each one:**
1. Click "Add Environment Variable"
2. Enter name in "Name" field
3. Enter value in "Value" field
4. Click "Add Variable"

### Step 5.4: Verify CircleCI Config
Go to CircleCI dashboard. You should see:
- Project name: `deploying-machine-learning-models`
- Status: Ready to build
- `.circleci/config.yml` recognized

✅ **Checkpoint:** All credentials are in CircleCI!

---

## Phase 6: Test the Pipeline (5 minutes)

### Step 6.1: Trigger First Deployment
```bash
# Make a small change
echo "# Pipeline Test" >> README.md

# Commit and push
git add README.md
git commit -m "Test pipeline trigger"
git push origin main
```

### Step 6.2: Watch CircleCI Build
1. Go to https://circleci.com/dashboard
2. Click your project
3. Watch the build progress:
   - **test** job runs first
   - Once tests pass, **build_and_push** starts
   - Then **publish_to_gemfury** runs
   - Finally **deploy_to_railway** executes

Each job typically takes:
- **test**: 2-3 minutes
- **build_and_push**: 3-5 minutes
- **publish_to_gemfury**: 1-2 minutes
- **deploy_to_railway**: 2-3 minutes

**Total: ~10 minutes**

### Step 6.3: Check Railway Deployment
1. Go to https://railway.app/dashboard
2. Click your project
3. Click the `house-prices-api` service
4. Go to "Deployments" tab
5. You should see a new deployment in progress

Wait for status to turn green (✓ Success)

### Step 6.4: Test Your API
Once deployment completes:
1. Go to Railway dashboard
2. Click `house-prices-api`
3. Copy the "Service URL"
4. Visit: `https://[YOUR_URL]/docs`
5. You should see the FastAPI Swagger UI!

Try the `/api/v1/predict` endpoint with test data.

✅ **Checkpoint:** Your API is deployed and working!

---

## Phase 7: Verify Everything (5 minutes)

### Step 7.1: Check All Services

**Docker Hub**
- Visit: https://hub.docker.com/r/YOUR_USERNAME/house-prices-api
- You should see your pushed images

**Gemfury**
- Visit: https://gemfury.com/me/dashboard
- You should see `tid-regression-model` package

**Railway**
- Visit: https://railway.app/dashboard
- Service should show "Online" status

**CircleCI**
- Visit: https://circleci.com/dashboard
- All jobs should show green checkmarks

### Step 7.2: Test API Endpoints
```bash
# Get your Railway URL from dashboard
RAILWAY_URL="https://your-railway-url"

# Test health endpoint
curl $RAILWAY_URL/

# Test API docs
curl $RAILWAY_URL/docs

# Test prediction (replace with real data)
curl -X POST $RAILWAY_URL/api/v1/predict \
  -H "Content-Type: application/json" \
  -d '{
    "Pclass": 1,
    "Sex": "male",
    "Age": 30,
    ...
  }'
```

✅ **Checkpoint:** All services are working together!

---

## Phase 8: Set Up Pull Request Workflow (Optional but Recommended)

### Step 8.1: Protect Master Branch (Optional)
1. Go to your GitHub repo
2. Click "Settings"
3. Click "Branches"
4. Under "Branch protection rules", click "Add rule"
5. Configure:
   - Branch name pattern: `main` (or `master`)
   - Require pull request reviews: ✓
   - Dismiss stale PR reviews: ✓
   - Require status checks to pass: ✓
   - Select `continuous-integration/circleci/build`

Now you can't push directly to main - only through PRs!

### Step 8.2: Use Feature Branches
```bash
# Create feature branch
git checkout -b feature/my-improvement

# Make changes
echo "My changes" >> app/main.py

# Commit and push
git add .
git commit -m "Add my improvement"
git push origin feature/my-improvement
```

Then:
1. Go to GitHub
2. Click "Compare & pull request"
3. Add description
4. Click "Create pull request"
5. CircleCI automatically tests the PR
6. Once tests pass, click "Merge pull request"
7. CircleCI automatically deploys!

---

## Phase 9: Monitor Your Deployment

### Daily Tasks

**Check CircleCI**
- Visit: https://circleci.com/dashboard
- All builds passing? ✓

**Check Railway**
- Visit: https://railway.app/dashboard
- Service online? ✓
- CPU/Memory usage normal? ✓

**Check API Health**
- Visit: `https://your-railway-url/docs`
- Can you see Swagger UI? ✓

**Check Logs**
```bash
# CircleCI logs: Click on job in dashboard
# Railway logs: Dashboard → Service → Logs
# Look for errors or warnings
```

---

## Phase 10: Troubleshooting Common Issues

### Issue 1: "Tests Failing in CircleCI"
**Solution:**
```bash
# Run tests locally to debug
cd section-08-deploying-with-containers/house-prices-api
pip install -r test_requirements.txt
pytest -v

# Fix issues
git add .
git commit -m "Fix test failures"
git push origin main
```

### Issue 2: "Docker Build Failing"
**Solution:**
```bash
# Test locally
cd section-08-deploying-with-containers
docker build \
  --build-arg PIP_EXTRA_INDEX_URL='https://TOKEN@push.fury.io/USERNAME/' \
  -t test .

# Check build logs for errors
# Common: Missing PIP_EXTRA_INDEX_URL in CircleCI env vars
```

### Issue 3: "Package Not Found on Gemfury"
**Solution:**
```bash
# Verify it was published
fury list --as=YOUR_USERNAME

# If not found, re-publish
cd section-05-production-model-package
fury push dist/*.whl --as=YOUR_USERNAME
```

### Issue 4: "Railway Deployment Stuck"
**Solution:**
1. Check Railway logs: Dashboard → Logs
2. Verify PORT=8001 is set
3. Check PIP_EXTRA_INDEX_URL is correct
4. Try manual rollback: Dashboard → Previous Deploy → Redeploy

---

## ✅ Final Checklist

- [ ] GitHub repository created and synced
- [ ] Docker Hub account created with token
- [ ] Model package published to Gemfury
- [ ] Gemfury credentials collected
- [ ] Railway account created with API token
- [ ] CircleCI linked to GitHub
- [ ] All environment variables added to CircleCI
- [ ] First deployment triggered and completed
- [ ] API is accessible on Railway
- [ ] All 4 services working together (GitHub → CircleCI → Docker → Gemfury → Railway)

---

## 🎉 You're Done!

Your CI/CD pipeline is now fully operational. 

**Your workflow is now:**
1. Make changes locally
2. Commit and push to GitHub
3. CircleCI tests automatically
4. On success, deploys automatically to Railway
5. Your API is updated and live!

---

## 📖 Next Steps

- Read `DEPLOYMENT_SETUP.md` for in-depth explanations
- Check `QUICK_REFERENCE.md` for common commands
- Set up branch protection on GitHub (optional)
- Configure monitoring alerts (optional)
- Document your API endpoints (already done with Swagger at `/docs`)

---

**Need help?** See the troubleshooting section or review the detailed docs.

**Questions about a service?** Check the links section in `DEPLOYMENT_SETUP.md`.

