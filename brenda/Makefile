MAKEFLAGS += --no-print-directory

.PHONY:	default
default: run-server

#https://github.com/xtermjs/xterm.js/archive/refs/tags/5.5.0.tar.gz
#https://cdn.jsdelivr.net/npm/@xterm/xterm@5.5.0/lib/xterm.js
#https://cdn.jsdelivr.net/npm/@xterm/xterm@5.5.0/css/xterm.css

xtermjs-version	= 5.5.0
xtermjs-url	= https://cdn.jsdelivr.net/npm/@xterm/xterm@$(xtermjs-version)
xterm-files	= lib/xterm.js lib/xterm.min.js \
		  css/xterm.css css/xterm.min.css

install-xtermjs:
	rm -rf xterm@$(xtermjs-version)
	for f in $(xterm-files); do			\
	    outfile=@xterm/xterm@$(xtermjs-version)/$$f;\
	    url=$(xtermjs-url)/$$f;			\
	    mkdir -p $$(dirname $$outfile) || ! break;	\
	    curl -L -o $$outfile $$url     || ! break;	\
	done



pyuser	= $(PWD)/pyuser
pyver	= 3.12
args	= --host 127.0.0.1

.PHONY:	run-server
run-server:
	PYTHONUSERBASE=$(pyuser) python$(pyver) brenda.py $(args)

.PHONY:	install-aiohttp+sockjs
install-aiohttp+sockjs:
	$(MAKE) clean
	PYTHONUSERBASE=$(pyuser)	\
	PIP_CACHE_DIR=$(pyuser)/cache	\
	pip$(pyver) install --user --no-cache-dir aiohttp sockjs

.PHONY:	clean
clean:
	rm -rf $(pyuser)
