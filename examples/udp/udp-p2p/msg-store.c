#include "msg-store.h"
#include <stdlib.h>
#include <string.h>

#include "sys/log.h"
#define LOG_MODULE "Node"
#define LOG_LEVEL LOG_LEVEL_INFO

/*---------------------------------------------------------------------------*/
static message_t *messages_head = NULL;
static message_t *messages_tail = NULL;
/*---------------------------------------------------------------------------*/
message_t*
find_message(uint32_t message_num)
{
  message_t *current = messages_head;
  while (current != NULL) {
    if (current->message_num == message_num) {
      return current;
    }
    current = current->next;
  }
  return NULL;
}
/*---------------------------------------------------------------------------*/
void
add_attestation(message_t *msg, const uint16_t attest_node)
{
  attestation_t *new_attestation = (attestation_t *)malloc(sizeof(attestation_t));
  if (new_attestation != NULL) {
    new_attestation->attest_node = attest_node;
    new_attestation->next = NULL;

    if (msg->attestations_tail == NULL) {
      msg->attestations = new_attestation;
      msg->attestations_tail = new_attestation;
    } else {
      msg->attestations_tail->next = new_attestation;
      msg->attestations_tail = new_attestation;
    }

    msg->attestation_count++;
  } else {
    LOG_ERR("Failed to allocate memory for attestation\n");
  }
}
/*---------------------------------------------------------------------------*/
void
add_message(uint32_t message_num)
{ 
  message_t *new_message = (message_t *)malloc(sizeof(message_t));
  if (new_message != NULL) {
    new_message->message_num = message_num;
    new_message->attestation_count = 0;
    new_message->attestations = NULL;
    new_message->attestations_tail = NULL;
    new_message->next = NULL;
    
    if (messages_tail == NULL) {
      messages_head = new_message;
      messages_tail = new_message;
    } else {
      messages_tail->next = new_message;
      messages_tail = new_message;
    }
  } else {
    LOG_ERR("Failed to allocate memory for message\n");
  }
}
/*---------------------------------------------------------------------------*/
void
print_msg_store(void)
{
  message_t *msg = messages_head;
  LOG_INFO("Current messages in store:\n");
  if (msg == NULL) {
    LOG_INFO("  Message store is empty\n");
    return;
  }
  while (msg != NULL) {
    LOG_INFO("  Message=%u, Attestations=%u\n", 
             msg->message_num, msg->attestation_count);

    attestation_t *att = msg->attestations;
    int att_index = 0;
    while (att != NULL) {
      LOG_INFO("    Attestation %d: attest_node=%hu\n", att_index, att->attest_node);
      att = att->next;
      att_index++;
    }

    msg = msg->next;
  }
}
/*---------------------------------------------------------------------------*/
