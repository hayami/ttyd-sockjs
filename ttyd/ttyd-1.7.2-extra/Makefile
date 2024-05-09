V	= 1.7.2
ORIGTGZ	= https://github.com/tsl0922/ttyd/archive/refs/tags/$(V).tar.gz
DIR	= ../ttyd-$(V)/html

UMASK	= $(shell umask)
FMODE	= $(shell awk 'END {printf("0%o", and(0644, compl(0$(UMASK))))}' < /dev/null)

ifeq ($(build),all)
YARN_RUN_TARGET = build
else
YARN_RUN_TARGET = inline
endif

MAKEFLAGS += --no-print-directory


.PHONY:	default
default: both-inline.html

.PHONY:	both-inline.html
both-inline.html:
	$(MAKE) $(DIR)/extra/inline-websocket.html
	$(MAKE) $(DIR)/extra/inline-sockjs.html

.PHONY:	clean
clean:
	rm -rf ../ttyd-$(V)

.PHONY:	distclean
distclean: clean
	rm -f ../ttyd-$(V).tar.gz
	rm -rf ../ttyd-$(V)-yarn.cache

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

$(DIR)/extra/patch-0xx.applied: ../ttyd-$(V)
	$(MAKE) files='patch-0*' patch
	mkdir -p $(@D)
	touch $@

$(DIR)/extra/yarn.install.done: $(DIR)/extra/patch-0xx.applied
	install -m $(FMODE) dot.yarnrc $(DIR)/.yarnrc
	sed -i.orig 's#^\(cache-folder\) .*#\1 ../../ttyd-$(V)-yarn.cache#' $(DIR)/.yarnrc
	cd $(DIR) && yarn install
	mkdir -p $(@D)
	touch $@

$(DIR)/extra/inline-websocket.html: $(DIR)/extra/yarn.install.done
	[ ! -f $(DIR)/extra/patch-1xx.applied ]
	cd $(DIR) && yarn run $(YARN_RUN_TARGET)
	install -m $(FMODE) $(DIR)/dist/inline.html $@

$(DIR)/extra/patch-1xx.applied: $(DIR)/extra/yarn.install.done
	$(MAKE) files='patch-1*' patch
	install -m $(FMODE) ttyd-sockjs.js $(DIR)/src/components/terminal/
	touch $@

$(DIR)/extra/inline-sockjs.html: $(DIR)/extra/yarn.install.done $(DIR)/extra/patch-1xx.applied
	[ -f $(DIR)/extra/patch-1xx.applied ]
	cd $(DIR) && yarn run $(YARN_RUN_TARGET)
	install -m $(FMODE) $(DIR)/dist/inline.html $@
