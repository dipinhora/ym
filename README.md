To install required python modules:

`pip install -r requirements.txt`

To run tests:

`pytest -v test_solution.py`

To run it all in a docker container:

`docker run --rm -v $(pwd):$(pwd) -w $(pwd) frolvlad/alpine-python-machinelearning sh -c 'pip install -r requirements.txt && PYTHONDONTWRITEBYTECODE=1 pytest -o cache_dir=/tmp -v test_solution.py'`
