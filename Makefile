.PHONY: clean virtualenv test docker dist dist-upload

install: require
	python3 -m pip install .
	
installdev: requiredev
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
	python3 -m venv --prompt 'ama' env
	@echo
	@echo "Virtual enviroment was created. Now run: source env/bin/activate"
	@echo "Now to install ama-framework run: make install"
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
