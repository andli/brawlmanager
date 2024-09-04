docker-compose build
docker push gcr.io/brawlmanager/brawlmanager-backend
docker push gcr.io/brawlmanager/brawlmanager-frontend
gcloud run deploy brawlmanager-backend --image gcr.io/brawlmanager/brawlmanager-backend --platform managed --region us-central1 --env-vars-file .env --allow-unauthenticated
gcloud run deploy brawlmanager-frontend --image gcr.io/brawlmanager/brawlmanager-frontend --platform managed --region us-central1 --env-vars-file .env --allow-unauthenticated