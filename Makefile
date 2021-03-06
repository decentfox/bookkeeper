.PHONY: clean-pyc clean-build clean

help:
	@echo "clean - remove all build, test and Python artifacts"
	@echo "clean-build - remove build artifacts"
	@echo "clean-pyc - remove Python file artifacts"
	@echo "test - run tests quickly with the default Python"
	@echo "release - package and upload a release"
	@echo "dist - package"
	@echo "install - install the package to the active Python's site-packages"

clean: clean-build clean-pyc

clean-build:
	rm -fr build/
	rm -fr dist/
	rm -fr .eggs/
	find . -name '*.egg-info' -exec rm -fr {} +
	find . -name '*.egg' -exec rm -f {} +

clean-pyc:
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +
	find . -name '__pycache__' -exec rm -fr {} +

test:
	python setup.py test

release: clean
	pip install git+https://github.com/decentfox/wheel.git
	python setup.py sdist upload
	python setup.py bdist_wheel --pyc-only upload

dist: clean
	pip install git+https://github.com/decentfox/wheel.git
	python setup.py sdist
	python setup.py bdist_wheel --pyc-only
	ls -l dist

install: clean
	pip install -e .
