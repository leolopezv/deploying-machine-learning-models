# Quick Reference Guide - CI/CD Pipeline

## 🚀 Quick Start

### 1. Initial Setup (One-time)

```bash
# Clone the repo
git clone https://github.com/YOUR_USERNAME/deploying-machine-learning-models.git
cd deploying-machine-learning-models

# Create and push main/master branch
git checkout -b main
git push -u origin main
```

### 2. Set Up Each Service

**Docker Hub**
- Sign up: https://hub.docker.com
- Generate token: Account Settings → Security → New Access Token
- Add to CircleCI/GitHub Actions:
  - `DOCKER_USERNAME` = your username
  - `DOCKER_PASSWORD` = your access token

**Gemfury**
- Sign up: https://gemfury.com
- Get credentials: Dashboard → Account Settings
- Publish package:
  ```bash
  gem install gemfury
  cd section-05-production-model-package
  python -m build
  fury push dist/*.whl --as=YOUR_USERNAME
  ```
- Add to CircleCI/GitHub Actions:
  - `PIP_EXTRA_INDEX_URL` = `https://TOKEN@push.fury.io/USERNAME/`
  - `GEMFURY_USERNAME` = your username
  - `GEMFURY_TOKEN` = your API token

**Railway**
- Sign up: https://railway.app
- Generate token: Dashboard → Profile → Account Settings → API Token
- Add to CircleCI/GitHub Actions:
  - `RAILWAY_TOKEN` = your token
- Set environment variables in Railway:
  - `PORT` = 8001
  - `PIP_EXTRA_INDEX_URL` = your Gemfury URL

**CircleCI**
- Sign up: https://circleci.com
- Link GitHub repo
- Go to Project Settings → Environment Variables
- Add all credentials above

### 3. Deploy

```bash
# Simple push to trigger pipeline
echo "# Updated" >> README.md
git add README.md
git commit -m "Trigger deployment"
git push origin main
```

## 📊 Pipeline Status

| Location | Purpose | URL |
|----------|---------|-----|
| **CircleCI** | Watch builds | https://circleci.com/dashboard |
| **Docker Hub** | View images | https://hub.docker.com/r/YOUR_USERNAME/house-prices-api |
| **Gemfury** | View packages | https://gemfury.com/me/dashboard |
| **Railway** | Access deployed API | https://railway.app/dashboard |

## 🔄 Workflow

```
Your Change
    ↓
Push to main/master
    ↓
CircleCI Triggered
    ├─ Run Tests
    ├─ Build Docker Image
    ├─ Push to Docker Hub
    ├─ Publish Package to Gemfury
    └─ Deploy to Railway
    ↓
API Live (Check Railway Logs)
```

## 🐛 Troubleshooting

### Tests Failing?
```bash
cd section-08-deploying-with-containers/house-prices-api
pip install -r test_requirements.txt
pytest -v
```

### Docker Build Failing?
```bash
cd section-08-deploying-with-containers
docker build --build-arg PIP_EXTRA_INDEX_URL='https://TOKEN@push.fury.io/USERNAME/' -t test .
docker run -it test /bin/bash
```

### Package Not Found?
```bash
# Check Gemfury
fury list --as=YOUR_USERNAME

# Re-publish
cd section-05-production-model-package
python -m build
fury push dist/*.whl --as=YOUR_USERNAME
```

### Railway Deployment Failed?
1. Check Railway logs: Dashboard → Logs
2. Verify environment variables set
3. Test Docker locally: `docker run -p 8001:8001 IMAGE`

## 📝 Common Commands

```bash
# Test locally
cd section-08-deploying-with-containers/house-prices-api
pytest

# Build Docker image
cd section-08-deploying-with-containers
docker build --build-arg PIP_EXTRA_INDEX_URL='...' -t house-prices-api .

# Run Docker image
docker run -p 8001:8001 house-prices-api

# Test API
curl http://localhost:8001/docs

# Deploy manually (requires all env vars set)
./deploy.sh all
```

## 🔐 Security Checklist

- [ ] Added `.env` to `.gitignore`
- [ ] Set environment variables in CircleCI/GitHub Actions (not in code)
- [ ] Used access tokens, not passwords
- [ ] Enabled private repository if needed
- [ ] Reviewed Docker image for secrets
- [ ] Checked Railway logs for exposed credentials

## 📖 Full Documentation

For detailed setup instructions, see: `DEPLOYMENT_SETUP.md`

## 💡 Tips

1. **Test before committing:**
   ```bash
   pytest
   docker build -t test .
   ```

2. **Use feature branches:**
   ```bash
   git checkout -b feature/my-improvement
   # ... make changes ...
   git push -u origin feature/my-improvement
   # Create pull request on GitHub
   ```

3. **Check CircleCI before merging:**
   - All tests must pass
   - Build must succeed
   - All checks must be green

4. **Monitor in production:**
   - Watch Railway logs: Dashboard → Logs
   - Check API health: `/api/v1/docs`
   - Monitor CPU/Memory: Railway → Metrics

## 🚨 Emergency: Rollback

If something goes wrong in production:

```bash
# Option 1: Redeploy previous working version
git revert HEAD
git push origin main

# Option 2: Manually rollback in Railway
# Railway Dashboard → Previous Deployment → Redeploy
```

---

**Need help?** See DEPLOYMENT_SETUP.md for full documentation.

