#!/bin/bash

# Build the backend Docker image
docker build -t gcr.io/brawlmanager/brawlmanager-backend ./bm-backend

# Build the frontend Docker image
docker build -t gcr.io/brawlmanager/brawlmanager-frontend ./bm-frontend