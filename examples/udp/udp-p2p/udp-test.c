#include "contiki.h"
#include "contiki-net.h"
#include "net/ipv6/uip-ds6.h"
#include "net/ipv6/simple-udp.h"
#include "net/ipv6/uip-debug.h"
#include <stdio.h>
#include <string.h>
#include <stdlib.h>

#define UDP_PORT 1234
#define BASE_INTERVAL (10 * CLOCK_SECOND)
#define RANDOM_INTERVAL (5 * CLOCK_SECOND) // Random interval between 0 and 5 seconds

typedef struct {
  char content[100];
} custom_message_t;

static struct simple_udp_connection udp_conn;

PROCESS(example_process, "Example process");
AUTOSTART_PROCESSES(&example_process);

static void udp_rx_callback(struct simple_udp_connection *c, const uip_ipaddr_t *sender_addr,
                            uint16_t sender_port, const uip_ipaddr_t *receiver_addr,
                            uint16_t receiver_port, const uint8_t *data, uint16_t datalen) {
  custom_message_t *msg = (custom_message_t *)data;
  printf("Received message: %s from ", msg->content);
  uip_debug_ipaddr_print(sender_addr);
  printf("\n");
}

PROCESS_THREAD(example_process, ev, data)
{
  static struct etimer timer;
  static uip_ipaddr_t dest_ipaddr;
  static custom_message_t msg;
  clock_time_t next_interval;

  PROCESS_BEGIN();

  simple_udp_register(&udp_conn, UDP_PORT, NULL, UDP_PORT, udp_rx_callback);

  // Set up the destination address
  uip_ip6addr(&dest_ipaddr, 0xfe80, 0, 0, 0, 0x203, 0x3, 0x3, 0x3);
  strcpy(msg.content, "Hello, this is a directed message!");

  // Set the initial timer
  next_interval = BASE_INTERVAL + (random_rand() % RANDOM_INTERVAL);
  etimer_set(&timer, next_interval);

  while(1) {
    PROCESS_WAIT_EVENT_UNTIL(etimer_expired(&timer));

    // Send the message to the specific node
    printf("Sending message to ");
    uip_debug_ipaddr_print(&dest_ipaddr);
    printf("\n");
    simple_udp_sendto(&udp_conn, &msg, sizeof(custom_message_t), &dest_ipaddr);

    // Reset the timer with randomness
    next_interval = BASE_INTERVAL + (random_rand() % RANDOM_INTERVAL);
    etimer_reset_with_new_interval(&timer, next_interval);
  }

  PROCESS_END();
}
