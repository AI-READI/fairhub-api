# api.fairhub.io

## Getting started

### Prerequisites/Dependencies

You will need the following installed on your system:

- Python 3.8+
- [Pip](https://pip.pypa.io/en/stable/)
- [Poetry](https://python-poetry.org/)
- [Docker](https://www.docker.com/)

### Setup

If you would like to update the api, please follow the instructions below.

1. Create a local virtual environment and activate it:

   ```bash
   python -m venv .venv
   source .venv/bin/activate
   ```

   If you are using Anaconda, you can create a virtual environment with:

   ```bash
   conda create -n fairhub-api-dev-env python=3.8
   conda activate fairhub-api-dev-env
   ```

2. Install the dependencies for this package. We use [Poetry](https://python-poetry.org/) to manage the dependencies:

   ```bash
   pip install poetry==1.3.2
   poetry install
   ```

   You can also use version 1.2.0 of Poetry, but you will need to run `poetry lock` after installing the dependencies.

3. Add your modifications and run the tests:

   ```bash
   poetry run pytest
   ```

   If you need to add new python packages, you can use Poetry to add them:

   ```bash
    poetry add <package-name>
   ```

4. Format the code:

   ```bash
   poe format
   ```

5. Check the code quality:

   ```bash
   poetry run flake8 pyfairdatatools tests
   ```

6. Run the tests and check the code coverage:

   ```bash
   poe test
   poe test --cov=pyfairdatatools
   ```

7. Build the package:

   Update the version number in `pyproject.toml` and `pyfairdatatools/__init__.py` and then run:

   ```text
   poetry build
   ```

8. Publish the package:

   ```bash
   poetry publish
   ```

## Docker

### Database

The api uses a postgres database. You can run a postgres database locally using docker:

```bash
docker-compose -f ./db-docker-compose.yaml up
```

Close the database with:

```bash
docker-compose -f ./db-docker-compose.yaml down -v
```

This database will not persist data between runs.

### Caching

The api uses a redis cache. You can run a redis cache locally using docker, too:
```bash
docker-compose -f ./cache-docker-compose.yaml up
```

Shut down the cache with:

```bash
docker-compose -f ./cache-docker-compose.yaml down -v
```

Like the database, the cache will not persist between runs.

### API

If you would like to run the api locally, you can use docker.

1. Build the docker image:

   ```bash
   docker build --tag fairhub-flask-api:local .
   ```

   You can set the `--tag` to whatever you want. We recommend to use `fairhub-flask-api:local`.

2. Run the docker image:

   ```bash
   docker run -p 5000:5000 -e FAIRHUB_DATABASE_URL=postgres://connection-string fairhub-flask-api:local
   ```

## License

This work is licensed under
[MIT](https://opensource.org/licenses/mit). See [LICENSE](https://github.com/AI-READI/pyfairdatatools/blob/main/LICENSE) for more information.

<a href="https://aireadi.org" >
  <img src="https://www.channelfutures.com/files/2017/04/3_0.png" height="30" />
</a>
