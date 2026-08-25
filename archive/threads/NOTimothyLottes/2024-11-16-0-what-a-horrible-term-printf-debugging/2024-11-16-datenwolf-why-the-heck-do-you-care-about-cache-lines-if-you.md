---
title: "@NOTimothyLottes Why the heck do you care about cache lines, if you write to a mmaped file? Of course there's overhead: TLBs aren't free."
type: archive
source: twitter
source_url: "https://x.com/datenwolf/status/1857820149039947846"
author: "datenwolf – here to witness Τwitter's death"
handle: datenwolf
post_id: "1857820149039947846"
date: 2024-11-16
archived: 2026-08-25
draft: false
tags:
  - archive
  - twitter
  - NOTimothyLottes
description: "@NOTimothyLottes Why the heck do you care about cache lines, if you write to a mmaped file? Of course there's overhead: TLBs aren't free."
in_reply_to: ""
parent_post_id: "1857805438151983120"
---

## Source

- URL: https://x.com/datenwolf/status/1857820149039947846
- Author: datenwolf – here to witness Τwitter's death (@datenwolf)
- Posted: 2024-11-16 16:16:54

## Branch

**1/** @datenwolf

@NOTimothyLottes Why the heck do you care about cache lines, if you write to a mmaped file? Of course there's overhead: TLBs aren't free. And TLBs matter… at lot in fact. When you map the file, initially the kernel marks some address space, but doesn't populate it with pages. 1/

**2/** @datenwolf

@NOTimothyLottes On the first write to a non-faulted page, the kernel has to find a free page in memory, associate it in the page table, all the while keeping an eye on all threads process, since changes to a process virtual address space must appear atomic. 2/

**3/** @datenwolf

@NOTimothyLottes Memory maps aren't free. Simple writes to a file will easily outperform and cause less overhead, than naively implemented mmaped I/O. 3/

**4/** @NOTimothyLottes

@datenwolf BTW, I pre-fault my mapped files. Just like I pre-fault the binary and data segments too. But sure the pre-fault could go stale. And yes TLBs are a system perf issue, but atlas you need admin priv on Windows to play 2 MiB pages for data, so it's off the table

**5/** @NOTimothyLottes

@datenwolf Why cacheline aligned and sized on the CPU? In theory store the entire line in a short enough timeframe and your Read-Modify-Write becomes just a Write! CPU doesn't have byte-write-mask (I think). If SW+HW is good. And threads keeping to isolated lines means no false sharing. Etc

**6/** @datenwolf

@NOTimothyLottes (That cacheline remark was meant rhetorically; between cache misses and page faults, a page fault will largely overshadow a cache miss in performance overhead.
But yes, if you prefault, then that problem is mitigated.)

**7/** @NOTimothyLottes

@datenwolf 'Smart' people keep trying to impose (aka force) their will on others through poor system APIs, like not being able to pre-pin pages. Good look buddy, I'll just run a background task that continuously touch walks the pages I want pinned anyway.

## Related

- Spine: [[archive/threads/NOTimothyLottes/2024-11-16-0-what-a-horrible-term-printf-debugging]]
