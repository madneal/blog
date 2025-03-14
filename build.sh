#!/bin/bash  
set -e  # Exit immediately if a command exits with a non-zero status  

echo -e "\033[0;32mDeploying updates to GitHub...\033[0m"  

# Use current timestamp if no commit message provided  
msg="${1:-Rebuilding site $(date)}"  

# Ensure you're on the correct branch  
git checkout master  

# Pull latest changes first  
git pull origin master  

# Stage all changes  
git add -A  

# Commit changes  
git commit -m "$msg" || echo "No changes to commit"  

# Push to remote  
git push origin master  

# Build Hugo site with verbose output  
hugo -t hugo-nuo --verbose > hugo.log  

# Check build log for errors  
cat hugo.log  

# Enter public directory  
cd public  

# Stage public directory changes  
git add -A  

# Commit public directory changes  
git commit -m "$msg" || echo "No public changes to commit"  

# Pull and push public directory  
git pull origin master  
git push origin master  

echo -e "\033[0;32mDeployment completed!\033[0m"  