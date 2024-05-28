CONTIKI_PROJECT = udp-p2p
PROJECT_SOURCEFILES += msg-cache.c

all: $(CONTIKI_PROJECT)

CONTIKI = ../..
include $(CONTIKI)/Makefile.include
CFLAGS += -DUIP_CONF_TCP=1
