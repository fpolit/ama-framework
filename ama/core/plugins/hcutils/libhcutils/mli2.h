/*
 * header file to wrap mli2 hashcat utility
*/

#ifndef _MLI2_H
#define _MLI2_H

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
#include <ctype.h>
#include <errno.h>
#include <fcntl.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <unistd.h>

#include "utils.h"

int mli2stdout(char* infile, char* mergefile);

#endif //_MLI2_H
