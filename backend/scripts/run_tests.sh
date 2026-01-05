#!/bin/bash

# Run all tests with coverage

echo "🧪 Running tests..."

# Run pytest with coverage
pytest \
  --cov=app \
  --cov-report=term-missing \
  --cov-report=html \
  --cov-report=xml \
  --cov-fail-under=90 \
  -v

# Check if tests passed
if [ $? -eq 0 ]; then
    echo "✅ All tests passed!"
    echo "📊 Coverage report: htmlcov/index.html"
else
    echo "❌ Tests failed!"
    exit 1
fi


