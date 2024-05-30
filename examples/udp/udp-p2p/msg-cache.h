#ifndef MSG_CACHE_H
#define MSG_CACHE_H

#include <stdint.h>
#include "contiki.h"

#define MAX_MSG_LEN 64
#define CACHE_SIZE 16

void message_cache_init(void);
int is_duplicate(const uint8_t *data, uint16_t datalen);
void add_to_cache(const uint8_t *data, uint16_t datalen);

#endif
