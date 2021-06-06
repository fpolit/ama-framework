.PHONY: clean virtualenv test docker dist dist-upload

install:
	python3 -m pip install .
	
installdev:
	python3 -m pip install . --verbose

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
	env/bin/pip3 install -r requirements.txt
	@echo
	@echo "VirtualENV Setup Complete. Now run: source env/bin/activate"
	@echo

virtualenv_dev:
	virtualenv --prompt '(ama)' env
	env/bin/pip3 install -r requirements-dev.txt
	@echo
	@echo "VirtualENV Setup Complete. Now run: source env/bin/activate"
	@echo

require:
	python3 -m pip install -r requirements.txt

requiredev:
	python3 -m pip install -r requirements-dev.txt

pkgdev:
	python3 -m pip install . --verbose

dist: clean
	rm -rf dist/*
	python setup.py sdist
	python setup.py bdist_wheel

dist-upload:
	twine upload dist/*
