# Developer Guide
## Setup / Install
First Navigate into this directory:
```commandline
cd backend
```
Then download the packages for the backend

```commandline
pip install -r requirements.txt
```

To run the Server run the Command:

```commandline
fastapi dev src/amin.py
```

The Server will run on the Port [http://127.0.0.1:8000](http://127.0.0.1:8000)
To see the Documentation of SwaggerUI, go to [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
Look up the section Schemas and try out the API.

## Run Tests

To Run the Tests run:

```
PYTHONPATH=. pytest tests/test_main.py;          
```

Since our Project Structure is splitted into the code and the tests, we cannot just run "pytest" but also have to
provide the path.

### Coverage

To run a coverage Test run:

```
PYTHONPATH=. coverage run -m pytest tests/test_main.py; 
```

and then the report:

```
coverage report -m
```

or create a html report with

```
coverage html
```

This will create a htmlcov/ directory with an index.html file in it.
Upon running the index.html file you can see the test coverage report as a website.

### Setting up with Pycharm

1. Install Requirements from requirements.txt
2. Run Tests
    1. On the Top Right Add a Configuration
    2. Select pytest
    3. Select tests/test_main.py as script
3. Add FastAPI as a new configuration and select /src/main.py as script

