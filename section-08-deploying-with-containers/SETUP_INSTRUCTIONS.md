# Deployment Setup Instructions

## Quick Start

This guide will help you deploy the House Prices API to Railway using CircleCI for CI/CD automation.

## Prerequisites

- [ ] GitHub account with this repository
- [ ] CircleCI account (connected to GitHub)
- [ ] Railway account (https://railway.app)
- [ ] Gemfury account (https://gemfury.com)

## Step 1: Set Up Gemfury (Private Package Registry)

1. Sign up at https://gemfury.com
2. Get your Gemfury username and token
3. Note these for CircleCI configuration

## Step 2: Configure CircleCI Environment Variables

Go to CircleCI project settings and add:

```
GEMFURY_TOKEN=<your-gemfury-token>
GEMFURY_USERNAME=<your-gemfury-username>
PIP_EXTRA_INDEX_URL=https://<username>:<token>@gem.fury.io/<username>/
RAILWAY_PROJECT_ID=<your-railway-project-id>
RAILWAY_API_TOKEN=<your-railway-api-token>
```

### Getting Gemfury Credentials:
1. Visit https://dashboard.gemfury.com/tokens
2. Create or copy your push token
3. Your username is shown in your Gemfury URL

### Getting Railway Credentials:
1. Create an account at https://railway.app
2. Create a new project
3. Get your project ID from project settings
4. Generate an API token at https://railway.app/account/tokens

## Step 3: Configure Railway

### Option A: Using railroad.toml (Recommended)
The `railway.toml` and `railway.json` files are already configured in the repository.

### Option B: Manual Railway Setup
```bash
railway login
railway create-project house-prices-api
railway create-service api --dockerfile section-08-deploying-with-containers/Dockerfile
```

## Step 4: Set Railway Environment Variables

In the Railway dashboard, go to your project and add these variables:

```
PYTHONUNBUFFERED=1
PIP_EXTRA_INDEX_URL=https://<username>:<token>@gem.fury.io/<username>/
PROJECT_NAME=House Prices API
API_V1_STR=/api/v1
BACKEND_CORS_ORIGINS=["https://your-railway-domain.railway.app"]
LOGGING_LEVEL=INFO
PORT=8001
```

## Step 5: Deployment

### Automatic Deployment (Recommended)
The CircleCI pipeline will automatically:
1. Run tests when you push to any branch
2. Build and deploy to Railway when you push to `master` or `demo` branch

```bash
# Push to trigger deployment
git add .
git commit -m "Deploy to Railway"
git push origin master
```

### Manual Deployment
```bash
cd section-08-deploying-with-containers
railway login
railway link <project-id>
railway up
```

## Step 6: Verify Deployment

```bash
# Get the deployed app URL
railway open

# Test the API
curl https://your-app.railway.app/
curl https://your-app.railway.app/api/v1/docs

# Test predictions
curl -X POST https://your-app.railway.app/api/v1/predictions/predict \
  -H "Content-Type: application/json" \
  -d '{"input": "data"}'
```

## File Structure

```
section-08-deploying-with-containers/
├── Dockerfile                      # Container image definition
├── .dockerignore                   # Files to exclude from Docker build
├── .env.example                    # Environment variables template
├── .env.template                   # Configuration template
├── railway.json                    # Railway config (simple)
├── house-prices-api/
│   ├── railway.json                # API service config
│   ├── .env.example                # API env template
│   ├── requirements.txt             # Python dependencies
│   ├── run.sh                      # Startup script
│   ├── Procfile                    # Heroku/Railway process file
│   └── app/
│       ├── main.py                 # FastAPI app
│       ├── config.py               # Configuration
│       ├── api.py                  # API routes
│       └── schemas/                # Request/response schemas
└── README.md                        # This file
```

## CircleCI Workflow

The CI/CD pipeline includes:

1. **Build & Test** (`section_08_test_app_and_container`)
   - Installs dependencies from Gemfury
   - Runs unit tests using tox
   - Runs on every commit

2. **Deploy** (`section_08_deploy_app_container_via_railway`)
   - Builds Docker image
   - Pushes to Railway
   - Only runs on `master` or `demo` branches
   - Only runs after tests pass

## Troubleshooting

### Build Failures in CircleCI
- Check CircleCI logs for errors
- Verify `PIP_EXTRA_INDEX_URL` is correct
- Ensure Gemfury package is published

### Container Build Failures
- Check Docker build logs: `railway logs --service api`
- Verify Dockerfile path is correct
- Ensure all dependencies are in `requirements.txt`

### Runtime Errors
- Check Railway logs: `railway logs`
- Verify environment variables in Railway dashboard
- Check API health at `/api/v1/health` (if implemented)

### Port Issues
- Railway assigns port dynamically via `$PORT`
- The app defaults to 8001 in Dockerfile
- Ensure `run.sh` uses `$PORT` variable

### Gemfury Issues
- Verify package is published: `pip index versions tid-regression-model --extra-index-url $PIP_EXTRA_INDEX_URL`
- Check Gemfury API token has push permissions
- Ensure token is not expired

## Monitoring

### CircleCI
- View pipeline: https://app.circleci.com/
- Check build logs for each job
- Monitor deployment status

### Railway
- View logs: `railway logs`
- Monitor metrics in dashboard
- Check service health

## Security Best Practices

1. **Never commit `.env` files** - they contain secrets
2. **Use CircleCI secrets** for sensitive variables
3. **Rotate tokens regularly** - Gemfury and Railway API tokens
4. **Use strong passwords** for your accounts
5. **Enable 2FA** on GitHub, CircleCI, Railway, and Gemfury
6. **Review CORS origins** for your domain only

## Next Steps

1. ✅ Sign up for Railway and Gemfury accounts
2. ✅ Generate API tokens
3. ✅ Add environment variables to CircleCI
4. ✅ Configure Railway project
5. ✅ Push to master branch
6. ✅ Monitor CircleCI pipeline
7. ✅ Verify deployment on Railway
8. ✅ Set up domain and SSL

## Additional Resources

- [Railway Documentation](https://docs.railway.app/)
- [CircleCI Documentation](https://circleci.com/docs/)
- [Gemfury Documentation](https://gemfury.com/help)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Docker Documentation](https://docs.docker.com/)

## Support

For issues or questions:
- Check the logs first
- Review this README
- Check CircleCI and Railway documentation
- Open an issue on GitHub

