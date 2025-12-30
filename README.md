# Geolibrary

A modern Python library for geospatial location management with PostgreSQL, featuring pure Python Ray Casting algorithm for point-in-polygon queries.

## Features

- SQLAlchemy 2.0 with PostgreSQL backend
- CRUD operations for locations and photos
- Pure Python Ray Casting algorithm for geospatial filtering
- Command-line interface using Click
- Full type hints and PEP 8 compliance

## Installation

### Configure Private Repository (Required)

This project uses the `artifactory-geo-pypi-dev-virtual` repository definition to publish (without /simple at the end) and the `geo-pypi-dev-virtual` repository definition to resolve. The `pyproject.toml` doesn't contains any credentials.


**Manual setup:**
```bash
# For fetching dependencies (modifies pyproject.toml locally)
poetry source add --priority=primary geo-pypi-dev-virtual https://solengeu.jfrog.io/artifactory/api/pypi/geo-pypi-dev-virtual/simple
poetry config http-basic.geo-pypi-dev-virtual <username> <password>

# For publishing (global config)
poetry config repositories.artifactory-geo-pypi-dev-virtual https://solengeu.jfrog.io/artifactory/api/pypi/geo-pypi-dev-virtual
poetry config http-basic.artifactory-geo-pypi-dev-virtual <username> <password>
```

### Install Dependencies

```bash
poetry install
```

## Configuration

Create a `.env` file in the project root with your PostgreSQL connection details:

```env
DATABASE_URL=postgresql://user:password@localhost:5432/geolibrary
```

Alternatively, you can use individual environment variables:

```env
DB_HOST=localhost
DB_PORT=5432
DB_USER=user
DB_PASSWORD=password
DB_NAME=geolibrary
```

## CLI Usage

The CLI is implemented using the [click](https://click.palletsprojects.com/en/stable/) framework.

### Initialize Database

```bash
poetry run geolib init-db
```

### Add a Location

```bash
poetry run geolib add --name "Central Park" --description "Famous park in NYC" --latitude 40.785091 --longitude -73.968285
```

### List All Locations

```bash
poetry run geolib list
```

### Get Location by ID or Name

```bash
poetry run geolib get --id 1
# or
poetry run geolib get --name "Central Park"
```

### Search Locations in Area

```bash
poetry run geolib search-area "40.7,-74.0 40.8,-74.0 40.8,-73.9 40.7,-73.9"
```

The search-area command accepts space-separated coordinate pairs in `latitude,longitude` format forming a polygon perimeter.

## Development

This project uses:
- Python 3.12+
- Poetry for dependency management
- SQLAlchemy 2.0
- Click for CLI
- PostgreSQL with psycopg2-binary

## Publishing

To publish this package to Artifactory, see [PUBLISHING.md](PUBLISHING.md) for detailed instructions.

Quick publish commands:
```bash
poetry build
poetry publish --repository artifactory-geo-pypi-dev-virtual --dist-dir ./dist
```
## Launch unit tests

```bash
poetry run pytest
```

