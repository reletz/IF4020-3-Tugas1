#include "reflector.h"

const char REFLECTOR_B[] = "YRUHQSLDPXNGOKMIEBFZCWVJAT";

Reflector refl_b(void) {
  Reflector reflector;

  for (int i = 0; i < 26; ++i) {
    reflector.forward_wiring[i] = REFLECTOR_B[i] - 'A';
  }

  return reflector;
}