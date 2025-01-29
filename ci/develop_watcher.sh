#!/bin/bash
# Usage: */5 * * * * /imaging-plaza/ci/develop_watcher.sh >> /imaging-plaza/ci/develop_watcher.log 2>&1

cd /imaging-plaza/gimie-api || exit

# Fetch the latest changes from the remote
git fetch origin develop

# Check if local is behind remote
LOCAL=$(git rev-parse HEAD)
REMOTE=$(git rev-parse origin/develop)

if [ "$LOCAL" != "$REMOTE" ]; then
  echo "$(date '+%Y-%m-%d %H:%M:%S'). Changes detected. Pulling..."
  git pull origin develop
  
  # Stop and remove the old container
  docker stop gimie-api || true
  docker rm gimie-api || true
  
  # Rebuild and run the new container
  docker build -t gimie-api .
  docker run -d --name gimie-api --env-file .env -p 7511:15400 gimie-api
else
  echo "$(date '+%Y-%m-%d %H:%M:%S'). No changes found."
fi
