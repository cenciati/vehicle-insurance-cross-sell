# variables
PYTHON := python3
PIP := pip3

# prints an informative panel
help:
	@echo "~~~~~~~~~~~~~~~~~HELP~~~~~~~~~~~~~~~~~~"
	@echo "setup : prepares the environment."
	@echo "run : to run the project."
	@echo "clean : cleans the environment created."
	@echo "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"

# prepares the environment
setup:
	docker image build -t restapi:latest .
	docker container run --name restapi_vehicle_insurance -p 8000:80 -d restapi
	${PYTHON} -m venv .venv && source .venv/bin/activate
	${PIP} install --upgrade pip
	${PIP} install -r requirements.txt
	pre-commit install

# runs the api handler
run:
	${PYTHON} src/api/handler.py

# cleans the environment
clean:
	docker container stop restapi
	docker container rm restapi
	deactivate
	rm -rf .venv/