.PHONY: clean virtualenv test docker dist dist-upload

install: virtualenv require dist/ama-*.whl
	env/bin/python3 -m pip install . --use-feature=in-tree-build

installdev: virtualenv requiredev
	env/bin/python3 -m pip install . --verbose --use-feature=in-tree-build

dist/ama-*.whl: ama/core/plugins/hcutils/pyhcutils.pyx ama/core/plugins/hcutils/libhcutils/combinator.* ama/core/plugins/hcutils/libhcutils/combinator3.* ama/core/plugins/hcutils/libhcutils/combipow.*
	env/bin/python3 -m build

clean: cleanslurm cleanbkp cleanmasks cleanstats cleanpkg

cleanpkg:
	rm -rf ama.egg-info
	rm -rf build
	rm -rf dist

cleanslurm:
	rm -f slurm-*_*.out
	rm -f slurm-*.out

cleanbkp:
	rm -f *.bkp

cleanmasks:
	rm -f *.hcmasks
	rm -f *.masks
cleanstats:
	rm -f *.stats

virtualenv:
	python3 -m venv --prompt 'ama' env
	@echo
	@echo "Virtual enviroment was created. Now activate it: source env/bin/activate"
	@echo
	env/bin/python3 -m pip install --upgrade pip

require:
	env/bin/python3 -m pip install -r requirements.txt

requiredev:
	env/bin/python3 -m pip install -r requirements-dev.txt

pkg: dist/ama-*.whl
	env/bin/python3 -m pip install . --use-feature=in-tree-build

pkgdev: dist/ama-*.whl
	env/bin/python3 -m pip install . --verbose --use-feature=in-tree-build

dist: clean
	rm -rf dist/*
	env/bin/python3 setup.py sdist
	env/bin/python3 setup.py bdist_wheel

dist-upload:
	env/bin/twine upload dist/*
