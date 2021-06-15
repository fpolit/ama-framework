/*
 * combipow - hashcat utils
 *
 * Maintainer: glozanoa <glozanoa@uni.pe>
 */
#ifndef _COMBIPOW_H
#define _COMBIPOW_H

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <errno.h>
#include <inttypes.h>

int combipow2stdout(char* wl);
int combipow(char* wl, char* out);

#endif //_COMBIPOW_H
