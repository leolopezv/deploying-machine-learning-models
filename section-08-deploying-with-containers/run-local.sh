#!/bin/bash

# Local Testing Script for section-08
# This script builds and tests the Docker container locally

set -e

echo "🐳 Building Docker image locally..."

# Build with build arguments
docker build \
  --build-arg PIP_EXTRA_INDEX_URL="${PIP_EXTRA_INDEX_URL}" \
  -t house-prices-api:local \
  .

echo "✅ Docker image built successfully!"
echo ""
echo "🚀 Running container..."
docker run -it \
  --env PORT=8001 \
  --env PIP_EXTRA_INDEX_URL="${PIP_EXTRA_INDEX_URL}" \
  -p 8001:8001 \
  house-prices-api:local

echo ""
echo "💡 To run in background:"
echo "   docker run -d --name api -p 8001:8001 house-prices-api:local"
echo ""
echo "📋 To view logs:"
echo "   docker logs -f api"
echo ""
echo "🧹 To clean up:"
echo "   docker stop api && docker rm api"

