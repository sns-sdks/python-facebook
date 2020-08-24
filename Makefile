all: help env clean docs lint test build

.PHONY: all

help:
	@echo "  env         install all production dependencies"
	@echo "  clean       remove unwanted stuff"
	@echo "  docs        build documentation"
	@echo "  lint        check style with flake8"
	@echo "  test        run tests"

env:
	pip install pipenv
	pipenv install --dev


clean:
	rm -fr build
	rm -fr dist
	rm -fr  *.egg-info
	find . -name '*.pyc' -exec rm -f {} \;
	find . -name '*.pyo' -exec rm -f {} \;
	find . -name '*~' ! -name '*.un~' -exec rm -f {} \;


docs:
	$(MAKE) -C doc html

lint:
	flake8 --ignore E111,E124,E126,E221,E501,w504 --exclude .git,__pycache__


test:
	pytest -s


build: clean
	python setup.py check
	python setup.py sdist
	python setup.py bdist_wheel
