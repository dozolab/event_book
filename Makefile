.PHONY: build clean clean-test clean-pyc clean-build start lint test

build:
	docker-compose build

start:
	docker-compose up

stop:
	docker-compose down

lint: ## check style with flake8
	docker-compose run -T parser-service flake8 --max-line-length 120 core tests

test: ## run tests quickly with pytest
	docker-compose run -T info py.test tests

run-testfile: ## run tests quickly with pytest
	docker-compose run -T parser-service py.test -vv -s $(FILE)

to-xml: ## run tests quickly with pytest
	docker-compose run -T parser-service pdftohtml $(IFILE) -xml -i -q $(OFILE)

clean: clean-build clean-pyc clean-test ## remove all build, test, coverage and Python artifacts

clean-build: ## remove build artifacts
	rm -fr build/
	rm -fr dist/
	rm -fr .eggs/
	find . -name '*.egg-info' -exec rm -fr {} +
	find . -name '*.egg' -exec rm -f {} +

clean-pyc: ## remove Python file artifacts
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +
	find . -name '__pycache__' -exec rm -fr {} +

clean-test: ## remove test and coverage artifacts
	rm -fr .tox/
	rm -f .coverage
	rm -fr htmlcov/
	rm -fr .pytest_cache
