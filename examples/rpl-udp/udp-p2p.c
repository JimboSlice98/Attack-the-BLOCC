#include "contiki.h"
#include "net/routing/routing.h"
#include "random.h"
#include "net/netstack.h"
#include "net/ipv6/simple-udp.h"
#include "net/ipv6/uiplib.h"
#include "net/ipv6/uip-ds6.h"
#include <stdint.h>
#include <inttypes.h>
#include <string.h>
#include "msg-cache.h"

#include "sys/log.h"
#define LOG_MODULE "App"
#define LOG_LEVEL LOG_LEVEL_INFO

#define UDP_PORT 8765
#define SEND_INTERVAL (10 * CLOCK_SECOND)

static struct simple_udp_connection udp_conn;
static uint32_t rx_count = 0;
static uint32_t tx_count = 0;
static uint32_t missed_tx_count = 0;

/*---------------------------------------------------------------------------*/
PROCESS(udp_p2p_process, "UDP P2P");
AUTOSTART_PROCESSES(&udp_p2p_process);
/*---------------------------------------------------------------------------*/
void
format_data(char *buffer, size_t buffer_size, uint32_t message_num,
            const uip_ipaddr_t *origin_addr)
{
  char addr_str[UIPLIB_IPV6_MAX_STR_LEN];
  uiplib_ipaddr_snprint(addr_str, sizeof(addr_str), origin_addr);
  snprintf(buffer, buffer_size, "%u|%s", message_num, addr_str);
}
/*---------------------------------------------------------------------------*/
int
parse_data(const char *data_str, uint32_t *message_num,
           uip_ipaddr_t *origin_addr)
{
  char addr_str[UIPLIB_IPV6_MAX_STR_LEN];
  int num_parsed = sscanf(data_str, "%u|%s", message_num, addr_str);
  if (num_parsed == 2) {
    return uiplib_ipaddrconv(addr_str, origin_addr);
  }
  return 0;
}
/*---------------------------------------------------------------------------*/
static void
udp_rx_callback(struct simple_udp_connection *c,
                const uip_ipaddr_t *sender_addr,
                uint16_t sender_port,
                const uip_ipaddr_t *receiver_addr,
                uint16_t receiver_port,
                const uint8_t *data,
                uint16_t datalen)
{
  uint32_t message_num;
  uip_ipaddr_t origin_addr;

  if (parse_data((const char *)data, &message_num, &origin_addr)) {
    LOG_INFO("Rx: '%.*s'\n", datalen, (char *) data);
    LOG_INFO("From:  ");
    LOG_INFO_6ADDR(sender_addr);
    LOG_INFO_("\n");

    if (is_duplicate(data, datalen)) {
      LOG_INFO("Duplicate message received, ignoring.\n");
      return;
    }

    add_to_cache(data, datalen);
    rx_count++;

    // Repeat the received message to the whole network
    LOG_INFO("Tx: flood '%.*s'\n", datalen, (char *)data);
    uip_ipaddr_t dest_ipaddr;
    uip_create_linklocal_allnodes_mcast(&dest_ipaddr);
    simple_udp_sendto(&udp_conn, data, datalen, &dest_ipaddr);
  } else {
    LOG_INFO("Rx: failed to parse data\n");
  }
}
/*---------------------------------------------------------------------------*/
PROCESS_THREAD(udp_p2p_process, ev, data)
{
  static struct etimer periodic_timer;
  static char str[MAX_MSG_LEN];
  uip_ipaddr_t dest_ipaddr;
  uip_ipaddr_t *local_ipaddr;

  PROCESS_BEGIN();

  /* Initialize UDP connection */
  simple_udp_register(&udp_conn, UDP_PORT, NULL, UDP_PORT, udp_rx_callback);

  /* Initialize message cache */
  message_cache_init();

  /* Add an initial delay to allow the network to form */
  etimer_set(&periodic_timer, CLOCK_SECOND * 30);
  PROCESS_WAIT_EVENT_UNTIL(etimer_expired(&periodic_timer));

  etimer_set(&periodic_timer, random_rand() % SEND_INTERVAL);
  while(1) {
    PROCESS_WAIT_EVENT_UNTIL(etimer_expired(&periodic_timer));

    /* Create a broadcast address */
    uip_create_linklocal_allnodes_mcast(&dest_ipaddr);

    /* Retrieve the link-local IP address */
    local_ipaddr = &uip_ds6_get_link_local(ADDR_PREFERRED)->ipaddr;

    if(local_ipaddr != NULL) {
      /* Print statistics every 10th TX */
      if(tx_count % 10 == 0) {
        LOG_INFO("Tx/Rx/MissedTx: %" PRIu32 "/%" PRIu32 "/%" PRIu32 "\n",
                 tx_count, rx_count, missed_tx_count);
      }

      /* Send to all nodes */
      LOG_INFO("Sending request %"PRIu32" to ", tx_count);
      LOG_INFO_6ADDR(&dest_ipaddr);
      LOG_INFO_("\n");
      format_data(str, sizeof(str), tx_count, local_ipaddr);
      simple_udp_sendto(&udp_conn, str, strlen(str), &dest_ipaddr);
      add_to_cache((const uint8_t *)str, strlen(str));
      tx_count++;
    } else {
      LOG_INFO("No link-local IP address available\n");
      missed_tx_count++;
    }

    /* Add some jitter */
    etimer_set(&periodic_timer, SEND_INTERVAL
      - CLOCK_SECOND + (random_rand() % (2 * CLOCK_SECOND)));
  }

  PROCESS_END();
}
/*---------------------------------------------------------------------------*/
