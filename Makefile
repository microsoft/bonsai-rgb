.ONESHELL:

# https://blog.ianpreston.ca/conda/python/bash/2020/05/13/conda_envs.html

SHELL=bash
CONDA_ENV = ./conda
CONDA_ACTIVATE = eval "$$(conda shell.bash hook)"; conda activate $(CONDA_ENV); export PYTHONPATH=`pwd`:$${PYTHONPATH}

.PHONY: test clean run help

run: $(CONDA_ENV)
	$(CONDA_ACTIVATE); python main.py

clean:
	find . -type f -name "*.py[co]" -delete
	find . -type d -name "__pycache__" -delete
	rm -rf $(CONDA_ENV)
	docker rmi -f rgb 2&> /dev/null

test: $(CONDA_ENV)
	$(CONDA_ACTIVATE); python test.py

$(CONDA_ENV): $(CONDA_ENV)/touchfile

$(CONDA_ENV)/touchfile: requirements.txt environment.yml
	conda env create --force --prefix $(CONDA_ENV) --file environment.yml 
	touch $(CONDA_ENV)/touchfile

docker:
	docker build -t rgb .

lint:
	$(CONDA_ACTIVATE) rgb
	black main.py
