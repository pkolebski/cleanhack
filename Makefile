all: install_models

install_models:
	pip install -r requirements.txt -r requirements-dev.txt
	python -m spacy download en_core_web_lg