#!/bin/bash
set -e
docker-compose build
docker-compose up -d db
echo "Waiting for database to initialize..." && sleep 5;
docker-compose run --rm web python -c 'from app.main import db; db.init_db()'
docker-compose up -d
echo "Waiting the download... (~1.7Gb, the ai will be dead until models finish downloading. you can check status with 'docker-compose logs ai' where you should see a uvicorn server)"  && sleep 120
