# NLS-NetOS v0.1.2

NLS-NetOS is a router operating-system project with platform discovery, CPU/memory management, routing and forwarding components, cryptography, Router-CA, IPsec, TLS, databases, packaging, and tests.

## Router Status CLI Tutorial

NLS-NetOS provides a status interface for inspecting the router platform from the terminal. The commands are designed to make it easy for an operator or developer to understand the current state of the Linux host underneath NLS-NetOS.

### Requirements

The status implementation reads Linux `/proc` and `/sys` interfaces. Use a Linux system for the complete hardware view.

From a source checkout, run the CLI with:

```bash
PYTHONPATH=src python3 -m router_os.cli status
```

The installed `nls` command is intended to provide the shorter form:

```bash
nls status
```

> **Note:** If `nls` is not yet installed into your shell's `PATH`, use the `PYTHONPATH=src python3 -m router_os.cli ...` form while developing from the repository.

---

## 1. `nls status`

Shows the complete high-level router/platform status.

```bash
nls status
```

It combines the major views:

```text
Platform
Hardware
CPU
Memory
PCI
Drivers
Interfaces
```

Typical information includes:

- operating system
- Linux kernel
- CPU architecture
- hostname
- logical CPU count
- CPU utilization
- network interface count
- PCI device count
- NUMA nodes
- memory totals and available memory
- hugepage count
- network interface state and MTU

Use this command first when you want a quick overview.

---

## 2. `nls status platform`

Displays platform identification information.

```bash
nls status platform
```

Example:

```text
NLS-NetOS Platform
------------------
OS              : Linux
Kernel          : 6.x.x
Architecture    : x86_64
Hostname        : router-01
```

### What it tells you

This answers:

> "What Linux platform is NLS-NetOS currently running on?"

It is useful when diagnosing differences between router hardware, virtual machines, development systems, and production systems.

---

## 3. `nls status hardware`

Displays a high-level hardware inventory.

```bash
nls status hardware
```

The status view reports information such as:

```text
Interfaces      : 6
PCI devices     : 8
NUMA nodes      : 1
```

### What it tells you

This is the quickest hardware sanity check. If a NIC or PCI device expected by the router is missing, this command helps identify the problem before debugging the routing or forwarding planes.

The platform layer obtains the underlying information from Linux rather than pretending that hardware exists.

---

## 4. `nls status cpu`

Displays CPU information relevant to the router.

```bash
nls status cpu
```

Typical output contains:

```text
CPU
---
Logical CPUs    : 8
Current usage   : 24.5%
NUMA nodes      : 1
```

### Why CPU status matters

Packet processing, forwarding, routing protocols, cryptographic operations, and management workloads all consume CPU resources.

The CPU status command gives the operator a fast view of whether the platform has the CPU resources expected by NLS-NetOS.

### Private CPU / CPU guard

NLS-NetOS also contains a CPU-guard subsystem for the requested private-CPU policy.

For an odd logical CPU count of at least three, the last logical CPU is reserved from the NLS routing/packet-worker affinity set:

```text
5 CPUs

CPU 0  ROUTING
CPU 1  ROUTING
CPU 2  ROUTING
CPU 3  ROUTING
CPU 4  NULL / RESERVED
```

For seven CPUs:

```text
CPU 0  ROUTING
CPU 1  ROUTING
CPU 2  ROUTING
CPU 3  ROUTING
CPU 4  ROUTING
CPU 5  ROUTING
CPU 6  NULL / RESERVED
```

The reserved CPU is **not physically disabled**. Linux can still use it for kernel work or unrelated processes. The CPU guard keeps it out of the NLS routing/packet-worker affinity mask.

The CPU guard also monitors utilization. At or above 90% it produces a warning; at 100% it produces a critical alert. The structured alert identifies LAN, WAN, and Router-CA as the intended consumers.

This design keeps the CPU policy isolated from the existing routing and forwarding directories.

---

## 5. `nls status memory`

Displays memory information.

```bash
nls status memory
```

Example:

```text
Memory
------
Total           : 31.2 GiB
Available       : 23.7 GiB
Hugepages       : 1024
```

### What it tells you

Memory is important for:

- routing tables
- LSDBs
- neighbor state
- packet buffers
- forwarding structures
- cryptographic operations
- connection/session state
- hugepage-backed packet processing

The command currently reports Linux memory information and hugepage information exposed through `/proc` and `/sys`.

---

## 6. `nls status pci`

Lists PCI devices discovered through Linux.

```bash
nls status pci
```

Example:

```text
PCI
---
Devices         : 4
  0000:01:00.0
  0000:01:00.1
  0000:02:00.0
  0000:03:00.0
```

### Why PCI status matters

Router hardware frequently exposes network adapters, storage controllers, accelerators, and other devices through PCI/PCIe.

If a physical NIC is expected but its PCI device is absent, the problem may be below the routing stack: hardware, firmware, PCI enumeration, BIOS/UEFI, or the Linux kernel.

This command is therefore useful during hardware bring-up.

---

## 7. `nls status drivers`

Displays the platform's driver layer status.

```bash
nls status drivers
```

The current status view identifies the major driver categories:

```text
Drivers
-------
Ethernet        : kernel/sysfs
NIC             : kernel/sysfs
Storage         : kernel/sysfs
Platform        : kernel/sysfs
```

### Important distinction

This command is a **platform status view**, not a replacement for Linux's complete driver inventory.

The NLS platform layer uses Linux kernel facilities and sysfs to discover hardware. Actual production NIC/Ethernet driver functionality remains provided by the appropriate Linux/vendor driver stack unless a dedicated NLS hardware driver is implemented for a device.

---

## 8. `nls status interfaces`

Lists network interfaces and their current basic state.

```bash
nls status interfaces
```

Example:

```text
Interfaces
----------
eth0            state=up         mtu=1500
eth1            state=down       mtu=1500
lo              state=unknown    mtu=65536
```

### What it tells you

For each interface, the status view reports:

- interface name
- operational state
- MTU

This is useful before investigating routing protocols or packet forwarding. If the required interface is missing or down, higher-level network functions may not be able to operate correctly.

---

# Recommended troubleshooting workflow

When an NLS router is not behaving as expected, start broad and then narrow the investigation:

```bash
nls status
```

Then inspect the relevant layer:

```bash
nls status platform
nls status hardware
nls status cpu
nls status memory
nls status pci
nls status drivers
nls status interfaces
```

A practical sequence is:

```text
                 nls status
                     │
                     ▼
              Platform healthy?
                     │
          ┌──────────┴──────────┐
          │                     │
         YES                    NO
          │                     │
          ▼                     ▼
       Hardware             platform
          │                investigation
          ▼
        PCI/NIC
          │
          ▼
     Interfaces UP?
          │
          ▼
       CPU/Memory
          │
          ▼
   Routing / Forwarding
```

## Quick reference

| Command | Purpose |
|---|---|
| `nls status` | Complete router/platform overview |
| `nls status platform` | OS, kernel, architecture and hostname |
| `nls status hardware` | Hardware inventory summary |
| `nls status cpu` | CPU count, utilization and NUMA information |
| `nls status memory` | RAM and hugepage information |
| `nls status pci` | PCI/PCIe device inventory |
| `nls status drivers` | Platform driver categories |
| `nls status interfaces` | Network interface state and MTU |

## Developer form

When running directly from a source checkout, the equivalent commands are:

```bash
PYTHONPATH=src python3 -m router_os.cli status
PYTHONPATH=src python3 -m router_os.cli status platform
PYTHONPATH=src python3 -m router_os.cli status hardware
PYTHONPATH=src python3 -m router_os.cli status cpu
PYTHONPATH=src python3 -m router_os.cli status memory
PYTHONPATH=src python3 -m router_os.cli status pci
PYTHONPATH=src python3 -m router_os.cli status drivers
PYTHONPATH=src python3 -m router_os.cli status interfaces
```

These commands provide the operator-facing foundation for future NLS-NetOS health, diagnostics, and monitoring features.
