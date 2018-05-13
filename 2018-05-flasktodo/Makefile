run:
	FLASK_APP=flasktd FLASK_ENV=development	flask run

init-db:
	FLASK_APP=flasktd flask init-db

test:
	pytest

coverage:
	coverage run -m pytest
	coverage report

coverage-report: coverage
	coverage html
	firefox ./htmlcov/index.html

.PHONY: test coverage-report
