MAKEFLAGS += --no-print-directory

.PHONY:	default
default: run-server

.PHONY: install
install: install-js install-py

.PHONY: clean
clean: clean-js clean-py


# client side
js-url	= https://cdn.jsdelivr.net
js-src	= npm/@xterm/xterm@5.5.0/css/xterm$(min).css		\
	  npm/@xterm/xterm@5.5.0/lib/xterm$(min).js		\
	  npm/@xterm/addon-fit@0.10.0/lib/addon-fit$(min).js	\
	  npm/sockjs-client@1.6.1/dist/sockjs$(min).js
js-min	= '' .min
curl	= curl --no-progress-meter -L

.PHONY: install-js
install-js:
	$(MAKE) clean-js
	for m in $(js-min); do				\
	    $(MAKE) _install-js-sub min=$$m || ! break;	\
	done

.PHONY: _install-js-sub
_install-js-sub:
	for js in $(js-src); do					\
	    echo "Installing: static/$$js";			\
	    mkdir -p $$(dirname static/$$js)      || ! break;	\
	    $(curl) -o static/$$js $(js-url)/$$js || ! break;	\
	done

.PHONY: clean-js
clean-js:
	rm -rf static


# server side
pyver	= 3.12
args	=

.PHONY:	run-server
run-server:
	PYTHONUSERBASE=$(PWD)/pyuser python$(pyver) brenda.py $(args)

.PHONY:	install-py
install-py:
	$(MAKE) clean-py
	PYTHONUSERBASE=$(PWD)/pyuser		\
	PIP_CACHE_DIR=$(PWD/)pyuser/cache	\
	pip$(pyver) install --user --no-cache-dir aiohttp sockjs

.PHONY:	clean-py
clean-py:
	rm -rf pyuser
