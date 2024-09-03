#!/bin/bash

# Deploy the backend service to Google Cloud Run
gcloud run deploy brawlmanager-backend \
  --image gcr.io/brawlmanager/brawlmanager-backend \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --set-env-vars=DATABASE_URL=YOUR_DATABASE_URL,GOOGLE_CLIENT_ID=YOUR_GOOGLE_CLIENT_ID,GOOGLE_CLIENT_SECRET=YOUR_GOOGLE_CLIENT_SECRET,SECRET_KEY=YOUR_SECRET_KEY

# Deploy the frontend service to Google Cloud Run
gcloud run deploy brawlmanager-frontend \
  --image gcr.io/brawlmanager/brawlmanager-frontend \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated