format:
	pipenv run isort setup.py src tests
	pipenv run black --line-length=120 setup.py src tests

lint:
	pipenv run flake8 setup.py src tests
	pipenv run mypy src
	pipenv run pylint --rcfile=.pylintrc setup.py src tests

tests:
	pipenv run integration-test
