---
title: "sendmmsg/recvmmsg can only work with 1024 packets at a time unfortunately."
type: archive
source: twitter
source_url: "https://x.com/AgileJebrim/status/2070338320765165758"
author: "Jebrim"
handle: AgileJebrim
post_id: "2070338320765165758"
date: 2026-06-26
archived: 2026-08-23
draft: true
tags:
  - archive
  - twitter
  - NOTimothyLottes
description: "sendmmsg/recvmmsg can only work with 1024 packets at a time unfortunately."
in_reply_to: ""
parent_post_id: "2070337342854832468"
---

## Source

- URL: https://x.com/AgileJebrim/status/2070338320765165758
- Author: Jebrim (@AgileJebrim)
- Posted: 2026-06-26 02:48:15

## Branch

**1/**

sendmmsg/recvmmsg can only work with 1024 packets at a time unfortunately. You’ve gotta loop them. While they’re surprisingly fairly deterministic in execution times, their throughput isn’t the best. The Linux kernel takes far longer to process sending the packets out than my own code does to process the sim and build the packets in the first place lol.

**2/**

@AgileJebrim Yes 1024 max, so best case 1/1024 the syscall count (well factored). As for overhead, for a co-located server you could always hijack the network card driver and just move your server into it and run kernel side if you really wanted to.

**3/**

@NOTimothyLottes If you want to be locked in to a particular NIC yeah.

**4/**

@AgileJebrim @NOTimothyLottes You can use eBPF as a poor man's kernel bypass.

**5/**

@aepau2 @AgileJebrim Not that any of my source would pass their nanny tester. When I was younger and running my own business, I used to host my business website off of a really old laptop running an in-kernel web server that I wrote. It wasn’t that hard to do long ago.

**6/**

@NOTimothyLottes @aepau2 eBPF doesn’t support SIMD lol

## Related

- Spine: [[archive/threads/NOTimothyLottes/2026-06-26-quick-summary-of-why-not-pselect-ppoll-epoll]]
