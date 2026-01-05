#!/bin/bash

# Development startup script

echo "🚀 Starting FinanceAI Backend (Development)"

# Check if .env exists
if [ ! -f .env ]; then
    echo "⚠️  .env file not found, creating from template..."
    cp env.template .env
    echo "✅ .env created. Please fill in your API keys!"
    exit 1
fi

# Start Docker services
echo "🐳 Starting PostgreSQL and Redis..."
docker-compose up -d postgres redis

# Wait for PostgreSQL to be ready
echo "⏳ Waiting for PostgreSQL..."
sleep 3

# Run migrations
echo "📊 Running database migrations..."
alembic upgrade head

# Start backend
echo "🔥 Starting FastAPI server..."
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000


