#!/bin/bash

# Build the backend Docker image
docker build -t gcr.io/brawlmanager/brawlmanager-backend -f bm-backend/Dockerfile .

# Build the frontend Docker image
docker build -t gcr.io/brawlmanager/brawlmanager-frontend -f bm-frontend/Dockerfile bm-frontend
