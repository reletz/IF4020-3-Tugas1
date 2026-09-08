#ifndef ROTOR_H
#define ROTOR_H

#include <stdbool.h>
#include <stddef.h>

typedef struct { const char *name; const char *wiring; const int *notches; size_t notch_count; } RotorSpec;
typedef struct { const char *name; int forward_wiring[26]; int backward_wiring[26]; bool notch_positions[26]; int ring_setting; int rotor_position; } Rotor;

Rotor build(const RotorSpec *,int,int);
int fwd(const Rotor *,int);
int rev(const Rotor *,int);
bool notch(const Rotor *);
void step(Rotor *);
const RotorSpec *get(const char *);

#endif