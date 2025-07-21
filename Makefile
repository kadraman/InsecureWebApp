-include .env

ROOT_DIR := $(abspath $(dir $(lastword $(MAKEFILE_LIST)))/..)
PROJECT := InsecureWebApp
PROJECT_LOWER := $(call tolower,$(PROJECT))
PROJECTS := $(filter %project%,$(wildcard *))
VERSION ?= $(shell git describe --tags --always --dirty --match=v* 2> /dev/null || echo "1.0.0")
COMMIT := $(shell git log -1 --pretty=format:"%H")

FLASK_APP := iwa

SAST_DEFAULT_OPTS := -Dcom.fortify.sca.ProjectRoot=.fortify -b "$(PROJECT)"
SAST_SCAN_OPTS := $(SAST_DEFAULT_OPTS)
ifeq ($(OS),Windows_NT)
	SAST_TRANSLATE_OPTS := $(SAST_DEFAULT_OPTS) -python-path ".venv\\Lib\\site-packages" iwa
	SAST_CUSTOM_RULES := etc\\sast-custom-rules\\example-custom-rules.xml
	SAST_FILTER := etc\\sast-filters\\example-filter.txt
else
	SAST_TRANSLATE_OPTS := $(SAST_DEFAULT_OPTS) -python-path ".venv/lib/python3.12/site-packages" iwa
	SAST_CUSTOM_RULES := $(ROOT_DIR)/etc/sast-custom-rules/example-custom-rules.xml
	SAST_FILTER := $(ROOT_DIR)/etc/sast-filters/example-filter.txt 
endif

.PHONY: default
default: help

# generate help info from comments
.PHONY: help
help: ## help information about make commands
	@python etc/print_makefile_help.py

.PHONY: version
version: ## display the version of the service
	@echo $(VERSION)

.PHONY: build
build:  ## build the project
	@echo "Building $(PROJECT)..."
	python -m venv .venv
	pip install -U flask
ifeq ($(OS),Windows_NT)
	cmd /c .\.venv\Scripts\activate.bat
	.venv/Scripts/pip install -r requirements.txt
else
	. .venv/bin/activate
	.venv/bin/pip install -r requirements.txt
endif


.PHONY: build-docker
build-docker: ## build the project as a docker image
	docker build -f Dockerfile -t $(PROJECT):$(VERSION) .

.PHONY: run
run: ## run the project
	@echo "Running $(PROJECT)..."
ifeq ($(OS),Windows_NT)
	cmd /C ".\.venv\Scripts\activate.bat && set FLASK_ENV=development && set FLASK_DEBUG=1 && set FLASK_APP=$(FLASK_APP) && flask run --host 0.0.0.0"
else
	FLASK_ENV=development FLASK_DEBUG=1 FLASK_APP=$(FLASK_APP) .venv/bin/flask run --host 0.0.0.0
endif

.PHONY: run-production
run-production: ## run the project in production mode
	@echo "Running $(PROJECT) in production mode..."
ifeq ($(OS),Windows_NT)
	cmd /C ".\.venv\Scripts\activate.bat && set FLASK_ENV=production && set FLASK_APP=$(FLASK_APP) && flask run --host 0.0.0.0"
else
	FLASK_ENV=production FLASK_APP=$(FLASK_APP) .venv/bin/flask run --host 0.0.0.0
endif

.PHONY: test
test: ## run unit tests for the project
	@echo "Testing $(PROJECT)..."
	pip install -U pytest
ifeq ($(OS),Windows_NT)
	cmd /C ".\.venv\Scripts\activate.bat && set FLASK_ENV=development && set FLASK_DEBUG=1 && set FLASK_APP=$(FLASK_APP) && pytest"
else
	FLASK_ENV=development FLASK_DEBUG=1 FLASK_APP=$(FLASK_APP) .venv/bin/pytest
endif

.PHONY: clean
clean: ## remove temporary files
ifeq ($(OS),Windows_NT)
	cmd /c "rmdir /s /q instance .venv .fortify bandit-report.html"
else
	rm -rf instance .venv .fortify bandit-report.html
endif

.PHONY: bandit-scan
bandit-scan: ## run Bandit security analysis
	@echo "Running Bandit security analysis..."
ifeq ($(OS),Windows_NT)
	.venv/Scripts/pip install bandit
	cmd /c ".venv\\Scripts\\bandit -r iwa -f html -o bandit-report.html"
else
	.venv/bin/pip install bandit
	.venv/bin/bandit -r iwa -f html -o bandit-report.html
endif
	@echo "Bandit report generated: bandit-report.html"

.PHONY: sast-scan
sast-scan: ## run OpenText static application security testing
	@echo "Running OpenText static application security testing..."
	sourceanalyzer $(SAST_DEFAULT_OPTS) -clean
	sourceanalyzer $(SAST_TRANSLATE_OPTS)
	sourceanalyzer $(SAST_SCAN_OPTS) -scan \
		-rules $(SAST_CUSTOM_RULES) \
		-filter $(SAST_FILTER) \
		-build-project "$(PROJECT)" -build-version "$(VERSION)" -build-label "SNAPSHOT" \
		-f "$(PROJECT).fpr"
ifeq ($(OS),Windows_NT)
	cmd /c "FPRUtility -information -analyzerIssueCounts -project $(PROJECT).fpr"
else
	FPRUtility -information -analyzerIssueCounts -project "$(PROJECT).fpr"
endif

.PHONY: sca-scan
sca-scan: ## run OpenText software composition analysis
	@echo "Running OpenText software composition analysis..."
	debricked scan . -r $(PROJECT) -c $(COMMIT) -t $(DEBRICKED_TOKEN)

.PHONY: nexus-iq-scan
nexus-iq-scan: ## run Sonatype Nexus IQ software composition analysis
	@echo "Running Sonatype Nexusi IQ software composition analysis..."
ifeq ($(OS),Windows_NT)
	cmd /c "rmdir /s /q deps"
	.venv/Scripts/pip download -r requirements.txt -d deps
else
	rm -rf deps
	.venv/bin/pip download -r requirements.txt -d deps
endif
	nexus-iq-cli -i $(PROJECT_LOWER) -s $(NEXUS_IQ_URL) -a "$(NEXUS_IQ_USERNAME):$(NEXUS_IQ_PASSWORD)" deps