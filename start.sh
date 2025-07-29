#!/bin/bash
set -e

echo "Starting KMart ML API server..."
echo "PORT environment variable: $PORT"

# Use PORT environment variable or default to 8000
PORT=${PORT:-8000}

echo "Starting uvicorn on port $PORT"
uvicorn api_server_refactored:app --host 0.0.0.0 --port $PORT 