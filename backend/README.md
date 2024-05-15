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
To see the Documentation of SwaggeUI, go to [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
Look up the section Schemas and try out the API.

## Run Tests

To Run the Tests run:

```
PYTHONPATH=. pytest tests/test_main.py;          
```

Since our Project Structure is splitted into the code and the tests, we cannot just run "pytest" but also have to
provide the path.

### Setting up with Pycharm


