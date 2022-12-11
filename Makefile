lint:
	poetry run flake8 --max-line-length 120 --extend-ignore E203,E741,E731 .
	poetry run mypy .
	poetry run isort -c .
	poetry run black -l 120 --check --diff .

fmt:
	poetry run isort .
	poetry run black -l 120 .

test:
	poetry run pytest .