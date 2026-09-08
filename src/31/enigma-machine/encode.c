#include <ctype.h>
#include <stdio.h>

void emit(char c, int *letters) {
  putchar(c);
  ++*letters;
  if (*letters % 4 == 0) putchar(' ');
  if (*letters % 40 == 0) putchar('\n');
}

int main(void) {
  int c, letters = 0;

  while ((c = getchar()) != EOF) {
    c = toupper((unsigned char) c);
    if (c >= 'A' && c <= 'Z') emit((char) c, &letters);
  }

  if (letters % 40) putchar('\n');
  return 0;
}