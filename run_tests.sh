pip install -r requirements-dev.txt
coverage run --source app -m pytest -x -rxP --durations=10  && coverage report