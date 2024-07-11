CONTIKI_PROJECT = udp-p2p
PROJECT_SOURCEFILES += msg-cache.c msg-store.c

MAKE_ROUTING = MAKE_ROUTING_NULLROUTING

all: $(CONTIKI_PROJECT)
CFLAGS += -DPROJECT_CONF_H=\"project-conf.h\"

CONTIKI = ../..
include $(CONTIKI)/Makefile.include
