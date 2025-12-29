# Publishing to Artifactory

This guide explains how to publish the `geolibrary` package to your Artifactory repository.

## Prerequisites

1. Build the package
2. Configure Artifactory repository for publishing
3. Set up authentication credentials

## Step 1: Build the Package

First, build the distribution packages:

```bash
poetry build
```

This creates:
- A source distribution (`.tar.gz` file)
- A wheel distribution (`.whl` file)

Both files will be in the `dist/` directory.

## Step 2: Configure Publishing Repository

The repository `artifactory-geo-pypi-dev-virtual` should already be configured if you ran `./setup-repo.sh`. If not, configure it:

```bash
poetry config repositories.artifactory-geo-pypi-dev-virtual https://solengeu.jfrog.io/artifactory/api/pypi/geo-pypi-dev-virtual
```

**Note:** The publish URL does NOT include `/simple` at the end, while the install URL does.

## Step 3: Configure Authentication

Set up your Artifactory credentials:

```bash
poetry config http-basic.artifactory-geo-pypi-dev-virtual <username> <password>
```

## Step 4: Publish

Publish to your configured repository:

```bash
poetry publish --repository artifactory-geo-pypi-dev-virtual --dist-dir ./dist 
```

## Alternative: Using Environment Variables

You can also use environment variables for authentication:

```bash
export POETRY_HTTP_BASIC_ARTIFACTORY_GEO_PYPI_DEV_VIRTUAL_USERNAME=<username>
export POETRY_HTTP_BASIC_ARTIFACTORY_GEO_PYPI_DEV_VIRTUAL_PASSWORD=<password>

poetry publish --repository artifactory-geo-pypi-dev-virtual --dist-dir ./dist 
```

## Verify Publication

After publishing, verify the package is available:

```bash
# Test installing from your repository (if not already configured)
poetry source add --priority=primary geo-pypi-dev-virtual https://solengeu.jfrog.io/artifactory/api/pypi/geo-pypi-dev-virtual/simple
poetry install
```

## Version Management

Before publishing a new version, update the version in `pyproject.toml`:

```toml
[tool.poetry]
version = "0.1.1"  # Increment version
```

Or use Poetry's version commands:

```bash
# Bump patch version (0.1.0 -> 0.1.1)
poetry version patch

# Bump minor version (0.1.0 -> 0.2.0)
poetry version minor

# Bump major version (0.1.0 -> 1.0.0)
poetry version major
```

## Complete Workflow

```bash
# 1. Update version (if needed)
poetry version patch

# 2. Build the package
poetry build

# 3. Publish to Artifactory
poetry publish --repository artifactory-geo-pypi-dev-virtual
```

## Troubleshooting

### Repository Not Found

If Poetry can't find the repository:
- Verify it's configured: `poetry config --list | grep repositories`
- Make sure you're using the correct repository name in the `--repository` flag

### Package Already Exists

If the version already exists in Artifactory:
- Increment the version number
- Or use `--skip-existing` flag: `poetry publish --repository artifactory-geo-pypi-dev-virtual --skip-existing`

