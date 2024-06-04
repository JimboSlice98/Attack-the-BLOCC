#include "msg-cache.h"
#include <stdlib.h>
#include <string.h>

#include "sys/log.h"
#define LOG_MODULE "Node"
#define LOG_LEVEL LOG_LEVEL_INFO

/*---------------------------------------------------------------------------*/
static cached_message_t message_cache[CACHE_SIZE];
int cache_index = 0;
/*---------------------------------------------------------------------------*/
void
print_cache(void)
{
  LOG_INFO("Current cache entries:\n");
  for (int i = 0; i < CACHE_SIZE; i++) {
    LOG_INFO("  Entry %d: '%.*s'\n", i, message_cache[i].datalen,
             (char *)message_cache[i].data);
  }
}
/*---------------------------------------------------------------------------*/
int
is_duplicate(const uint8_t *data, uint16_t datalen)
{
  for (int i = 0; i < CACHE_SIZE; i++) {
    if (message_cache[i].datalen == datalen
        && memcmp(message_cache[i].data, data, datalen) == 0) {
      return 1;
    }
  }
  return 0;
}
/*---------------------------------------------------------------------------*/
void
add_to_cache(const uint8_t *data, uint16_t datalen)
{
  if (cache_index >= CACHE_SIZE) {
    cache_index = 0;
  }

  message_cache[cache_index].datalen = datalen;
  memcpy(message_cache[cache_index].data, data, datalen);
  cache_index++;
}
/*---------------------------------------------------------------------------*/
