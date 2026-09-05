---
title: "Even on the cpu indices > pointers."
type: archive
source: twitter
source_url: "https://x.com/stainless_code/status/2095923859547463785"
author: "Yuriy Stets"
handle: stainless_code
post_id: "2095923859547463785"
date: 2026-09-04
archived: 2026-09-04
draft: false
tags:
  - archive
  - twitter
  - stainless_code
description: "Even on the cpu indices > pointers."
in_reply_to: ""
---

## Source

- URL: https://x.com/stainless_code/status/2095923859547463785
- Author: Yuriy Stets (@stainless_code)
- Posted: 2026-09-04 17:16:03

## Thread

**1/** **@stainless_code** ^2095923859547463785

Even on the cpu indices > pointers.
The pointers waste a lot of cache space to store useless bits that do not carry much of a value.

But I havent yet found a good/elegant solution of how to organize storage of multiple indices that belong to different contiguous chunks of memory.
Because if all of your indices belong to a single space, then you can carry the single base pointer around OOB, and index only off of that pointer. But If you have multiple spaces, let's say one or more index spaces per thread (e.g. per-thread arenas or something), like what would be an efficient way to represent that.
One way you can take some bits of an index to say which chunk you want to address into, but that eats into the size of indexable space and if you have a user-selectable number of threads - the number of bits reserved would be unpredictable.

**2/** **@NOTimothyLottes** ^2095927369949184094

**@stainless_code**

The right workaround is to have a way to run a process in a lower bounded address space. Hell, we have a VM tax we already pay for, so this is trivial. On Linux you can just do this and use system calls and bypass libc/etc. Only then some interfaces like Vulkan need workarounds.

**3/** **@NOTimothyLottes** ^2095928068615307653

**@stainless_code**

I personally indexify my VK dlsym() jump table down to 32-bit indexes from a fixed base, but of course some VK objects still force a little 64bit waste.
