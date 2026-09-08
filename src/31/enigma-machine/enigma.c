#include "enigma.h"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

const char *USAGE = " <left_rotor> <middle_rotor> <right_rotor> <rings> <positions>";

void bad_input(const char *program, const char *message) {
  fprintf(stderr, "%s Usage: %s%s\n", message ? message : "", program, USAGE);
  exit(1);
}

void require_capital(char c) {
  if (c < 'A' || c > 'Z') {
    fprintf(stderr, "Invalid configuration %c\n", c);
    exit(1);
  }
}

void require_capitals(const char *text) {
  for (; *text; ++text) require_capital(*text);
}

void rotate(Enigma *machine) {
   if (notch(&machine->center)) {
     step(&machine->center);
     step(&machine->left);
  }
   else if (notch(&machine->right)) step(&machine->center);
   step(&machine->right);
}

int run(Enigma *machine, int value) {
   rotate(machine);
   value = machine->plugboard.wiring[value];
   value = fwd(&machine->right, value);
   value = fwd(&machine->center, value);
   value = fwd(&machine->left, value);
   value = machine->reflector.forward_wiring[value];
   value = rev(&machine->left, value);
   value = rev(&machine->center, value);
   value = rev(&machine->right, value);
   return machine->plugboard.wiring[value];
}

Enigma new(const char *left_name, const char *center_name, const char *right_name, const char *rings, const char *pairs[10], const char *positions) {
   const RotorSpec *left = get(left_name), *center = get(center_name), *right = get(right_name);
   Enigma machine = {
     build(left, rings[0] - 'A', positions[0] - 'A'), build(center, rings[1] - 'A', positions[1] - 'A'), build(right, rings[2] - 'A', positions[2] - 'A'), connect(pairs), refl_b()
  };
   return machine;
}

Enigma plain(const char *left_name, const char *center_name, const char *right_name, const char *rings, const char *positions) {
   const RotorSpec *left=get(left_name), *center=get(center_name), *right=get(right_name);
   Enigma machine={
     build(left,rings[0]-'A',positions[0]-'A'),build(center,rings[1]-'A',positions[1]-'A'),build(right,rings[2]-'A',positions[2]-'A'),identity(),refl_b()
  };
   return machine;
}

int cli(int argc, char **argv) {
   if (argc != 6 && argc != 16) bad_input(argv[0], "");
   if (!strcmp(argv[1], argv[2]) || !strcmp(argv[2], argv[3]) || !strcmp(argv[1], argv[3])) {
     fprintf(stderr, "A given rotor can only be used once.\n");
     return 1;
  }
   if (!get(argv[1]) || !get(argv[2]) || !get(argv[3])) {
     fprintf(stderr, "Invalid rotor. Valid rotors are:\n I\n II\n III\n IV\n V\n VI\n VII\n VIII\n");
     return 1;
  }
   if (argc == 6) {
     if (strlen(argv[4]) != 3 || strlen(argv[5]) != 3) bad_input(argv[0], "");
     require_capitals(argv[4]);
     require_capitals(argv[5]);
     Enigma machine = plain(argv[1], argv[2], argv[3], argv[4], argv[5]);
     int c;
     while ((c = getchar()) != EOF) {
       if (c >= 'A' && c <= 'Z') putchar(run(&machine, c - 'A') + 'A');
       else if (c == '\n' || c == ' ') putchar(c);
       else {
         fprintf(stderr, "Unexpected character %d '%c', can only encode capital letters.\n", c, c);
         return 255;
      }
    }
     return 0;
  }
   if (strlen(argv[4]) != 3 || strlen(argv[15]) != 3) bad_input(argv[0], "");
   require_capitals(argv[4]);
   require_capitals(argv[15]);
   bool used[26] = {
     false
  };
   const char *pairs[10];
   for (int i = 0; i < 10; ++i) {
     pairs[i] = argv[5 + i];
     if (strlen(pairs[i]) != 2) bad_input(argv[0], "");
     require_capitals(pairs[i]);
     for (int j = 0; j < 2; ++j) {
       int value = pairs[i][j] - 'A';
       if (used[value]) {
         fprintf(stderr, "Duplicate plug provided - plug letters must be unique.\n");
         return 1;
      }
       used[value] = true;
    }
  }
   Enigma machine = new(argv[1], argv[2], argv[3], argv[4], pairs, argv[15]);
   int c;
   while ((c = getchar()) != EOF) {
     if (c >= 'A' && c <= 'Z') putchar(run(&machine, c - 'A') + 'A');
     else if (c == '\n' || c == ' ') putchar(c);
     else {
       fprintf(stderr, "Unexpected character %d '%c', can only encode capital letters.\n", c, c);
       return 255;
    }
  }
   return 0;
}