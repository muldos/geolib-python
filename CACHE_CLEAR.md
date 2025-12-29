# Clearing Local Cache Files

This guide covers cleaning all types of cache files in your project.

## Quick Clean (All Caches)

Run the cleanup script:
```bash
./clean-cache.sh
```

Or manually clean everything:
```bash
# Python cache files
find . -type d -name "__pycache__" -exec rm -r {} + 2>/dev/null
find . -type f -name "*.pyc" -delete
find . -type f -name "*.pyo" -delete

# Build artifacts
rm -rf dist/ build/ *.egg-info/

# Test cache
rm -rf .pytest_cache/ .coverage htmlcov/ .tox/ .nox/

# Type checking cache
rm -rf .mypy_cache/ .dmypy.json dmypy.json

# Poetry cache (specific repository)
poetry cache clear artifactory-geo-pypi-dev-virtual --all -n
```

## Clear Poetry Cache

### Clear All Caches (Non-Interactive)
```bash
# Clear cache for a specific repository
poetry cache clear artifactory-geo-pypi-dev-virtual --all -n

# Clear all Poetry caches (will prompt for confirmation)
poetry cache clear --all pypi
```

### Clear Specific Repository Cache
```bash
# Clear cache for your Artifactory repository
poetry cache clear artifactory-geo-pypi-dev-virtual --all -n

# Clear cache for PyPI
poetry cache clear pypi --all -n
```

### View Cache Contents
```bash
poetry cache list
```

## Re-download Dependencies

### Option 1: Remove Lock File and Reinstall (Recommended)
```bash
# Remove the lock file
rm poetry.lock

# Remove virtual environment (optional, for complete clean)
rm -rf .venv

# Reinstall everything from scratch
poetry install
```

### Option 2: Update Dependencies
```bash
# Update all dependencies to latest compatible versions
poetry update

# Or update specific package
poetry update sqlalchemy
```

### Option 3: Force Reinstall
```bash
# Remove virtual environment
rm -rf .venv

# Reinstall
poetry install
```

## Clear Python Cache Files

### Python Bytecode Cache
```bash
# Remove all __pycache__ directories
find . -type d -name "__pycache__" -exec rm -r {} + 2>/dev/null

# Remove all .pyc files
find . -type f -name "*.pyc" -delete

# Remove all .pyo files
find . -type f -name "*.pyo" -delete
```

## Clear Build Artifacts

```bash
# Remove distribution files
rm -rf dist/

# Remove build files
rm -rf build/

# Remove egg-info directories
find . -type d -name "*.egg-info" -exec rm -r {} + 2>/dev/null
find . -type d -name "*.egg" -exec rm -r {} + 2>/dev/null
```

## Clear Test Cache

```bash
# Pytest cache
rm -rf .pytest_cache/

# Coverage files
rm -rf .coverage .coverage.* htmlcov/ .tox/ .nox/

# Hypothesis cache
rm -rf .hypothesis/
```

## Clear Type Checking Cache

```bash
# MyPy cache
rm -rf .mypy_cache/ .dmypy.json dmypy.json

# Pyre cache
rm -rf .pyre/
```

## Complete Clean Script

Create a `clean-cache.sh` script for easy cleanup:

```bash
#!/bin/bash
# Clean all cache files and build artifacts

echo "Cleaning Python cache files..."
find . -type d -name "__pycache__" -exec rm -r {} + 2>/dev/null
find . -type f -name "*.pyc" -delete
find . -type f -name "*.pyo" -delete

echo "Cleaning build artifacts..."
rm -rf dist/ build/
find . -type d -name "*.egg-info" -exec rm -r {} + 2>/dev/null

echo "Cleaning test cache..."
rm -rf .pytest_cache/ .coverage .coverage.* htmlcov/ .tox/ .nox/ .hypothesis/

echo "Cleaning type checking cache..."
rm -rf .mypy_cache/ .dmypy.json dmypy.json .pyre/

echo "Cleaning Poetry cache..."
poetry cache clear artifactory-geo-pypi-dev-virtual --all -n 2>/dev/null || true

echo "Cache cleanup complete!"
```

## Verify Installation

After reinstalling, verify everything works:
```bash
# Check installed packages
poetry show

# Run tests
poetry run pytest

# Test CLI
poetry run geolib list
```

