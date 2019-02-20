all: help env clean lint test build

.PHONY: all

help:
	@echo "  env         install all production dependencies"
	@echo "  clean       remove unwanted stuff"
	@echo "  lint        check style with flake8"
	@echo "  test        run tests"
	@echo "  coverage    run tests with coverage

env:
	pip install -Ur requirements.txt


clean:
	rm -fr build
	rm -fr dist
	find . -name '*.pyc' -exec rm -f {} \;
	find . -name '*.pyo' -exec rm -f {} \;
	find . -name '*~' ! -name '*.un~' -exec rm -f {} \;

lint:
	flake8 --ignore E111,E124,E126,E221,E501,w504 --exclude .git,__pycache__


test:
	pytest -s tests
	#python setup.py test


coverage: clean
	coverage run --source=pyfacebook setup.py test
	coverage html
	coverage report


build: clean
	python setup.py check
	python setup.py sdist
	python setup.py bdist_wheel
