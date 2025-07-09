#!/bin/bash

# Pull latest image from Docker Hub
docker pull your_dockerhub_username/flask-api:latest

# Stop and remove existing container
docker stop flask-api || true
docker rm flask-api || true

# Run the container
docker run -d --name flask-api -p 80:5000 your_dockerhub_username/flask-api:latest
