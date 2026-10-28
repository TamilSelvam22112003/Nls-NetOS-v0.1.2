/*
 * NLS-NetOS native DPDK packet engine.
 *
 * This is a real DPDK RX/TX datapath. Intel register programming is performed
 * by the selected DPDK Intel PMD (ice/i40e/ixgbe/igc/etc.); this application
 * deliberately does not touch vendor MMIO registers directly.
 *
 * Build on Ubuntu with a DPDK development package/toolchain. Example:
 *   cc $(pkg-config --cflags libdpdk) -O3 -march=native -Wall -Wextra \
 *      -o nls-dpdk-forwarder dpdk_forwarder.c $(pkg-config --libs libdpdk)
 *
 * Run only after deployment tooling has assigned the target NICs to an
 * appropriate DPDK/VFIO-compatible driver:
 *   sudo ./nls-dpdk-forwarder -l 1-2 -a 0000:03:00.0 -a 0000:03:00.1
 */

#include <errno.h>
#include <getopt.h>
#include <inttypes.h>
#include <signal.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

#include <rte_eal.h>
#include <rte_ethdev.h>
#include <rte_mbuf.h>
#include <rte_mempool.h>
#include <rte_lcore.h>

#define RX_DESC 1024U
#define TX_DESC 1024U
#define NUM_MBUFS 8192U
#define MBUF_CACHE 256U
#define BURST 32U
#define SOCKET_ANY SOCKET_ID_ANY

static volatile sig_atomic_t force_quit;

static void signal_handler(int signum) {
    if (signum == SIGINT || signum == SIGTERM)
        force_quit = 1;
}

static void usage(const char *prog) {
    fprintf(stderr,
        "Usage: %s [DPDK EAL args]\n"
        "       %s -l <cores> -a <pci0> -a <pci1>\n"
        "The first two probed DPDK ports are used as a bidirectional L2 forwarder.\n",
        prog, prog);
}

static int port_init(uint16_t port, struct rte_mempool *pool) {
    struct rte_eth_conf conf = {0};
    struct rte_eth_dev_info info;
    struct rte_eth_txconf txconf;
    struct rte_eth_rxconf rxconf;
    int rc;

    rte_eth_dev_info_get(port, &info);
    conf.rxmode.mq_mode = RTE_ETH_MQ_RX_NONE;
    conf.txmode.mq_mode = RTE_ETH_MQ_TX_NONE;

    rc = rte_eth_dev_configure(port, 1, 1, &conf);
    if (rc < 0)
        return rc;

    rxconf = info.default_rxconf;
    txconf = info.default_txconf;

    rc = rte_eth_rx_queue_setup(port, 0, RX_DESC,
                                rte_eth_dev_socket_id(port), &rxconf, pool);
    if (rc < 0)
        return rc;

    rc = rte_eth_tx_queue_setup(port, 0, TX_DESC,
                                rte_eth_dev_socket_id(port), &txconf);
    if (rc < 0)
        return rc;

    rc = rte_eth_dev_start(port);
    if (rc < 0)
        return rc;

    rte_eth_promiscuous_enable(port);
    return 0;
}

static void forward_loop(uint16_t port_a, uint16_t port_b) {
    struct rte_mbuf *bufs[BURST];
    uint16_t from[2] = {port_a, port_b};
    uint16_t to[2] = {port_b, port_a};

    while (!force_quit) {
        for (unsigned direction = 0; direction < 2; ++direction) {
            uint16_t n = rte_eth_rx_burst(from[direction], 0, bufs, BURST);
            if (n == 0)
                continue;

            uint16_t sent = rte_eth_tx_burst(to[direction], 0, bufs, n);
            for (uint16_t i = sent; i < n; ++i)
                rte_pktmbuf_free(bufs[i]);
        }
    }
}

int main(int argc, char **argv) {
    int eal_argc;
    uint16_t nb_ports;
    uint16_t port_a, port_b;
    unsigned lcore;
    struct rte_mempool *pool;
    char pool_name[64];

    signal(SIGINT, signal_handler);
    signal(SIGTERM, signal_handler);

    eal_argc = rte_eal_init(argc, argv);
    if (eal_argc < 0) {
        rte_exit(EXIT_FAILURE, "DPDK EAL initialization failed\n");
    }

    (void)optind;
    nb_ports = rte_eth_dev_count_avail();
    if (nb_ports < 2) {
        usage(argv[0]);
        rte_exit(EXIT_FAILURE, "At least two DPDK ports are required, found %u\n", nb_ports);
    }

    port_a = 0;
    port_b = 1;

    snprintf(pool_name, sizeof(pool_name), "nls_mbuf_%u", (unsigned)getpid());
    pool = rte_pktmbuf_pool_create(pool_name, NUM_MBUFS, MBUF_CACHE,
                                   0, RTE_MBUF_DEFAULT_BUF_SIZE, SOCKET_ANY);
    if (pool == NULL)
        rte_exit(EXIT_FAILURE, "mbuf pool creation failed: %s\n", rte_strerror(rte_errno));

    if (port_init(port_a, pool) < 0 || port_init(port_b, pool) < 0)
        rte_exit(EXIT_FAILURE, "DPDK port initialization failed\n");

    lcore = rte_get_next_lcore(rte_lcore_id(), 1, 0);
    if (lcore == RTE_MAX_LCORE)
        lcore = rte_lcore_id();

    printf("NLS-NetOS DPDK forwarder running: ports %u <-> %u on lcore %u\n",
           port_a, port_b, lcore);

    forward_loop(port_a, port_b);

    rte_eth_dev_stop(port_a);
    rte_eth_dev_stop(port_b);
    rte_eth_dev_close(port_a);
    rte_eth_dev_close(port_b);
    rte_mempool_free(pool);
    rte_eal_cleanup();
    return 0;
}
