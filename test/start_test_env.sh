#!/bin/bash

# Kill any existing uvicorn processes
pkill uvicorn || true

# Create docker network if it doesn't exist
docker network create test-network 2>/dev/null || true

# Start MySQL container
docker-compose up -d

# Wait for MySQL to be ready
echo "Waiting for MySQL to be ready..."
sleep 10

# Set environment variables for the application
export MYSQL_HOST=localhost
export MYSQL_USER=user
export MYSQL_PASSWORD=password
export MYSQL_DB=lecture_db
export MYSQL_PORT=3306

# Change to app directory and start the FastAPI application
cd ../app || exit
uvicorn main:app --reload --host 0.0.0.0 --port 8003
