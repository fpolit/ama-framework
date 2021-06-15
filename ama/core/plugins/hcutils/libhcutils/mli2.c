#include "mli2.h"
#define _GNU_SOURCE
#define _FILE_OFFSET_BITS 64
#define __MSVCRT_VERSION__ 0x0700

/**
 * Name........: mli2
 * Autor.......: Jens Steube <jens.steube@gmail.com>
 * License.....: MIT
 */

static int cmp_cache (const void *p1, const void *p2)
{
  return strcmp (p1, p2);
}

int mli2stdout(char* infile, char* mergefile)
{
  FILE *fd1;
  FILE *fd2;

  /* if (argc != 3) */
  /* { */
  /*   fprintf (stderr, "usage: %s infile mergefile\n", argv[0]); */

  /*   return (-1); */
  /* } */

  if ((fd1 = fopen (infile, "rb")) == NULL)
  {
    fprintf (stderr, "%s: %s\n", infile, strerror (errno));

    return (-1);
  }

  if ((fd2 = fopen (mergefile, "rb")) == NULL)
  {
    fprintf (stderr, "%s: %s\n", mergefile, strerror (errno));

    fclose (fd1);

    return (-1);
  }

  char line_buf1[BUFSIZ];
  char line_buf2[BUFSIZ];

  if (fgetl (fd1, BUFSIZ, line_buf1) == -1) memset (line_buf1, 0, BUFSIZ);
  if (fgetl (fd2, BUFSIZ, line_buf2) == -1) memset (line_buf2, 0, BUFSIZ);

  int comp = 1;

  while (!feof (fd1) && !feof (fd2))
  {
    comp = cmp_cache (line_buf1, line_buf2);

    if (comp == 0)
    {
      puts (line_buf1);

      if (fgetl (fd1, BUFSIZ, line_buf1) == -1) memset (line_buf1, 0, BUFSIZ);
      if (fgetl (fd2, BUFSIZ, line_buf2) == -1) memset (line_buf2, 0, BUFSIZ);
    }
    else if (comp > 0)
    {
      puts (line_buf2);

      if (fgetl (fd2, BUFSIZ, line_buf2) == -1) memset (line_buf2, 0, BUFSIZ);
    }
    else if (comp < 0)
    {
      puts (line_buf1);

      if (fgetl (fd1, BUFSIZ, line_buf1) == -1) memset (line_buf1, 0, BUFSIZ);
    }
  }

  if (!feof (fd1) && comp == 0) puts (line_buf1);
  if (!feof (fd2) && comp == 0) puts (line_buf2);

  if (comp > 0) puts (line_buf1);

  while (!feof (fd1))
  {
    if (fgetl (fd1, BUFSIZ, line_buf1) == -1)
    {
      memset (line_buf1, 0, BUFSIZ);

      continue;
    }

    puts (line_buf1);
  }

  while (!feof (fd2))
  {
    if (fgetl (fd2, BUFSIZ, line_buf2) == -1)
    {
      memset (line_buf2, 0, BUFSIZ);

      continue;
    }

    puts (line_buf2);
  }

  fclose (fd1);
  fclose (fd2);

  return 0;
}
