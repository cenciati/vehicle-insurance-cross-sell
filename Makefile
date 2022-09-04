SHELL = /bin/bash

# set variables
PYTHON := python3
PIP := pip3
IMAGE_NAME := api:latest
CONTAINER_NAME := api_vehicle_insurance

.PHONY: help
help:
	@echo "~~~~~~~~~~~~~~~~~~~HELP~~~~~~~~~~~~~~~~~~~~"
	@echo "setup : prepares the enviornment."
	@echo "clean : cleans the environment."
	@echo "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"

.ONESHELL:
.PHONY: setup
setup:
	${PYTHON} -m venv .venv
	source .venv/bin/activate
	${PIP} install --no-cache-dir --upgrade -r requirements.txt
	${PIP} install -r requirements.txt
	pre-commit install
	docker image build -t ${IMAGE_NAME} .
	docker container run --name ${CONTAINER_NAME} -p 8000:8000 -d --rm ${IMAGE_NAME}

.PHONY: clean
clean: setup
	docker container stop ${CONTAINER_NAME}
	docker image rm ${IMAGE_NAME}
	pre-commit uninstall
	deactivate
	rm -rf .venv/