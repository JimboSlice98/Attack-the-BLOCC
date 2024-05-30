#include "contiki.h"
#include "random.h"
#include "net/netstack.h"
#include "net/ipv6/simple-udp.h"
#include "net/ipv6/uiplib.h"
#include "net/ipv6/uip-ds6.h"
#include "net/packetbuf.h"
#include "sys/log.h"
#include "sys/rtimer.h"
#include "msg-cache.h"

#define LOG_MODULE "Node"
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
void format_data(char *buffer, size_t buffer_size, uint32_t message_num, const uip_ipaddr_t *origin_addr) {
  char addr_str[UIPLIB_IPV6_MAX_STR_LEN];
  uiplib_ipaddr_snprint(addr_str, sizeof(addr_str), origin_addr);
  snprintf(buffer, buffer_size, "%u|%s", message_num, addr_str);
}

/*---------------------------------------------------------------------------*/
int parse_data(const char *data_str, uint32_t *message_num, uip_ipaddr_t *origin_addr) {
  char addr_str[UIPLIB_IPV6_MAX_STR_LEN];
  int num_parsed = sscanf(data_str, "%u|%s", message_num, addr_str);
  if (num_parsed == 2) {
    return uiplib_ipaddrconv(addr_str, origin_addr);
  }
  return 0;
}

/*---------------------------------------------------------------------------*/
static void udp_rx_callback(struct simple_udp_connection *c, const uip_ipaddr_t *sender_addr,
                            uint16_t sender_port, const uip_ipaddr_t *receiver_addr,
                            uint16_t receiver_port, const uint8_t *data, uint16_t datalen) {
  uint32_t message_num;
  uip_ipaddr_t origin_addr;

  int16_t rssi = (int16_t)packetbuf_attr(PACKETBUF_ATTR_RSSI);
  uint8_t lqi = packetbuf_attr(PACKETBUF_ATTR_LINK_QUALITY);
  radio_value_t channel;

  if (parse_data((const char *)data, &message_num, &origin_addr)) {
    LOG_INFO("Rx: '%.*s'\n", datalen, (char *)data);
    LOG_INFO("From:  ");
    LOG_INFO_6ADDR(sender_addr);
    LOG_INFO_("\n");
    
    if (NETSTACK_RADIO.get_value(RADIO_PARAM_CHANNEL, &channel) == RADIO_RESULT_OK) {
      LOG_INFO("RSSI: %d, LQI: %u, CHNL: %u\n", rssi, lqi, channel);
    } else {
      LOG_INFO("Failed to get current channel\n");
    }

    if (is_duplicate(data, datalen)) {
      return;
    }

    add_to_cache(data, datalen);
    rx_count++;

    // Repeat the received message to the whole network
    LOG_INFO("Bx: '%.*s'\n", datalen, (char *)data);
    uip_ipaddr_t dest_ipaddr;
    uip_create_linklocal_allnodes_mcast(&dest_ipaddr);
    simple_udp_sendto(&udp_conn, data, datalen, &dest_ipaddr);
  } else {
    // LOG_INFO("Rx: failed to parse data\n");
  }
}

/*---------------------------------------------------------------------------*/
PROCESS_THREAD(udp_p2p_process, ev, data) {
  static struct etimer periodic_timer;
  static char str[MAX_MSG_LEN];
  uip_ipaddr_t dest_ipaddr;
  uip_ipaddr_t *local_ipaddr;

  PROCESS_BEGIN();

  // Initialize UDP connection
  simple_udp_register(&udp_conn, UDP_PORT, NULL, UDP_PORT, udp_rx_callback);

  // Initialize message cache
  message_cache_init();

  // Add an initial delay to allow the network to form
  etimer_set(&periodic_timer, CLOCK_SECOND * 10);
  PROCESS_WAIT_EVENT_UNTIL(etimer_expired(&periodic_timer));

  etimer_set(&periodic_timer, random_rand() % SEND_INTERVAL);
  while (1) {
    PROCESS_WAIT_EVENT_UNTIL(etimer_expired(&periodic_timer));

    // Log the current channel
    radio_value_t channel;
    if(NETSTACK_RADIO.get_value(RADIO_PARAM_CHANNEL, &channel) == RADIO_RESULT_OK) {
      LOG_INFO("Current channel: %u\n", channel);
    } else {
      LOG_INFO("Failed to get current channel\n");
    }

    // Get link-local ip address and multicast address
    uip_create_linklocal_allnodes_mcast(&dest_ipaddr);
    local_ipaddr = &uip_ds6_get_link_local(ADDR_PREFERRED)->ipaddr;

    if (local_ipaddr != NULL) {
      // Send to all nodes
      format_data(str, sizeof(str), tx_count, local_ipaddr);
      LOG_INFO("Tx: '%.*s'\n", (int)strlen(str), str);
      simple_udp_sendto(&udp_conn, str, strlen(str), &dest_ipaddr);
      add_to_cache((const uint8_t *)str, strlen(str));
      tx_count++;
    } else {
      LOG_INFO("No link-local IP address available\n");
      missed_tx_count++;
    }

    // Add some jitter
    etimer_set(&periodic_timer, SEND_INTERVAL - CLOCK_SECOND + (random_rand() % (2 * CLOCK_SECOND)));
  }

  PROCESS_END();
}
