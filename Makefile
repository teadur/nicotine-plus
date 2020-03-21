.PHONY: install lint mypy
.DEFAULT_GOAL := all

ifeq ($(PREFIX),)
    PREFIX := /usr/local
endif

SRC = nicotine.py pynicotine plugins

all: install lint mypy

install:
	poetry install

	install -d $(DESTDIR)$(PREFIX)/share/man/man1/
	install -m 644 manpages/nicotine.1 $(DESTDIR)$(PREFIX)/share/man/man1/
	install -d $(DESTDIR)$(PREFIX)/share/icons/hicolor/
	install -m 644 files/icons/ $(DESTDIR)$(PREFIX)/share/icons/hicolor/
	install -d $(DESTDIR)$(PREFIX)/share/applications/
	install -m 644 files/nicotine.desktop $(DESTDIR)$(PREFIX)/share/applications/
		install -d $(DESTDIR)$(PREFIX)/share/applications/
	install -m 644 files/nicotine.desktop $(DESTDIR)$(PREFIX)/share/applications/


lint:
	isort --recursive ${SRC}
	flake8 ${SRC} --ignore=E501,E402,W504,W503

mypy:
	mypy ${SRC}

image:
	docker build -t nicotine -f docker/Dockerfile.python3 --network=host .
