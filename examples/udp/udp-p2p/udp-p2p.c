#include "contiki.h"
#include "random.h"
#include "net/netstack.h"
#include "net/ipv6/simple-udp.h"
#include "net/ipv6/uiplib.h"
#include "net/ipv6/uip-ds6.h"
#include "net/packetbuf.h"
#include "sys/log.h"
#include "sys/rtimer.h"
#include "sys/node-id.h"
#include "dev/serial-line.h"
#include "msg-cache.h"
#include "msg-store.h"

#define LOG_MODULE "Node"
#define LOG_LEVEL LOG_LEVEL_INFO

#define UDP_PORT 8765
#define SEND_INTERVAL (60 * CLOCK_SECOND)

static struct simple_udp_connection udp_conn;
static uint32_t tx_count = 0;

/*---------------------------------------------------------------------------*/
PROCESS(udp_p2p_process, "UDP P2P");
AUTOSTART_PROCESSES(&udp_p2p_process);
/*---------------------------------------------------------------------------*/
int
parse_msg(const char *data_str, uint32_t *message_num,
           uint16_t *origin_node, uint16_t *attest_node)
{
  int num_parsed = sscanf(data_str, "%u|%hu|%hu", message_num, origin_node, attest_node);
  return (num_parsed == 3);
}
/*---------------------------------------------------------------------------*/
static void
udp_rx_callback(struct simple_udp_connection *c, const uip_ipaddr_t *sender_addr,
                uint16_t sender_port, const uip_ipaddr_t *receiver_addr,
                uint16_t receiver_port, const uint8_t *data, uint16_t datalen)
{
  uint32_t message_num;
  uint16_t origin_node;
  uint16_t attest_node;

  uip_ipaddr_t dest_ipaddr;
  uip_create_linklocal_allnodes_mcast(&dest_ipaddr);

  if (parse_msg((const char *)data, &message_num, &origin_node, &attest_node)) {
    LOG_INFO("Rx: '%.*s' from node: '%u'\n",
             datalen, (char *)data, (uint16_t)sender_addr->u8[15]);

    if (is_duplicate(data, datalen)) {
      return;
    } else add_to_cache(data, datalen);

    // Handle incoming attestations
    if (attest_node != 0 && origin_node != node_id) {
      LOG_INFO("Bx: '%.*s'\n", datalen, (char *)data);
      simple_udp_sendto(&udp_conn, data, datalen, &dest_ipaddr);
      return;
    } else if (attest_node != 0) {
      add_attestation(find_message(message_num), attest_node);
      return;
    }

    // Handle incoming messages
    LOG_INFO("Bx: '%.*s'\n", datalen, (char *)data);
    simple_udp_sendto(&udp_conn, data, datalen, &dest_ipaddr);

    // Create new attestation
    static char str[MAX_MSG_LEN];
    snprintf(str, sizeof(str), "%u|%hu|%hu", message_num,
             origin_node, node_id);
    LOG_INFO("Ax: '%.*s'\n", (int)strlen(str), str);
    simple_udp_sendto(&udp_conn, str, strlen(str), &dest_ipaddr);
    add_to_cache((const uint8_t *)str, strlen(str));

  } else {
    // LOG_INFO("Rx: failed to parse data\n");
  }
}
/*---------------------------------------------------------------------------*/
PROCESS_THREAD(udp_p2p_process, ev, data) {
  static struct etimer periodic_timer;
  static char str[MAX_MSG_LEN];
  uip_ipaddr_t dest_ipaddr;

  PROCESS_BEGIN();

  // Initialize UDP connection and wait 10s
  simple_udp_register(&udp_conn, UDP_PORT, NULL, UDP_PORT, udp_rx_callback);
  etimer_set(&periodic_timer, CLOCK_SECOND * (10 + node_id));
  PROCESS_WAIT_EVENT_UNTIL(etimer_expired(&periodic_timer));

  // Initialize serial line
  serial_line_init();

  // Set timer to correct message interval
  etimer_set(&periodic_timer, SEND_INTERVAL);
  while (1) {
    PROCESS_WAIT_EVENT();

    if (ev == PROCESS_EVENT_TIMER && etimer_expired(&periodic_timer)) {
      // Format and broadcast new message to network
      uip_create_linklocal_allnodes_mcast(&dest_ipaddr);
      snprintf(str, sizeof(str), "%u|%hu|%hu", tx_count, node_id, 0);
      LOG_INFO("Tx: '%.*s'\n", (int)strlen(str), str);
      
      simple_udp_sendto(&udp_conn, str, strlen(str), &dest_ipaddr);
      add_to_cache((const uint8_t *)str, strlen(str));
      add_message(tx_count);
      tx_count++;

      etimer_set(&periodic_timer, SEND_INTERVAL);
    } else if (ev == serial_line_event_message) {
      char *received_cmd = (char *)data;
      if (strcmp(received_cmd, "print_cache") == 0) {
        print_cache();
      }
      else if (strcmp(received_cmd, "print_store") == 0) {
        print_msg_store();
      }
    }
  }

  PROCESS_END();
}
/*---------------------------------------------------------------------------*/
