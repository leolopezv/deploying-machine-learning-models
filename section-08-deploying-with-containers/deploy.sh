#!/bin/bash

# Deployment script for house-prices-api to Railway
# This script automates the manual deployment steps

set -e  # Exit on error

echo "🚀 Starting House Prices API Deployment..."

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check for required environment variables
check_env_vars() {
    local required_vars=("RAILWAY_TOKEN" "DOCKER_USERNAME" "DOCKER_PASSWORD" "PIP_EXTRA_INDEX_URL")
    for var in "${required_vars[@]}"; do
        if [ -z "${!var}" ]; then
            echo -e "${RED}❌ Error: $var is not set${NC}"
            return 1
        fi
    done
    echo -e "${GREEN}✓ All required environment variables are set${NC}"
}

# Build Docker image
build_docker_image() {
    echo -e "${YELLOW}📦 Building Docker image...${NC}"
    docker build \
        --build-arg PIP_EXTRA_INDEX_URL="${PIP_EXTRA_INDEX_URL}" \
        -t house-prices-api:latest \
        -t house-prices-api:${CI_COMMIT_SHA:0:7} \
        section-08-deploying-with-containers/.
    echo -e "${GREEN}✓ Docker image built successfully${NC}"
}

# Push to Docker Hub
push_to_docker_hub() {
    echo -e "${YELLOW}🐳 Pushing to Docker Hub...${NC}"
    echo "${DOCKER_PASSWORD}" | docker login -u "${DOCKER_USERNAME}" --password-stdin
    docker tag house-prices-api:latest "${DOCKER_USERNAME}/house-prices-api:latest"
    docker tag house-prices-api:${CI_COMMIT_SHA:0:7} "${DOCKER_USERNAME}/house-prices-api:${CI_COMMIT_SHA:0:7}"
    docker push "${DOCKER_USERNAME}/house-prices-api:latest"
    docker push "${DOCKER_USERNAME}/house-prices-api:${CI_COMMIT_SHA:0:7}"
    echo -e "${GREEN}✓ Image pushed to Docker Hub${NC}"
}

# Deploy to Railway
deploy_to_railway() {
    echo -e "${YELLOW}🚂 Deploying to Railway...${NC}"

    # Check if Railway CLI is installed
    if ! command -v railway &> /dev/null; then
        echo -e "${YELLOW}Installing Railway CLI...${NC}"
        npm install -g @railway/cli
    fi

    export RAILWAY_TOKEN="${RAILWAY_TOKEN}"

    # Deploy using Railway CLI
    railway up \
        --service house-prices-api \
        --dockerfile section-08-deploying-with-containers/Dockerfile \
        --build-arg PIP_EXTRA_INDEX_URL="${PIP_EXTRA_INDEX_URL}"

    echo -e "${GREEN}✓ Deployment to Railway completed${NC}"
}

# Run tests
run_tests() {
    echo -e "${YELLOW}🧪 Running tests...${NC}"
    cd section-08-deploying-with-containers/house-prices-api
    pip install -r test_requirements.txt
    pytest
    cd - > /dev/null
    echo -e "${GREEN}✓ Tests passed${NC}"
}

# Main execution
main() {
    echo "=================================================="
    echo "  House Prices API Deployment Pipeline"
    echo "=================================================="
    echo ""

    # Parse arguments
    case "${1:-all}" in
        check)
            check_env_vars
            ;;
        test)
            run_tests
            ;;
        build)
            build_docker_image
            ;;
        push)
            push_to_docker_hub
            ;;
        deploy)
            deploy_to_railway
            ;;
        all)
            check_env_vars
            run_tests
            build_docker_image
            push_to_docker_hub
            deploy_to_railway
            ;;
        *)
            echo "Usage: $0 {check|test|build|push|deploy|all}"
            echo ""
            echo "  check   - Check environment variables"
            echo "  test    - Run tests only"
            echo "  build   - Build Docker image"
            echo "  push    - Push to Docker Hub"
            echo "  deploy  - Deploy to Railway"
            echo "  all     - Run all steps (default)"
            exit 1
            ;;
    esac

    echo ""
    echo -e "${GREEN}✅ Deployment pipeline completed successfully!${NC}"
    echo "=================================================="
}

main "$@"

