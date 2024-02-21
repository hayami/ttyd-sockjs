V	= 1.7.2
ORIGTGZ	= https://github.com/tsl0922/ttyd/archive/refs/tags/$(V).tar.gz
DIR	= ../ttyd-$(V)/html

MAKEFLAGS += --no-print-directory

.PHONY:	default
default: yarn-build

.PHONY:	yarn-install
yarn-install: $(DIR)/yarn.install.done

.PHONY:	yarn-build
yarn-build: $(DIR)/dist/inline.html

.PHONY:	yarn-build-all
yarn-build-all: $(DIR)/../src/html.h

.PHONY:	patch
patch:
	@set -e;					\
	echo "patch files to be applied:" $(files);	\
	for f in $(files); do				\
	    test -f "$$f" || continue;			\
	    (cd $(DIR) && patch -p1) < "$$f";		\
	done

../ttyd-$(V).tar.gz:
	curl -o $@ -L $(ORIGTGZ)

../ttyd-$(V): ../ttyd-$(V).tar.gz
	cd .. && tar -xpzf ttyd-$(V).tar.gz
	cd $@ && chmod -R go-rwxst . && chmod -R a+rX .
	cd $@ && find . -name '.git*' -exec rm -rf {} +

$(DIR)/yarn.install.done: ../ttyd-$(V)
	cat dot.yarnrc > $(DIR)/.yarnrc
	$(MAKE) files='patch-0*' patch
	cd $(DIR) && yarn install
	$(MAKE) files='patch-1*' patch
	touch $@

$(DIR)/src/components/terminal/ttyd-sockjs.js: $(DIR)/yarn.install.done
	test -f $@ || $(MAKE) files='patch-2*' patch
	cat ttyd-sockjs.js > $@

$(DIR)/dist/inline.html: $(DIR)/src/components/terminal/ttyd-sockjs.js
	cd $(DIR) && yarn run inline

$(DIR)/../src/html.h: $(DIR)/src/components/terminal/ttyd-sockjs.js
	cd $(DIR) && yarn run build

.PHONY: distclean
distclean:
	rm -rf ../ttyd-$(V)
	rm -f ../ttyd-$(V).tar.gz
