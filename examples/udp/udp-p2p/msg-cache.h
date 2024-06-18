#ifndef MSG_CACHE_H
#define MSG_CACHE_H

#include <stdint.h>
#include "contiki.h"

#define MAX_MSG_LEN 64
#define HASH_SIZE 20011
// #define HASH_SIZE 207
#define GRACE_TIME (5 * CLOCK_SECOND) // Define the grace time as 5 seconds

typedef struct CacheEntry {
  uint32_t message_num;
  uint16_t origin_node;
  uint16_t attest_node;
  clock_time_t time_of_broadcast;
  struct CacheEntry *next;
} CacheEntry;

void initialise_cache();
void print_cache(void);
int is_duplicate(uint32_t message_num, uint16_t origin_node, uint16_t attest_node);
int within_grace(clock_time_t time_of_broadcast);
void add_to_cache(uint32_t message_num, uint16_t origin_node, uint16_t attest_node, clock_time_t time_of_broadcast);

#endif /* MSG_CACHE_H */
