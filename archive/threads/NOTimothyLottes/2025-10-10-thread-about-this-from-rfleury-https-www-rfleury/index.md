---
title: "Thread about this from @rfleury - https://www.rfleury.com/p/multi-core-by-default - because I used to do that too on the CPU ..."
type: archive
source: twitter
source_url: "https://x.com/NOTimothyLottes/status/1976631453749535059"
author: "NOTimothyLottes"
handle: NOTimothyLottes
post_id: "1976631453749535059"
date: 2025-10-10
archived: 2026-08-25
draft: false
tags:
  - archive
  - twitter
  - NOTimothyLottes
description: "Thread about this from @rfleury - https://www.rfleury.com/p/multi-core-by-default - because I used to do that too on the CPU ..."
in_reply_to: ""
---

## Source

- URL: https://x.com/NOTimothyLottes/status/1976631453749535059
- Author: NOTimothyLottes (@NOTimothyLottes)
- Posted: 2025-10-10 12:50:37

## Thread

**1/**

Thread about this from @rfleury - https://www.rfleury.com/p/multi-core-by-default - because I used to do that too on the CPU ...

**2/**

Same basic idea, all CPU threads ran the same program, each thread entry point gets an index of which thread they are. Same style as GPU programming but on the CPU! Also did runtime C code editing by exiting all threads and re-entering via new DLL ...

**3/**

There are some obvious problems though: CPU "random" preemptions -> if any thread grabs work through an atomic or even by just dividing up work according to thread index, if that thread gets preempted, the future sync will stall introducing bubbles ...

**4/**

Some CPU schedulers will preempt long running CPU threads at times of which one has no control. About the only way to try to improve this situation is to have a pair of threads instead of one, where they round robin execution using system context switches ...

**5/**

Meaning giving the OS places that it becomes better to context switch a thread (at the point the thread has no ownership of a work item). This of course introduces overhead and complexity and breaks the manual threadIndex approach to work carving

**6/**

Meaning patching the problem by speculative context switches doesn't guarantee the OS won't preempt during a bad time, it just decreases the probability

**7/**

There are other options though: allow work duplication, meaning make the work such that if 2 or more threads all compute the data, they get the same answer ... then if a thread gets to a dependency, it can start to finish work that gets stalled due to preemption

**8/**

This unfortunately also adds complexity and overhead, but at least one can continue to make forward progress. The RIGHT solution is pinned explicit CPU cores, an in modern times with huge thread count CPUs, there is no real excuse not to do this other than stupidity

Branches: [[archive/threads/NOTimothyLottes/2025-10-10-thread-about-this-from-rfleury-https-www-rfleury/2025-10-10-AgileJebrim-thats-what-i-do-one-pinned-thread-per-core-sched]], [[archive/threads/NOTimothyLottes/2025-10-10-thread-about-this-from-rfleury-https-www-rfleury/2025-10-11-lectem-pinning-works-well-only-if-your-program-is-the]], [[archive/threads/NOTimothyLottes/2025-10-10-thread-about-this-from-rfleury-https-www-rfleury/2025-10-11-techno_bog-do-you-have-a-source-from-which-one-could-learn]]
