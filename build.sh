#!/bin/bash  

# Set strict error handling  
set -e  

# Color codes  
GREEN='\033[0;32m'  
RED='\033[0;31m'  
NC='\033[0m' # No Color  

# Function for logging  
log() {  
    echo -e "${GREEN}[DEPLOY] $1${NC}"  
}  

# Function for error handling  
error() {  
    echo -e "${RED}[ERROR] $1${NC}"  
    exit 1  
}  

# Timestamp for commit message  
TIMESTAMP=$(date "+%Y-%m-%d %H:%M:%S")  
COMMIT_MSG="${1:-Site update: $TIMESTAMP}"  

# Step 1: Verify current branch  
CURRENT_BRANCH=$(git rev-parse --abbrev-ref HEAD)  
if [ "$CURRENT_BRANCH" != "master" ]; then  
    error "Not on master branch. Current branch: $CURRENT_BRANCH"  
fi  

# Step 2: Pull latest changes  
log "Pulling latest changes..."  
git pull origin master || error "Failed to pull changes"  

# Step 3: Stage all changes  
log "Staging all changes..."  
git add -A  

# Step 4: Commit changes  
log "Committing changes: $COMMIT_MSG"  
git commit -m "$COMMIT_MSG" || log "No changes to commit"  

# Step 5: Push to repository  
log "Pushing to remote repository..."  
git push origin master || error "Failed to push to repository"  

# Step 6: Hugo build  
log "Building Hugo site..."  
hugo -t hugo-nuo || error "Hugo build failed"  

# Optional: Generate build log  
hugo -t hugo-nuo > hugo_build.log 2>&1  

# Step 7: Deploy public directory  
cd public  

# Stage public directory changes  
git add -A  

# Commit public changes  
git commit -m "$COMMIT_MSG" || log "No public directory changes"  

# Push public directory  
git pull origin master  
git push origin master  

# Final success message  
log "Deployment completed successfully! 🚀"  