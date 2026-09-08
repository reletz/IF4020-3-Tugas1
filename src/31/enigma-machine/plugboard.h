#ifndef PLUGBOARD_H
#define PLUGBOARD_H

typedef struct {
  int wiring[26];
} Plugboard;

Plugboard connect(const char *pairs[10]);
Plugboard identity(void);

#endif