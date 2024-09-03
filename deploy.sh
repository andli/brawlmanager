#!/bin/bash

# Load environment variables from the .env file into local variables
while IFS='=' read -r key value; do
  # Trim whitespace
  key=$(echo $key | xargs)
  value=$(echo $value | xargs)

  # Skip lines that are comments or empty
  if [[ -z "$key" || "$key" == \#* ]]; then
    continue
  fi

  # Assign the variables
  case $key in
    DATABASE_URL) DATABASE_URL=$value ;;
    GOOGLE_CLIENT_ID) GOOGLE_CLIENT_ID=$value ;;
    GOOGLE_CLIENT_SECRET) GOOGLE_CLIENT_SECRET=$value ;;
    SECRET_KEY) SECRET_KEY=$value ;;
    GOOGLE_REDIRECT_URI) GOOGLE_REDIRECT_URI=$value ;;
  esac
done < .env

# Deploy the backend service to Google Cloud Run
gcloud run deploy brawlmanager-backend \
  --image gcr.io/brawlmanager/brawlmanager-backend \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --set-env-vars=DATABASE_URL=$DATABASE_URL,GOOGLE_CLIENT_ID=$GOOGLE_CLIENT_ID,GOOGLE_CLIENT_SECRET=$GOOGLE_CLIENT_SECRET,SECRET_KEY=$SECRET_KEY,GOOGLE_REDIRECT_URI=$GOOGLE_REDIRECT_URI

# Deploy the frontend service to Google Cloud Run
gcloud run deploy brawlmanager-frontend \
  --image gcr.io/brawlmanager/brawlmanager-frontend \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated