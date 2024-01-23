# Pytest for AI-READI API Testing

Pytest is a testing framework that allows you to write tests for your code. It is used for testing the API of AI-READI.

## Running Tests

To run the tests, you can use the following commands:

```bash
# Run all tests
poe test
# Run all tests with print statements
poe test_with_capture
```

## Writing Tests

To write tests, you can follow the format of the tests in the `tests/functional` directory. The tests are written using pytest fixtures. You can read more about fixtures [here](https://docs.pytest.org/en/stable/fixture.html).

Pytest Fixtures allow for functions to be used across testing files and modules. This is useful for setting up the testing clients needed throughout testing. For example, the `client` fixture in `tests/conftest.py` is used to create multiple clients for testing. The `client` fixture creates multiple users with different permissions after the POST request is made to the `/study` endpoint. This allows for the main user to invite contributors and admins to the study.

Everytime the test is run with `poe test`, the database is cleared and the fixtures are run again. This ensures that the tests are run on a clean database everytime. This is done by using the `@pytest.fixture(scope='session')` decorator. The `scope='session'` ensures that the fixture is only run once per session. Then after the main user is logged in with `_logged_in_user` but then `clients` is used once all users have been created and signed in.

To create fixtures resort to using the `@pytest.fixture` decorator. This will allow for the fixture to be used in other testing files. The `@pytest.fixture` decorator can take in a `scope` argument. The `scope` argument can be used to specify how often the fixture is run. The `scope` argument can take in the following values:

- `function`: The fixture is run once per test function. (default)
- `class`: The fixture is run once per test class.
- `module`: The fixture is run once per test module.
- `package`: The fixture is run once per test package.
- `session`: The fixture is run once per test session.

Global variables are created in `conftest.py` to manage important information such as `study_id`, `dataset_id`. These variables are used throughout the testing files. The `conftest.py` file is used to store fixtures that are used across multiple testing files. The `conftest.py` file is automatically discovered by pytest. You can read more about `conftest.py` [here](https://docs.pytest.org/en/stable/fixture.html#conftest-py-sharing-fixture-functions).