## *********************
## * Makefile commands *
## *********************
##


.DEFAULT_GOAL := help

PYTHON_INTERPRETER=./venv/bin/python


.PHONY: deps
deps:         ## install all dependencies from requirements.txt
	$(PYTHON_INTERPRETER) -m pip install -r requirements.txt


.PHONY: help
help:         ## show this help
	@sed -ne '/@sed/!s/##\s\?//p' $(MAKEFILE_LIST)


.PHONY: init
init:         ## create virtual environment
	virtualenv venv -p python3
	$(MAKE) deps


.PHONY: lint
lint:         ## run linter with less strict checks
lint: DISABLE=invalid-name,unused-argument
lint: pylint

.PHONY: lint.all
lint.all:     ## run linter with all usable checks
lint.all: pylint

.PHONY: pylint
pylint:       ## run pylint (with disabled checks specified in $DISABLE variable)
	cd ..; ./op/$(PYTHON_INTERPRETER) -m pylint ./op --rcfile="./op/pylintrc" --disable="$(DISABLE)"


.PHONY: test
test:         ## run unit tests
	$(PYTHON_INTERPRETER) -m pytest tests/unit

.PHONY: test.all
test.all:     ## run all tests
	$(PYTHON_INTERPRETER) -m pytest tests