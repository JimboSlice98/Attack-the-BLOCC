#include "contiki.h"
#include "lib/memb.h"
#include "lib/list.h"
#include "msg-cache.h"
#include <string.h>

#include "sys/log.h"
#define LOG_MODULE "App"
#define LOG_LEVEL LOG_LEVEL_INFO

typedef struct {
  uint8_t data[MAX_MSG_LEN];
  uint16_t datalen;
} message_t;

/*---------------------------------------------------------------------------*/
MEMB(message_cache_memb, message_t, CACHE_SIZE);
LIST(message_cache);

/*---------------------------------------------------------------------------*/
void
message_cache_init(void)
{
  memb_init(&message_cache_memb);
  list_init(message_cache);
}

/*---------------------------------------------------------------------------*/
int
is_duplicate(const uint8_t *data, uint16_t datalen)
{
  message_t *msg;
  LOG_INFO("Rx: '%.*s'\n", datalen, (char *) data);
  for(msg = list_head(message_cache); msg != NULL; msg = list_item_next(msg)) {
    LOG_INFO("  Cx: '%.*s'\n", msg->datalen, (char *) msg->data);
    if(msg->datalen == datalen && memcmp(msg->data, data, datalen) == 0) {
      LOG_INFO("Duplicate found\n");
      return 1;
    }
  }
  return 0;
}

/*---------------------------------------------------------------------------*/
void
print_cache(void)
{
  message_t *msg;
  int index = 0;
  LOG_INFO("Current cache entries:\n");
  for(msg = list_head(message_cache); msg != NULL; msg = list_item_next(msg)) {
    LOG_INFO("  Entry %d: '%.*s'\n", index, msg->datalen, (char *)msg->data);
    index++;
  }
  if(index == 0) {
    LOG_INFO("  Cache is empty\n");
  }
}

/*---------------------------------------------------------------------------*/
void
add_to_cache(const uint8_t *data, uint16_t datalen)
{
  if(datalen >= MAX_MSG_LEN) {
    LOG_ERR("Message too long to cache\n");
    return;
  }

  if(list_length(message_cache) >= CACHE_SIZE) {
    message_t *oldest_msg = list_chop(message_cache);
    if (oldest_msg != NULL) {
      memb_free(&message_cache_memb, oldest_msg);
    }
  }
  
  message_t *msg = memb_alloc(&message_cache_memb);
  if(msg != NULL) {
    memset(msg->data, 0, MAX_MSG_LEN);
    memcpy(msg->data, data, datalen);
    msg->datalen = datalen;
    list_add(message_cache, msg);
    LOG_INFO("Added to cache: '%.*s'\n", datalen, (char *)data);
    print_cache();
  } else {
    LOG_ERR("Failed to allocate memory for message\n");
  }
}
