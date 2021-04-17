.PHONY: clean virtualenv test docker dist dist-upload

clean: cleanslurm cleanbkp cleanmasks

cleanslurm:
	rm -f slurm-*_*.out
	rm -f slurm-*.out

cleanbkp:
	rm -f *.bkp

cleanmasks:
	rm -f *.hcmasks
	rm -f *.masks

virtualenv:
	virtualenv --prompt '(ama)' env
	env/bin/pip3 install -r requirements-dev.txt
	env/bin/python3 setup.py develop
	@echo
	@echo "VirtualENV Setup Complete. Now run: source env/bin/activate"
	@echo

require:
	python3 -m pip install -r requirements.txt

requiredev:
	python3 -m pip install -r requirements-dev.txt

install: require
	python3 -m pip install .
	
installdev: requiredev
	python3 -m pip install . --verbose

pkgdev:
	python3 -m pip install . --verbose

test:
	env/bin/python3 -m pytest \
		-v \
		--cov=ama \
		--cov-report=term \
		--cov-report=html:coverage-report \
		tests/

docker: clean
	docker build -t ama:latest .

dist: clean
	rm -rf dist/*
	python setup.py sdist
	python setup.py bdist_wheel

dist-upload:
	twine upload dist/*
