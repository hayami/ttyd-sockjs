.PHONY:	default
default: run-server

.PHONY: install
install: install-js install-py

.PHONY: clean
clean: clean-js clean-py


MAKEFLAGS += --no-print-directory


###
### client side
###
js-url	= https://cdn.jsdelivr.net
# Extract strings corresponding to ^^^: ="static/npm/------(.min).---"
#                                                ^^^^^^^^^^      ^^^^
js-src	= $(shell sed -E -n 's!.*="static/(npm/[^"]*)".*!\1!p'	\
	< main.html | sed -E 's/([.]min)?[.]([a-z]+)$$/$${min}.\2/')
js-min	= '' .min
js-map	= true
curl	= curl --no-progress-meter -L

.PHONY: install-js
install-js:
	$(MAKE) clean-js
	for m in $(js-min); do				\
	    $(MAKE) _install-js-sub min=$$m || ! break;	\
	done

.PHONY: _install-js-sub
_install-js-sub:
	@for js in $(js-src); do				\
	    echo "Installing: static/$$js";			\
	    mkdir -p $$(dirname static/$$js)      || ! break;	\
	    $(curl) -o static/$$js $(js-url)/$$js || ! break;	\
	    [ "$(js-map)" = "true" ] || continue;		\
	    case "$$js" in					\
	    *.min.js) ;;					\
	    *.js)						\
	        echo "Installing: static/$$js.map";		\
	        $(curl) -o static/$$js.map			\
	                $(js-url)/$$js.map || ! break ;;	\
	    esac;						\
	done

.PHONY: clean-js
clean-js:
	rm -rf static/npm


###
### server side
###
pyver	= 3.12
python	= python$(pyver)
env-lang= env -u LANGUAGE LANG=C.UTF-8 LC_ALL=C.UTF-8
run-args=

.PHONY:	run-server
run-server:
	$(env-lang) PYTHONUSERBASE=$(PWD)/pyuser \
	$(python) terminalserver.py $(run-args)

.PHONY:	install-py
install-py:
	$(MAKE) clean-py
	$(env-lang) PYTHONUSERBASE=$(PWD)/pyuser PIP_CACHE_DIR=$(PWD)/pipcache \
	$(python) -m pip install --user --no-cache-dir aiohttp sockjs

.PHONY:	clean-py
clean-py:
	rm -rf pyuser pipcache
