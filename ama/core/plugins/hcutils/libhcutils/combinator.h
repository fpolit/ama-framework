/*
 * combinator - hashcat-utils
 *
 * Maintainer: glozanoa <glozanoa@uni.pe>
 */

#ifndef _COMBINATOR_H
#define _COMBINATOR_H

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
#include <ctype.h>
#include <errno.h>
#include <fcntl.h>

#include "utils.h"

int combinator(char* wl1, char* wl2, char* out);
int combinator2stdout(char* wl1, char* wl2);

#endif //_COMBINATOR_H
