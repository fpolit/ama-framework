#ifndef _UTILS_H
#define _UTILS_H

typedef unsigned int uint;
int super_chop (char *s, const int len_orig);
int fgetl (FILE *fd, const size_t sz, char *buf);

#ifdef _WINDOWS
uint get_random_num (const uint min, const uint max);
#else
uint get_random_num (const uint min, const uint max);
#endif

#endif //_UTILS_H
