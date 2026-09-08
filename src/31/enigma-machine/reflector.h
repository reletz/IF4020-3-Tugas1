#ifndef REFLECTOR_H
#define REFLECTOR_H

typedef struct {
  int forward_wiring[26];
} Reflector;

Reflector refl_b(void);

#endif