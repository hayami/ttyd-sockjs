PYTHONUSERBASE	= $(PWD)/pybase

MAKEFLAGS += --no-print-directory

PHONY:	default
default: run

PHONY:	run
run:
	PYTHONUSERBASE=$(PYTHONUSERBASE) python3 ttyd-sockjs.py

PHONY:	pip-install
pip-install:
	$(MAKE) clean
	curl -L -O https://bootstrap.pypa.io/pip/pip.pyz
	PYTHONUSERBASE=$(PYTHONUSERBASE)	\
	PIP_CACHE_DIR=$(PYTHONUSERBASE)/cache	\
	python3 pip.pyz install --user --no-cache-dir aiohttp sockjs

PHONY:	clean
clean:
	rm -f pip.pyz
	rm -rf $(PYTHONUSERBASE)
