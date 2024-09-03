#!/bin/bash

# Push the backend Docker image to Google Container Registry
docker push gcr.io/brawlmanager/brawlmanager-backend

# Push the frontend Docker image to Google Container Registry
docker push gcr.io/brawlmanager/brawlmanager-frontend