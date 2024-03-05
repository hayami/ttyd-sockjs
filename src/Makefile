PYTHONUSERBASE	= $(PWD)/pyuser
PYVER	= 3.11

MAKEFLAGS += --no-print-directory

PHONY:	default
default: run

PHONY:	run
run:
	PYTHONUSERBASE=$(PYTHONUSERBASE) python$(PYVER) ttyd-sockjs.py

PHONY:	pip-install
pip-install:
	$(MAKE) clean
	PYTHONUSERBASE=$(PYTHONUSERBASE)	\
	PIP_CACHE_DIR=$(PYTHONUSERBASE)/cache	\
	pip$(PYVER) install --user --no-cache-dir aiohttp sockjs

PHONY:	clean
clean:
	rm -rf $(PYTHONUSERBASE)
