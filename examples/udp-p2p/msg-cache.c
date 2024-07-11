#include "msg-cache.h"
#include <stdlib.h>
#include <string.h>
#include "sys/node-id.h"
#include "sys/log.h"

#define LOG_MODULE "Node"
#define LOG_LEVEL LOG_LEVEL_INFO

CacheEntry **hash_table;
int hash_size = HASH_SIZE;
int cache_size = 0;

/*---------------------------------------------------------------------------*/
unsigned int
hash_function(uint32_t message_num, uint16_t origin_node, uint16_t attest_node)
{
  unsigned int hash = message_num;
  hash = (hash * 31) + origin_node;
  hash = (hash * 31) + attest_node;
  return hash % hash_size;
}
/*---------------------------------------------------------------------------*/
void
initialise_cache()
{
  hash_table = (CacheEntry **)calloc(hash_size, sizeof(CacheEntry *));
  if (hash_table == NULL) {
    LOG_ERR("Memory allocation for hash table failed\n");
  }
}
/*---------------------------------------------------------------------------*/
void
print_cache(void)
{
  LOG_INFO("Current cache entries:\n");
  for (int i = 0; i < hash_size; i++) {
    CacheEntry *entry = hash_table[i];
    while (entry != NULL) {
      LOG_INFO("  Entry: msg_num: %u, origin_node: %u, attest_node: %u, time: %lu\n",
               entry->message_num, entry->origin_node, entry->attest_node, entry->time_of_broadcast);
      entry = entry->next;
    }
  }
}
/*---------------------------------------------------------------------------*/
int
is_duplicate(uint32_t message_num, uint16_t origin_node, uint16_t attest_node)
{
  // LOG_INFO("CHECKING: %u|%u|%u\n", message_num, origin_node, attest_node);
  // print_cache();
  unsigned int index = hash_function(message_num, origin_node, attest_node);
  CacheEntry *entry = hash_table[index];
  while (entry != NULL) {
    if ((entry->message_num == message_num) && 
        (entry->origin_node == origin_node) &&
        (entry->attest_node == attest_node)) {
          // LOG_INFO("MATCH: %u|%u|%u\n", entry->message_num, entry->origin_node, entry->attest_node);
      return 1;
    }
    entry = entry->next;
  }
  return 0;
}
/*---------------------------------------------------------------------------*/
int
within_grace(clock_time_t time_of_broadcast)
{
  clock_time_t current_time = clock_time();
  int32_t time_difference = (int32_t)(current_time - time_of_broadcast);

  // if (abs(time_difference) <= (int32_t)GRACE_TIME) {
  //   return 1;
  // }
  // LOG_INFO("Current: %lu, Broadcast: %lu, Diff: %d, Grace: %lu\n",
  //          (unsigned long)current_time, (unsigned long)time_of_broadcast, (int)time_difference, (unsigned long)GRACE_TIME);
  // return 0;
  return (abs(time_difference) <= (int32_t)GRACE_TIME);
}
/*---------------------------------------------------------------------------*/
void
add_to_cache(uint32_t message_num, uint16_t origin_node, uint16_t attest_node, clock_time_t time_of_broadcast)
{
  // LOG_INFO("ADDING TO CACHE: %u|%u|%u|%lu\n", message_num, origin_node, attest_node, time_of_broadcast);
  unsigned int index = hash_function(message_num, origin_node, attest_node);
  CacheEntry *entry = hash_table[index];
  CacheEntry *prev = NULL;

  while (entry != NULL) {
    if (clock_time() - entry->time_of_broadcast > GRACE_TIME) {
      if (prev == NULL) {
        hash_table[index] = entry->next;
      } else {
        prev->next = entry->next;
      }
      CacheEntry *expired_entry = entry;
      entry = entry->next;
      free(expired_entry);
      cache_size--;
    } else {
      prev = entry;
      entry = entry->next;
    }
  }

  CacheEntry *new_entry = (CacheEntry *)malloc(sizeof(CacheEntry));
  if (new_entry == NULL) {
    LOG_ERR("Memory allocation failed\n");
    return;
  }
  new_entry->message_num = message_num;
  new_entry->origin_node = origin_node;
  new_entry->attest_node = attest_node;
  new_entry->time_of_broadcast = time_of_broadcast;
  new_entry->next = hash_table[index];
  hash_table[index] = new_entry;
  cache_size++;
}
/*---------------------------------------------------------------------------*/
