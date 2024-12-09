#!/bin/bash
# Usage: */5 * * * * /path/to/script.sh >> /path/to/logfile.log 2>&1

cd /imaging-plaza/gimie-api || exit

# Check if local is behind remote
LOCAL=$(git rev-parse develop)
REMOTE=$(git rev-parse origin/develop)

if [ "$LOCAL" != "$REMOTE" ]; then
  echo "Changes detected. Pulling..."
  git pull origin develop
  
  # Stop and remove the old container
  docker stop gimieapi || true
  docker rm gimieapi || true
  
  # Rebuild and run the new container
  docker build -t gimieapi .
  docker run -d --name gimieapi -p 7000:15400 gimieapi
else
  echo "No changes found."
fi