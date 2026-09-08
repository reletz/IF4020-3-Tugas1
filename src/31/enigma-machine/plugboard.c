#include "plugboard.h"

Plugboard connect(const char *pairs[10]) {
  Plugboard board;

  for (int i = 0; i < 26; ++i) {
    board.wiring[i] = i;
  }

  for (int i = 0; i < 10; ++i) {
    int left = pairs[i][0] - 'A';
    int right = pairs[i][1] - 'A';

    board.wiring[left] = right;
    board.wiring[right] = left;
  }

  return board;
}

Plugboard identity(void) {
  Plugboard board;

  for (int i = 0; i < 26; ++i) {
    board.wiring[i] = i;
  }

  return board;
}