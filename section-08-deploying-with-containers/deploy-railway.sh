#!/bin/bash

# Railway Deployment Script
# This script deploys the section-08 application to Railway

set -e  # Exit on error

echo "🚀 Starting Railway Deployment..."

# Check if railway CLI is installed
if ! command -v railway &> /dev/null; then
    echo "📦 Installing Railway CLI..."
    npm install -g @railway/cli
fi

# Check for required environment variables
if [ -z "$RAILWAY_API_TOKEN" ]; then
    echo "❌ Error: RAILWAY_API_TOKEN is not set"
    exit 1
fi

if [ -z "$RAILWAY_PROJECT_ID" ]; then
    echo "❌ Error: RAILWAY_PROJECT_ID is not set"
    exit 1
fi

echo "📂 Navigating to section-08 directory..."
cd "$(dirname "$0")"

echo "🔗 Linking to Railway project..."
railway link "$RAILWAY_PROJECT_ID"

echo "📝 Checking environment..."
railway status

echo "🚀 Deploying to Railway..."
railway up --detach

echo "✅ Deployment initiated!"
echo ""
echo "📊 View deployment status:"
echo "   railway status"
echo ""
echo "📋 View logs:"
echo "   railway logs"
echo ""
echo "🌐 Open in browser:"
echo "   railway open"

