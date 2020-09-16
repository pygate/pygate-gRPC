format:
	pipenv run isort setup.py pygate_grpc tests
	pipenv run black --line-length=120 setup.py pygate_grpc tests

lint:
	pipenv run flake8 setup.py pygate_grpc tests
	pipenv run mypy pygate_grpc
	pipenv run pylint --rcfile=.pylintrc setup.py pygate_grpc tests

tests:
	pipenv run integration-test
