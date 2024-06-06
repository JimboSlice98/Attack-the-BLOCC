#include "msg-cache.h"
#include <stdlib.h>
#include <string.h>
#include "sys/log.h"

#define LOG_MODULE "Node"
#define LOG_LEVEL LOG_LEVEL_INFO

CacheEntry **hash_table;
int hash_size = INITIAL_HASH_SIZE;
int cache_size = 0;

/*---------------------------------------------------------------------------*/
unsigned int
hash_function(const uint8_t *data, uint16_t datalen)
{
  unsigned int hash = 0;
  for (uint16_t i = 0; i < datalen; i++) {
    hash = (hash * 31) + data[i];
  }
  return hash % hash_size;
}
/*---------------------------------------------------------------------------*/
// void
// rehash()
// {
//   int old_hash_size = hash_size;
//   hash_size *= 2; // Double the hash table size
//   CacheEntry **new_hash_table = (CacheEntry **)calloc(hash_size, sizeof(CacheEntry *));
//   CacheEntry *entry;
  
//   // Rehash all existing entries
//   for (int i = 0; i < old_hash_size; i++) {
//     entry = hash_table[i];
//     while (entry != NULL) {
//       CacheEntry *next = entry->next;
//       unsigned int new_index = hash_function(entry->data, entry->datalen);
//       entry->next = new_hash_table[new_index];
//       new_hash_table[new_index] = entry;
//       entry = next;
//     }
//   }
  
//   free(hash_table);
//   hash_table = new_hash_table;
// }
/*---------------------------------------------------------------------------*/
void
print_cache(void)
{
  LOG_INFO("Current cache entries:\n");
  for (int i = 0; i < hash_size; i++) {
    CacheEntry *entry = hash_table[i];
    while (entry != NULL) {
      LOG_INFO("  Entry: '%.*s'\n", entry->datalen, (char *)entry->data);
      entry = entry->next;
    }
  }
}
/*---------------------------------------------------------------------------*/
int
is_duplicate(const uint8_t *data, uint16_t datalen)
{
  unsigned int index = hash_function(data, datalen);
  CacheEntry *entry = hash_table[index];
  while (entry != NULL) {
    if (entry->datalen == datalen && memcmp(entry->data, data, datalen) == 0) {
      return 1;
    }
    entry = entry->next;
  }
  return 0;
}
/*---------------------------------------------------------------------------*/
void
add_to_cache(const uint8_t *data, uint16_t datalen)
{
  if (cache_size >= CACHE_SIZE) {
    // Remove the oldest entry in a simple round-robin manner
    static int round_robin_index = 0;
    while (hash_table[round_robin_index] == NULL) {
      round_robin_index = (round_robin_index + 1) % hash_size;
    }
    CacheEntry *old_entry = hash_table[round_robin_index];
    hash_table[round_robin_index] = old_entry->next;
    free(old_entry);
    cache_size--;
  }

  // if ((float)cache_size / hash_size > LOAD_FACTOR_THRESHOLD) {
  //   rehash();
  // }

  unsigned int index = hash_function(data, datalen);
  CacheEntry *new_entry = (CacheEntry *)malloc(sizeof(CacheEntry));
  if (new_entry == NULL) {
    LOG_ERR("Memory allocation failed\n");
    return;
  }
  memcpy(new_entry->data, data, datalen);
  new_entry->datalen = datalen;
  new_entry->next = hash_table[index];
  hash_table[index] = new_entry;
  cache_size++;
}
/*---------------------------------------------------------------------------*/
__attribute__((constructor))
void
initialize_hash_table()
{
  hash_table = (CacheEntry **)calloc(hash_size, sizeof(CacheEntry *));
  if (hash_table == NULL) {
    LOG_ERR("Memory allocation for hash table failed\n");
  }
}
/*---------------------------------------------------------------------------*/
