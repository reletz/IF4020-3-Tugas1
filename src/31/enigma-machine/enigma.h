#ifndef ENIGMA_H
#define ENIGMA_H

#include "plugboard.h"
#include "reflector.h"
#include "rotor.h"

typedef struct { Rotor left; Rotor center; Rotor right; Plugboard plugboard; Reflector reflector; } Enigma;

Enigma new(const char *,const char *,const char *,const char *,const char *[10],const char *);
Enigma plain(const char *,const char *,const char *,const char *,const char *);
int run(Enigma *,int);
int cli(int,char **);

#endif