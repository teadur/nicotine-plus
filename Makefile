.PHONY: install lint mypy
.DEFAULT_GOAL := all

ifeq ($(PREFIX),)
    PREFIX := /usr/local
endif

SRC = nicotine.py pynicotine plugins

all: install lint mypy

install:
	poetry install

lint:
	isort --recursive ${SRC}
	flake8 ${SRC} --ignore=E501,E402,W504,W503

mypy:
	mypy ${SRC}

image:
	docker build -t nicotine -f docker/Dockerfile.python3 --network=host .
