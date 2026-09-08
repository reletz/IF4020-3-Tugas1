CC ?= cc
CFLAGS ?= -O3 -std=c17 -Wall -Wextra -Wpedantic

.PHONY: all clean
all: machine encode
machine: machine.c enigma.c enigma.h rotor.c rotor.h plugboard.c plugboard.h reflector.c reflector.h
	$(CC) $(CFLAGS) machine.c enigma.c rotor.c plugboard.c reflector.c -o $@
encode: encode.c
	$(CC) $(CFLAGS) $< -o $@
clean:
	rm -f machine encode