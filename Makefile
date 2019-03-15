# Second tag after tip is usually the latest release
RELEASE=$(shell hg tags -T "{node|short}\n" | sed -n 2p)

develop:
	pip install -ve . | grep -v link

help:
	@echo "targets: cleanall and develop"

clean:
	rm -rf build dist

clean_pyc:
	find fluidsht -name "*.pyc" -delete
	find fluidsht -name "__pycache__" -type d | xargs rm -rf

cleanpythran:
	find fluidsht -name "__pythran__" -type d | xargs rm -rf

cleanall: clean clean_pyc cleanpythran

shortlog:
	@hg log -M -r$(RELEASE): --template '- {desc|firstline} (:rev:`{node|short}`)\n'

deploy: cleanall
	python setup.py sdist
	# python setup.py bdist_wheel
	twine upload dist/*

tests:
	python -m unittest discover -v

_tests_coverage:
	mkdir -p .coverage
	coverage run -m unittest discover

_report_coverage:
	coverage report
	coverage html
	coverage xml
	@echo "Code coverage analysis complete. View detailed report:"
	@echo "file://${PWD}/.coverage/index.html"

coverage: _tests_coverage _report_coverage

black:
	black -l 82 fluidsht

black_commit: black
	hg commit -m "Apply $(shell black --version)"
