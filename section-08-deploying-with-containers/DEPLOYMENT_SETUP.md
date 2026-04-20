# CI/CD Deployment Pipeline Setup Guide

## Overview

This guide walks you through setting up a complete continuous integration and continuous deployment (CI/CD) pipeline for your ML model API using:

- **CircleCI**: Orchestrates the CI/CD workflow
- **Docker**: Containerizes your application
- **Gemfury**: Hosts your Python packages (model dependencies)
- **Railway**: Hosts and runs your containerized application

## Architecture Flow

```
GitHub Push/PR to Master
         ↓
    CircleCI Triggered
         ↓
  Run Tests (pytest)
         ↓
  Build Docker Image
         ↓
  Push to Docker Hub
         ↓
  Publish Package to Gemfury
         ↓
  Deploy to Railway
         ↓
  API Live (Auto-scaling)
```

## Step 1: GitHub Setup

### 1.1 Create a GitHub Account (if needed)
- Go to https://github.com and sign up

### 1.2 Push Your Repository to GitHub
```bash
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/YOUR_USERNAME/deploying-machine-learning-models.git
git branch -M main
git push -u origin main
```

### 1.3 Create a `master` Branch (Optional)
If you prefer using `master` instead of `main`:
```bash
git checkout -b master
git push -u origin master
```

## Step 2: Docker Setup

### 2.1 Create Docker Hub Account
1. Visit https://hub.docker.com and sign up
2. Verify your email address
3. Create a Docker Hub Access Token:
   - Go to Account Settings → Security
   - Click "New Access Token"
   - Copy the token (you'll need this for CircleCI)

### 2.2 Understand the Dockerfile

Your `Dockerfile` in `section-08-deploying-with-containers/`:
```dockerfile
FROM python:3.11
RUN adduser --disabled-password --gecos '' ml-api-user
WORKDIR /opt/house-prices-api
ARG PIP_EXTRA_INDEX_URL
ADD ./house-prices-api /opt/house-prices-api/
RUN pip install --upgrade pip
RUN pip install -r /opt/house-prices-api/requirements.txt
RUN chmod +x /opt/house-prices-api/run.sh
RUN chown -R ml-api-user:ml-api-user ./
USER ml-api-user
EXPOSE 8001
CMD ["bash", "./run.sh"]
```

**Key Features:**
- Non-root user (`ml-api-user`) for security
- Python 3.11 base image
- `PIP_EXTRA_INDEX_URL` argument for Gemfury packages
- Exposes port 8001 for the API

## Step 3: Gemfury Setup (Python Package Repository)

### 3.1 Create Gemfury Account
1. Visit https://gemfury.com and sign up
2. Choose the free tier
3. Create your repository

### 3.2 Get Your Gemfury Credentials
1. Go to https://gemfury.com/me/dashboard
2. Click "Account Settings"
3. Copy your API Token
4. Note the repository URL format:
   ```
   https://YOUR_TOKEN@push.fury.io/YOUR_USERNAME/
   ```

### 3.3 Publish Your Model Package to Gemfury

First, prepare your package (if not already done):
```bash
cd section-05-production-model-package
python -m build
```

Then push using the Gemfury CLI:
```bash
gem install gemfury
fury push dist/tid_regression_model-4.0.5-py3-none-any.whl --as=YOUR_USERNAME
```

### 3.4 Update requirements.txt

Your `house-prices-api/requirements.txt` should have:
```
--extra-index-url=https://YOUR_TOKEN@push.fury.io/YOUR_USERNAME/

uvicorn>=0.20.0,<0.30.0
fastapi>=0.88.0,<1.0.0
...
tid-regression-model==4.0.5
...
```

The `--extra-index-url` tells pip to look in Gemfury for the `tid-regression-model` package.

## Step 4: CircleCI Setup

### 4.1 Create CircleCI Account
1. Visit https://circleci.com
2. Sign up with your GitHub account
3. Authorize CircleCI to access your GitHub repositories

### 4.2 Set Up Your Project

1. Go to CircleCI Dashboard
2. Click "Create Project"
3. Select your `deploying-machine-learning-models` repository
4. Click "Set Up Project"
5. You can use the existing `.circleci/config.yml` (CircleCI will auto-detect it)

### 4.3 Configure Environment Variables in CircleCI

Navigate to: **Project Settings → Environment Variables**

Add the following variables:

| Variable Name | Value | Source |
|---|---|---|
| `DOCKER_USERNAME` | Your Docker Hub username | Docker Hub Account |
| `DOCKER_PASSWORD` | Your Docker Hub Access Token | Docker Hub Security Settings |
| `PIP_EXTRA_INDEX_URL` | `https://YOUR_TOKEN@push.fury.io/YOUR_USERNAME/` | Gemfury Dashboard |
| `GEMFURY_USERNAME` | Your Gemfury username | Gemfury Dashboard |
| `GEMFURY_TOKEN` | Your Gemfury API token | Gemfury Settings |
| `RAILWAY_TOKEN` | Your Railway API token | Railway Dashboard |

**⚠️ Security Note:** Never commit these credentials to GitHub. CircleCI stores them securely and injects them at runtime.

## Step 5: Railway Setup

### 5.1 Create Railway Account
1. Visit https://railway.app
2. Sign up (recommended: with GitHub)
3. Create a new project

### 5.2 Get Railway API Token
1. Go to https://railway.app/dashboard
2. Click your profile (bottom left)
3. Go to "Account Settings"
4. Click "API Token"
5. Generate a new token and copy it
6. Add it to CircleCI as `RAILWAY_TOKEN`

### 5.3 Create Railway Service
```bash
# Install Railway CLI
npm install -g @railway/cli

# Login to Railway
railway login

# Link to your project
railway link
```

### 5.4 Configure Railway Environment Variables

In Railway Dashboard for your project:
- `PORT`: Set to `8001`
- `PIP_EXTRA_INDEX_URL`: Set to your Gemfury URL
- Any other environment variables your app needs

## Step 6: CircleCI Workflow Explanation

The `.circleci/config.yml` defines this workflow:

### Job 1: **test**
- Runs on every branch
- Installs dependencies
- Runs pytest
- Ensures code quality

### Job 2: **build_and_push**
- Triggered only if `test` passes
- Runs only on `main` or `master` branches
- Builds Docker image with Gemfury credentials
- Tags with commit SHA and `latest`
- Pushes to Docker Hub

### Job 3: **publish_to_gemfury**
- Triggered after `build_and_push`
- Publishes Python package to Gemfury
- Useful if you update the model package

### Job 4: **deploy_to_railway**
- Triggered after `build_and_push`
- Deploys the Docker image to Railway
- Auto-scales based on traffic

## Step 7: Making Your First Deployment

### 7.1 Set Up Git Branches

```bash
# Create main branch
git checkout -b main
git push -u origin main

# Or use master (whichever CircleCI config references)
git checkout -b master
git push -u origin master
```

### 7.2 Make a Change and Push

```bash
# Make any change to your code
echo "# Updated" >> README.md

# Commit and push to main/master
git add .
git commit -m "Update documentation"
git push origin main
```

### 7.3 Watch CircleCI Pipeline

1. Go to CircleCI Dashboard
2. Click your project
3. Watch the pipeline execute:
   - Tests run
   - Docker image builds
   - Image pushes to Docker Hub
   - Package publishes to Gemfury
   - Deployment to Railway starts
4. Check Railway dashboard to see your app go live

## Step 8: Troubleshooting

### 8.1 Docker Build Fails
**Symptom:** "pip: command not found" or "module not found"

**Solution:**
- Check `requirements.txt` is correct
- Verify `PIP_EXTRA_INDEX_URL` environment variable is set in CircleCI
- Ensure Gemfury package is published

```bash
# Test locally
docker build --build-arg PIP_EXTRA_INDEX_URL='https://TOKEN@push.fury.io/USERNAME/' -t test .
docker run -p 8001:8001 test
```

### 8.2 Package Not Found on Gemfury
**Symptom:** "ERROR: Could not find a version that satisfies the requirement tid-regression-model"

**Solution:**
```bash
# Verify package is published
fury list --as=YOUR_USERNAME

# Re-publish if needed
fury push dist/*.whl --as=YOUR_USERNAME
```

### 8.3 Railway Deployment Fails
**Symptom:** "Build failed" or "deployment timeout"

**Solution:**
- Check Railway logs: Railway Dashboard → Logs
- Verify environment variables are set in Railway
- Check Docker image runs locally: `docker run -p 8001:8001 IMAGE_NAME`

### 8.4 Tests Failing in CircleCI
**Symptom:** "pytest exited with code 1"

**Solution:**
```bash
# Run tests locally with same Python version
docker run -it python:3.11 /bin/bash
pip install -r test_requirements.txt
pytest
```

## Step 9: Pull Request Workflow (Recommended)

For a more robust workflow, use feature branches:

```bash
# Create feature branch
git checkout -b feature/my-improvement
git push -u origin feature/my-improvement

# CircleCI automatically tests this branch
# Once tests pass, create a Pull Request on GitHub

# Create PR from feature/my-improvement → main/master
# CircleCI runs tests again

# Once approved, merge the PR
# CircleCI automatically deploys to Railway

# Delete feature branch
git branch -d feature/my-improvement
```

## Step 10: Monitoring and Logs

### CircleCI Logs
- **URL**: https://circleci.com/gh/YOUR_USERNAME/deploying-machine-learning-models
- Shows each job's output
- Useful for debugging failed builds

### Railway Logs
- **URL**: https://railway.app/dashboard
- Click your project → Logs
- Shows application runtime logs
- Useful for debugging runtime errors

### Docker Hub
- **URL**: https://hub.docker.com/repository/docker/YOUR_USERNAME/house-prices-api
- Shows pushed images
- Useful for version tracking

## Step 11: Advanced: Custom Deployment Triggers

To only deploy on version tags:

Edit `.circleci/config.yml`:
```yaml
filters:
  tags:
    only: /^v.*/
  branches:
    ignore: /.*/
```

This way, you can manually trigger deployments:
```bash
git tag v1.0.0
git push origin v1.0.0
```

## Verification Checklist

- [ ] GitHub repository created and pushed
- [ ] Docker Hub account and access token created
- [ ] CircleCI project linked to GitHub repo
- [ ] CircleCI environment variables configured
- [ ] Gemfury account and repository created
- [ ] Model package published to Gemfury
- [ ] Railway account and project created
- [ ] Railway API token added to CircleCI
- [ ] First manual test: Push to main/master branch
- [ ] Watch CircleCI pipeline complete
- [ ] Verify app is live on Railway
- [ ] Test the API endpoint from Railway URL

## Summary

Now your workflow is:

1. **Code Change** → Push to GitHub main/master
2. **Automatic** → CircleCI tests code
3. **Automatic** → Docker image built and pushed
4. **Automatic** → Package published to Gemfury
5. **Automatic** → Application deployed to Railway
6. **Result** → Your API is live and publicly accessible

Any new commit to main/master will automatically rebuild, test, and redeploy your application!

## Support Resources

- **CircleCI Docs**: https://circleci.com/docs/
- **Railway Docs**: https://docs.railway.app/
- **Gemfury Docs**: https://gemfury.com/help/
- **Docker Docs**: https://docs.docker.com/
- **FastAPI Docs**: https://fastapi.tiangolo.com/

---

**Last Updated:** April 2026

