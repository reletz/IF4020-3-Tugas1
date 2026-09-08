#include "rotor.h"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

const int notch_i[] = {16};
const int notch_ii[] = {4};
const int notch_iii[] = {21};
const int notch_iv[] = {9};
const int notch_v[] = {25};
const int notch_vi[] = {12, 25};
const RotorSpec ROTOR_SPECS[] = {
   {
     "I", "EKMFLGDQVZNTOWYHXUSPAIBRCJ", notch_i, 1
  }
   , {
     "II", "AJDKSIRUXBLHWTMCQGZNPYFVOE", notch_ii, 1
  }
   , {
     "III", "BDFHJLCPRTXVZNYEIWGAKMUSQO", notch_iii, 1
  }
   , {
     "IV", "ESOVPZJAYQUIRHXLNFTGKDCMWB", notch_iv, 1
  }
   , {
     "V", "VZBRGITYUPSDNHLXAWMJQOFECK", notch_v, 1
  }
   , {
     "VI", "JPGVOUMFYQBENHZRDKASXLICTW", notch_vi, 2
  }
   , {
     "VII", "NZJHGRCXMYSWBOUFAIVLPEKQDT", notch_vi, 2
  }
   , {
     "VIII", "FKQHTLXOCBJSPDZRAMEWNIUYGV", notch_vi, 2
  }
   ,
};

int map(int value, int position, int ring, const int map[26]) {
   int shift = position - ring;
   return (map[(value + shift + 26) % 26] - shift + 26) % 26;
}

Rotor build(const RotorSpec *spec, int ring, int position) {
   Rotor rotor = {0};
   rotor.name = spec->name;
   rotor.ring_setting = ring;
   rotor.rotor_position = position;

   for (int i = 0; i < 26; ++i) {
     rotor.forward_wiring[i] = spec->wiring[i] - 'A';
  }
   for (int i = 0; i < 26; ++i) {
     rotor.backward_wiring[rotor.forward_wiring[i]] = i;
  }
   for (size_t i = 0; i < spec->notch_count; ++i) {
     rotor.notch_positions[spec->notches[i]] = true;
  }
   return rotor;
}

int fwd(const Rotor *rotor, int value) {
   return map(value, rotor->rotor_position, rotor->ring_setting, rotor->forward_wiring);
}

int rev(const Rotor *rotor, int value) {
   return map(value, rotor->rotor_position, rotor->ring_setting, rotor->backward_wiring);
}

bool notch(const Rotor *rotor) {
   return rotor->notch_positions[rotor->rotor_position];
}

void step(Rotor *rotor) {
   rotor->rotor_position = (rotor->rotor_position + 1) % 26;
}

const RotorSpec *get(const char *name) {
   for (size_t i = 0; i < sizeof(ROTOR_SPECS) / sizeof(ROTOR_SPECS[0]); ++i) {
     if (!strcmp(name, ROTOR_SPECS[i].name)) return &ROTOR_SPECS[i];
  }
   return NULL;
}