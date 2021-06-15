/*
 * combinator3 - hashcat utils
 *
 * Maintainer: glozanoa <glozanoa@uni.pe>
 */

#ifndef _COMBINATOR3_H
#define _COMBINATOR3_H

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
#include <ctype.h>
#include <errno.h>
#include <fcntl.h>

#include "utils.h"

int combinator32stdout(char* wl1, char* wl2, char* wl3);
int combinator3(char* wl1, char* wl2, char* wl3, char* out);

#endif //_COMBINATOR3_H
