#include "contiki.h"
#include "net/routing/routing.h"
#include "random.h"
#include "net/netstack.h"
#include "net/ipv6/uiplib.h"
#include "net/ipv6/uip-ds6.h"
#include "net/ipv6/tcp-socket.h"
#include <stdint.h>
#include <stdio.h>
#include <string.h>

#include "sys/log.h"
#define LOG_MODULE "TCP Client"
#define LOG_LEVEL LOG_LEVEL_INFO

#define SERVER_IP "aaaa::1"  // Use the IP address assigned to the TUN interface
#define SERVER_PORT 60001    // Update to match the port used by tunslip6

static struct tcp_socket socket;
static uint8_t buffer[128];
static uint8_t output_buffer[128];
static char msg[] = "Hello from Contiki-NG!";

/*---------------------------------------------------------------------------*/
PROCESS(tcp_client_process, "TCP Client Process");
AUTOSTART_PROCESSES(&tcp_client_process);
/*---------------------------------------------------------------------------*/
PROCESS_THREAD(tcp_client_process, ev, data)
{
  uip_ipaddr_t server_ipaddr;

  PROCESS_BEGIN();

  /* Initialize the TCP socket */
  LOG_INFO("Registering TCP socket\n");
  tcp_socket_register(&socket, NULL,
                      buffer, sizeof(buffer),
                      output_buffer, sizeof(output_buffer),
                      NULL, NULL);
  
  if (uiplib_ipaddrconv(SERVER_IP, &server_ipaddr) == 0) {
    LOG_ERR("Failed to parse server IP address\n");
    PROCESS_EXIT();
  }
  
  LOG_INFO("Connecting to server ");
  LOG_INFO_6ADDR(&server_ipaddr);
  LOG_INFO_("\n");
  tcp_socket_connect(&socket, &server_ipaddr, SERVER_PORT);

  /* Send a message to the server */
  LOG_INFO("Sending message: %s\n", msg);
  int sent_len = tcp_socket_send_str(&socket, msg);
  if (sent_len > 0) {
    LOG_INFO("Message sent successfully\n");
  } else {
    LOG_ERR("Failed to send message\n");
  }

  PROCESS_END();
}
/*---------------------------------------------------------------------------*/
