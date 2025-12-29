#!/bin/bash
# Clean all cache files and build artifacts

set -e

echo "🧹 Cleaning local cache files..."

# Python cache files
echo "  - Cleaning Python cache files (__pycache__, *.pyc)..."
find . -type d -name "__pycache__" -exec rm -r {} + 2>/dev/null || true
find . -type f -name "*.pyc" -delete 2>/dev/null || true
find . -type f -name "*.pyo" -delete 2>/dev/null || true

# Build artifacts
echo "  - Cleaning build artifacts (dist/, build/, *.egg-info)..."
rm -rf dist/ build/ 2>/dev/null || true
find . -type d -name "*.egg-info" -exec rm -r {} + 2>/dev/null || true
find . -type d -name "*.egg" -exec rm -r {} + 2>/dev/null || true

# Test cache
echo "  - Cleaning test cache (.pytest_cache, .coverage, htmlcov/)..."
rm -rf .pytest_cache/ .coverage .coverage.* htmlcov/ .tox/ .nox/ .hypothesis/ 2>/dev/null || true

# Type checking cache
echo "  - Cleaning type checking cache (.mypy_cache, .pyre/)..."
rm -rf .mypy_cache/ .dmypy.json dmypy.json .pyre/ 2>/dev/null || true

# Poetry cache
echo "  - Cleaning Poetry cache..."
poetry cache clear artifactory-geo-pypi-dev-virtual --all -n 2>/dev/null || true

echo "✅ Cache cleanup complete!"

