#ifndef MSG_STORE_H
#define MSG_STORE_H

#include "contiki.h"
#include "net/ipv6/uip.h"

typedef struct attestation {
  uint16_t attest_node;
  struct attestation *next;
} attestation_t;

typedef struct message {
  uint32_t message_num;
  uint32_t attestation_count;
  attestation_t *attestations;
  attestation_t *attestations_tail;
  struct message *next;
} message_t;

void msg_store_init(void);
message_t* find_message(uint32_t message_num);
void add_attestation(message_t *msg, const uint16_t attest_node);
void add_message(uint32_t message_num);
void print_msg_store();

#endif
