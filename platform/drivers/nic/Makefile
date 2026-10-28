CC ?= cc
CFLAGS ?= -O3 -march=native -Wall -Wextra -Wpedantic
DPDK_CFLAGS := $(shell pkg-config --cflags libdpdk 2>/dev/null)
DPDK_LIBS := $(shell pkg-config --libs libdpdk 2>/dev/null)

TARGET := nls-dpdk-forwarder
SRC := dpdk_forwarder.c

.PHONY: all clean check-dpdk

all: check-dpdk $(TARGET)

check-dpdk:
	@pkg-config --exists libdpdk || (echo "libdpdk development files are required on Ubuntu"; exit 1)

$(TARGET): $(SRC)
	$(CC) $(CFLAGS) $(DPDK_CFLAGS) -o $@ $< $(DPDK_LIBS)

clean:
	rm -f $(TARGET)
