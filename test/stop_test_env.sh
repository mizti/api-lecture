#!/bin/bash

# Stop and remove containers
docker-compose down

# Remove any leftover containers (if any)
docker ps -a | grep 'mysql' | awk '{print $1}' | xargs -r docker rm -f

# Remove the test network
docker network rm test-network 2>/dev/null || true
