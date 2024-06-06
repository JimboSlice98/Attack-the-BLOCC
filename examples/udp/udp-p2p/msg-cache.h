#ifndef MSG_CACHE_H
#define MSG_CACHE_H

#include <stdint.h>
#include "contiki.h"

#define MAX_MSG_LEN 64
#define CACHE_SIZE 2000
#define INITIAL_HASH_SIZE 20011
#define LOAD_FACTOR_THRESHOLD 0.75

typedef struct CacheEntry {
  uint8_t data[MAX_MSG_LEN];
  uint16_t datalen;
  struct CacheEntry *next;
} CacheEntry;

void print_cache(void);
int is_duplicate(const uint8_t *data, uint16_t datalen);
void add_to_cache(const uint8_t *data, uint16_t datalen);

#endif /* MSG_CACHE_H */
