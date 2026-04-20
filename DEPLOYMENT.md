# Deployment Guide: Railway with CircleCI and Gemfury

This guide covers deploying the House Prices API to Railway using CircleCI for CI/CD and Gemfury for private package hosting.

## Prerequisites

1. **Railway Account**: Create an account at [railway.app](https://railway.app)
2. **CircleCI Account**: Connected to your GitHub repository
3. **Gemfury Account**: For hosting private packages (tid-regression-model)
4. **GitHub Repository**: Connected to CircleCI

## Setup Steps

### 1. CircleCI Environment Variables

Add these environment variables to your CircleCI project settings:

```
GEMFURY_TOKEN=<your-gemfury-token>
PIP_EXTRA_INDEX_URL=https://<gemfury-username>:<gemfury-token>@gem.fury.io/< gemfury-username>/
REGISTRY_HOST=registry.fly.io
RAILWAY_PROJECT_ID=<your-railway-project-id>
RAILWAY_API_TOKEN=<your-railway-api-token>
```

### 2. Railway Setup

#### Option A: Using railway.json (Simple)
```bash
cd section-08-deploying-with-containers/house-prices-api
railway init
```

#### Option B: Using railway.toml (Recommended)
Railway will automatically detect `railway.toml` at the root of your repository.

#### Option C: Using CLI
```bash
railway login
railway create-project house-prices-api
railway create-service api --dockerfile section-08-deploying-with-containers/Dockerfile
railway up
```

### 3. Configure Environment Variables in Railway

In Railway Dashboard, set these environment variables:

```
PYTHONUNBUFFERED=1
PIP_EXTRA_INDEX_URL=https://<gemfury-username>:<gemfury-token>@gem.fury.io/<gemfury-username>/
PROJECT_NAME=House Prices API
API_V1_STR=/api/v1
BACKEND_CORS_ORIGINS=["https://your-domain.railway.app"]
LOGGING_LEVEL=INFO
PORT=8001
```

### 4. Dockerfile Configuration

The Dockerfile is already configured to:
- Build with Python 3.11
- Install packages from both PyPI and Gemfury (using `PIP_EXTRA_INDEX_URL`)
- Run the app as a non-root user for security
- Expose port 8001

### 5. CircleCI Workflow

The CircleCI pipeline will:
1. **Build and Test**: Run tests on every push
2. **Push Image**: Build and push Docker image to registry
3. **Deploy to Railway**: Deploy to Railway on main branch only

Trigger workflows by pushing to the `main` branch.

## Deployment Process

### Automatic Deployment (Recommended)
Push to main branch → CircleCI builds/tests → Deploys to Railway

```bash
git push origin main
```

### Manual Deployment
```bash
railway login
railway link <project-id>
railway up --service api
```

## Testing the Deployment

```bash
# Get the Railway app URL
railway open

# Test the API
curl https://your-railway-app.railway.app/
curl https://your-railway-app.railway.app/api/v1/docs

# Test prediction endpoint
curl -X POST https://your-railway-app.railway.app/api/v1/predictions/predict \
  -H "Content-Type: application/json" \
  -d @request.json
```

## Troubleshooting

### Build Failures
- Check CircleCI logs for test failures
- Verify `PIP_EXTRA_INDEX_URL` is correctly set for Gemfury
- Ensure all requirements are specified in `requirements.txt`

### Runtime Errors
- Check Railway logs: `railway logs`
- Verify environment variables are set in Railway dashboard
- Ensure the model package (tid-regression-model) is available on Gemfury

### Port Issues
- Railway automatically assigns a port via `$PORT` environment variable
- The Procfile and run.sh scripts should use `$PORT`
- The API listens on port 8001 by default

## Security Considerations

1. **Non-root User**: API runs as `ml-api-user`
2. **Environment Variables**: Keep Gemfury token in CircleCI secrets
3. **CORS Configuration**: Update `BACKEND_CORS_ORIGINS` for your domain
4. **Health Checks**: Railway monitors `/` endpoint for service health

## Monitoring and Logs

### CircleCI
- View build logs at: `https://app.circleci.com/`

### Railway
- View logs: `railway logs`
- Monitor metrics in Railway dashboard
- Set up alerts for deployment failures

## File Structure

```
.
├── .circleci/
│   └── config.yml                    # CircleCI pipeline
├── .railway/
│   └── config.json                   # Railway service config
├── railway.toml                       # Railway deployment config
├── railway.json                       # Alternative Railway config
├── section-08-deploying-with-containers/
│   ├── Dockerfile                     # Container image
│   ├── .dockerignore                  # Docker build excludes
│   └── house-prices-api/
│       ├── railway.json               # API service config
│       ├── .env.example               # Environment template
│       ├── requirements.txt            # Python dependencies
│       ├── Procfile                   # Process file for Railway
│       ├── run.sh                     # Startup script
│       └── app/
│           └── main.py                # FastAPI application
└── DEPLOYMENT.md                      # This file
```

## Next Steps

1. ✅ Commit all files to GitHub
2. ✅ Set CircleCI environment variables
3. ✅ Configure Railway project
4. ✅ Push to main branch to trigger deployment
5. ✅ Monitor logs and verify the API is running

For more information, see:
- [Railway Documentation](https://docs.railway.app/)
- [CircleCI Documentation](https://circleci.com/docs/)
- [Gemfury Documentation](https://gemfury.com/help)

