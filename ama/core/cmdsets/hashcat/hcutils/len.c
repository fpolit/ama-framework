#define _GNU_SOURCE
#define _FILE_OFFSET_BITS 64
#define __MSVCRT_VERSION__ 0x0700

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
#include <ctype.h>
#include <errno.h>
#include <fcntl.h>


/**
 * Name........: len
 * Autor.......: Jens Steube <jens.steube@gmail.com>
 * License.....: MIT
 */

int len(int min, int max, char* infile, char* outfile)
{

  FILE *in;
  FILE *out;

  #ifdef _WINDOWS
  _setmode (_fileno (stdin), _O_BINARY);
  #endif

  if (min > max)
  {
    fprintf (stderr, "min > max\n");

    return (-1);
  }

  char line_buf[BUFSIZ];

  int line_len;

  while ((line_len = fgetl (stdin, BUFSIZ, line_buf)) != -1)
  {
    if (line_len == 0) continue;

    if (line_len < min) continue;
    if (line_len > max) continue;

    puts (line_buf);
  }

  return 0;
}
