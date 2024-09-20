MAKEFLAGS += --no-print-directory

.PHONY:	default
default: run-server

.PHONY: install
install: install-js install-py

.PHONY: clean
clean: clean-js clean-py


# client side
js-url	= https://cdn.jsdelivr.net
js-src	= npm/@xterm/xterm@5.5.0/css/xterm{min}css		\
	  npm/@xterm/xterm@5.5.0/lib/xterm{min}js		\
	  npm/@xterm/addon-fit@0.10.0/lib/addon-fit{min}js	\
	  npm/sockjs-client@1.6.1/dist/sockjs{min}js
js-min	= '' .min
static	= $(PWD)/static

install-js: clean-js
	$(MAKE) clean-js
	for i in $(js-src); do					\
	    for m in $(js-min); do				\
	        im=$$(echo $$i | sed "s/{min}/$${m}./");	\
	        out=$(static)/$$im;				\
	        mkdir -p $$(dirname $$out)	|| ! break;	\
	        echo "install: $$out";				\
	        curl -L -o $$out $(js-url)/$$im	|| ! break;	\
	    done;						\
	done

clean-js:
	rm -rf $(static)


# server side
pyuser	= $(PWD)/pyuser
pyver	= 3.12
args	=

.PHONY:	run-server
run-server:
	PYTHONUSERBASE=$(pyuser) python$(pyver) brenda.py $(args)

.PHONY:	install-py
install-py:
	$(MAKE) clean-py
	PYTHONUSERBASE=$(pyuser)	\
	PIP_CACHE_DIR=$(pyuser)/cache	\
	pip$(pyver) install --user --no-cache-dir aiohttp sockjs

.PHONY:	clean-py
clean-py:
	rm -rf $(pyuser)
