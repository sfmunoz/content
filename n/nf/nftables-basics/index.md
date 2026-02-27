---
slug: nftables-basics
title: 'nftables basics'
summary: 'nftables essential information'
url: 'tips/:slug'
date: '2026-02-27T06:30:52Z'
categories: ['tips']
tags: ['nftables','firewall']
draft: false
---

## References

- https://wiki.nftables.org/wiki-nftables/index.php/Netfilter_hooks
- https://wiki.nftables.org/wiki-nftables/index.php/Configuring_chains
- https://github.com/sfmunoz/i12e/issues/223

## Type, hook and priority

Example:

```
# nft list ruleset
(...)
table inet filter {
  (...)
  chain prerouting {
    type filter hook prerouting priority filter; policy drop;
    udp dport 51823 counter packets 0 bytes 0 accept
    iifname != { "cni*", "flannel*", "lo", "veth*", "wg*" } jump port_knocking
    counter packets 8852906 bytes 2293686150 accept
  }
  (...)
}
(...)
```

Without details, just a loose reference:

- **type** (what?):
  - **filter**:
    - limits allowed/denied traffic
    - checks every packet
    - it's the "everyday" type
  - **nat**:
    - tweaks addressing
    - checks the first packet of the connection
    - sets conntrack
  - **route**: route decisions (never use it)
- **hook** (where?):
  - ingress
  - prerouting
  - forward
  - input
  - output
  - postrouting
  - egress
- **priority**: order of chain execution connected to the same hook
  - raw: -300
  - mangle: -150
  - dstnat: -100
  - filter: 0
  - security: 50
  - srcnat: 100

## Accept vs Reject/Drop

- accept
  - it's final within a chain
  - packet processing goes on in chain with same hook and higher priority number
- drop/reject:
  - it's final for the packet
  - no further processing is done
