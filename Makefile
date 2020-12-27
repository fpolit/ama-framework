.PHONY: clean virtualenv test docker dist dist-upload

clean:
	find . -name '*.py[co]' -delete

virtualenv:
	virtualenv --prompt '|> mattack <| ' env
	env/bin/pip3 install -r requirements-dev.txt
	env/bin/python3 setup.py develop
	@echo
	@echo "VirtualENV Setup Complete. Now run: source env/bin/activate"
	@echo

pkg:
	python3 -m pip install -r requirements.txt

pkgdev:
	python3 -m pip install -r requirements-dev.txt

install:
	python3 -m pip install -r requirements.txt
	python3 -m pip install .
	
installdev:
	python3 -m pip install -r requirements-dev.txt
	python3 -m pip install .

test:
	env/bin/python3 -m pytest \
		-v \
		--cov=mattack \
		--cov-report=term \
		--cov-report=html:coverage-report \
		tests/

docker: clean
	docker build -t mattack:latest .

dist: clean
	rm -rf dist/*
	python setup.py sdist
	python setup.py bdist_wheel

dist-upload:
	twine upload dist/*
