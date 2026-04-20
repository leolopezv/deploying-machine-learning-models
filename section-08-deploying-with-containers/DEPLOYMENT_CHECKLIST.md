# Deployment Checklist

Complete this checklist to successfully deploy to Railway using CircleCI and Gemfury.

## Pre-Deployment Setup

### Accounts & Access
- [ ] GitHub account with repository access
- [ ] CircleCI account (https://circleci.com)
- [ ] Railway account (https://railway.app)
- [ ] Gemfury account (https://gemfury.com)

### Get Credentials
- [ ] Gemfury username and push token
- [ ] Railway project ID
- [ ] Railway API token
- [ ] CircleCI personal API token (if needed)

## CircleCI Configuration

### Project Setup
- [ ] Visit https://app.circleci.com/
- [ ] Connect to GitHub repository (if not already connected)
- [ ] Select this project

### Environment Variables
Add these variables in CircleCI project settings:

```
GEMFURY_TOKEN            = <your-gemfury-push-token>
GEMFURY_USERNAME         = <your-gemfury-username>
PIP_EXTRA_INDEX_URL      = https://<username>:<token>@gem.fury.io/<username>/
RAILWAY_PROJECT_ID       = <your-railway-project-id>
RAILWAY_API_TOKEN        = <your-railway-api-token>
```

Steps to add:
1. Go to Project Settings
2. Click Environment Variables
3. Click "Add Environment Variable"
4. Add each variable

- [ ] GEMFURY_TOKEN set
- [ ] GEMFURY_USERNAME set
- [ ] PIP_EXTRA_INDEX_URL set
- [ ] RAILWAY_PROJECT_ID set
- [ ] RAILWAY_API_TOKEN set

## Railway Configuration

### Project Setup
- [ ] Create new project on Railway
- [ ] Note the project ID
- [ ] Create a new service (docker)

### Environment Variables
Set in Railway dashboard (Project > Variables):

```
PYTHONUNBUFFERED     = 1
PIP_EXTRA_INDEX_URL  = https://<username>:<token>@gem.fury.io/<username>/
PROJECT_NAME         = House Prices API
API_V1_STR           = /api/v1
BACKEND_CORS_ORIGINS = ["https://your-railway-domain.railway.app"]
LOGGING_LEVEL        = INFO
PORT                 = 8001
```

- [ ] PYTHONUNBUFFERED set to 1
- [ ] PIP_EXTRA_INDEX_URL set (same as CircleCI)
- [ ] PROJECT_NAME set
- [ ] API_V1_STR set
- [ ] BACKEND_CORS_ORIGINS configured
- [ ] LOGGING_LEVEL set
- [ ] PORT set to 8001

### Configure Dockerfile
- [ ] Dockerfile exists in section-08-deploying-with-containers/
- [ ] .dockerignore exists in section-08-deploying-with-containers/

## Code Review

### Files Verified
- [ ] Dockerfile syntax is correct
- [ ] requirements.txt includes all dependencies
- [ ] test_requirements.txt exists and complete
- [ ] tox.ini configured with PIP_EXTRA_INDEX_URL in passenv
- [ ] run.sh script is executable
- [ ] app/main.py is configured correctly

### Configuration Files
- [ ] .circleci/config.yml updated with section-08 jobs
- [ ] railway.json exists in root
- [ ] railway.json exists in section-08-deploying-with-containers/house-prices-api/
- [ ] railway.toml exists in root

### Documentation
- [ ] README.md created in section-08
- [ ] SETUP_INSTRUCTIONS.md created
- [ ] .env.template created
- [ ] .env.example created

## Local Testing (Optional but Recommended)

### Docker Build Test
```bash
cd section-08-deploying-with-containers
export PIP_EXTRA_INDEX_URL="https://<username>:<token>@gem.fury.io/<username>/"
docker build --build-arg PIP_EXTRA_INDEX_URL=$PIP_EXTRA_INDEX_URL -t test:local .
```

- [ ] Docker build succeeds
- [ ] No dependency errors
- [ ] Image builds in reasonable time

### Application Tests
```bash
cd section-08-deploying-with-containers/house-prices-api
tox
```

- [ ] All tests pass
- [ ] Type checks pass
- [ ] Lint checks pass

## Deployment

### Initial Deployment
1. **Commit and push**:
   ```bash
   git add .
   git commit -m "Configure Railway deployment with CircleCI"
   git push origin master
   ```
   - [ ] Code pushed to master branch

2. **Monitor CircleCI**:
   - [ ] Visit https://app.circleci.com/
   - [ ] Watch the pipeline execute
   - [ ] `section_08_test_app_and_container` job completes
   - [ ] `section_08_deploy_app_container_via_railway` job completes
   - [ ] All jobs pass (green checkmark)

3. **Monitor Railway**:
   - [ ] Visit https://railway.app/
   - [ ] Navigate to your project
   - [ ] Watch deployment progress
   - [ ] Service shows as running (green status)

### Verify Deployment

In Railway dashboard:
- [ ] Service status is "Running"
- [ ] Port 8001 is exposed
- [ ] Environment variables are set correctly

Test the API:
```bash
# Get your Railway domain URL first from Railway dashboard
RAILWAY_URL="https://your-domain.railway.app"

# Test root endpoint
curl $RAILWAY_URL/

# Test API health
curl $RAILWAY_URL/api/v1/

# Test OpenAPI docs
curl $RAILWAY_URL/api/v1/docs
```

- [ ] Root endpoint responds with HTML
- [ ] API responds to requests
- [ ] OpenAPI docs are accessible
- [ ] No 500 errors in response

## Monitoring & Maintenance

### Setup Monitoring
- [ ] Enable log streaming in Railway
- [ ] Check logs: `railway logs` (if CLI installed)
- [ ] Set up alerts for errors

### Regular Checks
- [ ] Monitor CircleCI pipeline status
- [ ] Review Railway logs periodically
- [ ] Check error rates
- [ ] Monitor response times

### Security Checklist
- [ ] No .env files committed to git
- [ ] All secrets in CircleCI/Railway only
- [ ] CORS origins set to actual domain
- [ ] Tokens rotated if needed
- [ ] 2FA enabled on all accounts

## Post-Deployment

### Documentation
- [ ] Create deployment runbook
- [ ] Document custom domain setup (if applicable)
- [ ] Document scaling procedures
- [ ] Document rollback procedures

### Team Communication
- [ ] Inform team of deployment
- [ ] Share Railway dashboard access
- [ ] Share CircleCI pipeline access
- [ ] Document the deployment process

## Troubleshooting

If deployment fails:

1. **Check CircleCI logs**
   - [ ] Visit https://app.circleci.com/
   - [ ] Click on failed job
   - [ ] Read error messages
   - [ ] Look for PIP_EXTRA_INDEX_URL issues

2. **Check Railway logs**
   - [ ] Visit https://railway.app/
   - [ ] Navigate to service
   - [ ] Click on Logs tab
   - [ ] Look for startup errors

3. **Common Issues**
   - [ ] Verify environment variables in CircleCI
   - [ ] Verify environment variables in Railway
   - [ ] Verify Gemfury token is correct
   - [ ] Verify Railway API token is correct
   - [ ] Verify repository branch is master or demo

4. **Get Help**
   - [ ] Review README.md
   - [ ] Review SETUP_INSTRUCTIONS.md
   - [ ] Check CircleCI documentation
   - [ ] Check Railway documentation
   - [ ] Check Gemfury documentation

## Success Criteria

✅ **Deployment is successful when**:
- [ ] CircleCI pipeline runs successfully on every push
- [ ] Tests pass automatically
- [ ] Docker image builds without errors
- [ ] Railway deployment completes without errors
- [ ] API responds to HTTP requests
- [ ] API documentation is accessible at /api/v1/docs
- [ ] Logs show no errors
- [ ] Service is marked as running in Railway

---

**Status**: Ready for Deployment
**Last Updated**: 2026-04-19
**Estimated Time**: 30-60 minutes to complete

