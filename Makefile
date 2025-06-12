-include .env

ROOT_DIR := $(abspath $(dir $(lastword $(MAKEFILE_LIST)))/..)
ROOT_DIR := $(shell dirname $(realpath $(firstword $(MAKEFILE_LIST))))
PROJECT := InsecureWebApp
PROJECTS := $(shell ls . | grep project)
VERSION ?= $(shell git describe --tags --always --dirty --match=v* 2> /dev/null || echo "1.0.0")
COMMIT := $(shell git log -1 --pretty=format:"%H")

FLASK_APP := iwa
FLASK := FLASK_APP=$(FLASK_APP) .venv/bin/flask

SAST_DEFAULT_OPTS := -Dcom.fortify.sca.ProjectRoot=.fortify -b "$(PROJECT)"
SAST_TRANSLATE_OPTS := $(SAST_DEFAULT_OPTS) -python-path ".venv/lib/python3.12/site-packages" iwa
SAST_SCAN_OPTS := $(SAST_DEFAULT_OPTS)

.PHONY: default
default: help

# generate help info from comments
.PHONY: help
help: ## help information about make commands
	@grep -h -P '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

.PHONY: version
version: ## display the version of the service
	@echo $(VERSION)

.PHONY: build
build:  ## build the project
	@echo "Building $(PROJECT)..."
	python -m venv .venv
	. .venv/bin/activate
	.venv/bin/pip install -r requirements.txt

.PHONY: build-docker
build-docker: ## build the project as a docker image
	docker build -f Dockerfile -t $(PROJECT):$(VERSION) .

.PHONY: run
run: ## run the project
	@echo "Running $(PROJECT)..."
	FLASK_ENV=development FLASK_DEBUG=1 FLASK_APP=$(FLASK_APP) .venv/bin/flask run --host 0.0.0.0

.PHONY: run-production
run-production: ## run the project in production mode
	@echo "Running $(PROJECT) in production mode..."
	FLASK_ENV=production FLASK_APP=$(FLASK_APP) .venv/bin/flask run --host 0.0.0.0

.PHONY: test
test: ## run unit tests for the project
	@echo "Testing $(PROJECT)..."
	FLASK_ENV=development FLASK_DEBUG=1 FLASK_APP=$(FLASK_APP) .venv/bin/pytest

.PHONY: clean
clean: ## remove temporary files
	rm -rf instance .venv .fortify *.lock

.PHONY: bandit-scan
bandit-scan: ## run Bandit security analysis
	@echo "Running Bandit security analysis..."
	@.venv/bin/pip install bandit
	@.venv/bin/bandit -r iwa -f html -o bandit-report.html
	@echo "Bandit report generated: bandit-report.html"

.PHONY: sast-scan
sast-scan: ## run OpenText static application security testing
	@echo "Running OpenText static application security testing..."
	@sourceanalyzer $(SAST_DEFAULT_OPTS) -clean
	@sourceanalyzer $(SAST_TRANSLATE_OPTS)
	@sourceanalyzer $(SAST_SCAN_OPTS) -scan \
		-rules $(ROOT_DIR)/etc/sast-custom-rules/example-custom-rules.xml \
		-filter $(ROOT_DIR)/etc/sast-filters/example-filter.txt \
		-build-project "$(PROJECT)" -build-version "$(VERSION)" -build-label "SNAPSHOT" \
		-f "$(PROJECT).fpr"
	@FPRUtility -information -analyzerIssueCounts -project "$(PROJECT).fpr"

.PHONY: sca-scan
sca-scan: ## run OpenText software composition analysis
	@echo "Running OpenText software composition analysis..."
	@debricked scan . -r $(PROJECT) -c $(COMMIT) -t $(DEBRICKED_TOKEN)


