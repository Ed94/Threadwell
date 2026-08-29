---
title: "I'm bored so I'm gonna give this question a good shot (I learned a bunch of GPU architecture stuff back in uni but I had to look a couple things up to make sure I wasn't mixing terms up)."
type: archive
source: twitter
source_url: "https://x.com/brainage19/status/2058448551290839084"
author: "thomas 🍙"
handle: brainage19
post_id: "2058448551290839084"
date: 2026-05-24
archived: 2026-08-29
draft: false
tags:
  - archive
  - twitter
  - AgileJebrim
description: "I'm bored so I'm gonna give this question a good shot (I learned a bunch of GPU architecture stuff back in uni but I had to look a couple things up to make sure I wasn't mixing terms up)."
in_reply_to: ""
parent_post_id: "2058420153348391346"
---

## Source

- URL: https://x.com/brainage19/status/2058448551290839084
- Author: thomas 🍙 (@brainage19)
- Posted: 2026-05-24 07:22:33

## Branch

**1/** **@brainage19** ^2058448551290839084

I'm bored so I'm gonna give this question a good shot (I learned a bunch of GPU architecture stuff back in uni but I had to look a couple things up to make sure I wasn't mixing terms up). I would assume the most efficient way is to mass add them in pairs across all streaming multiprocessors to halve the numbers you need to add, and keep doing that until you have 1 number left (the final result).

You take M chunks of N numbers from global memory and load then into L2 cache, L1 caches in streaming multiprocessors, shared memory, then finally into registers, instructions to add them in pairs get scheduled to run on threads via the warp scheduler, and the results get written into registers. I'm not exactly sure how the instructions get loaded into instruction cache but I imagine it would be a similar process.

Load the results from the registers all the way back up into global memory, now you have N/2 result numbers, N/2 original numbers, and the rest of the numbers. You repeat the process for the next chunk of numbers, making sure the results are read back into VRAM where the original numbers from the previous iteration start (this is to make sure after all chunks are processed, the results are contiguous in memory - working with contiguous memory is more efficient due to how memory is read/written in cache lines of several bytes at a time to minimise the cycles wasted waiting for data to be loaded into memory)

You keep repeating this process until eventually you will have processed all of the chunks and you will have half of the numbers in memory that you started with in global memory contiguously. Before repeating this process of processing M chunks of N numbers, you would have to wait until all streaming multiprocessors have finished processing all chunks of data. This probably sounds really stupid given how much other stuff I know and the level of detail that I have explained it but I'm not sure how that really works at an architecture/instruction level.

You repeat this process of processing M chunks of N numbers, repeatedly halving the numbers in VRAM until eventually you have 1 number left.

Is this the right idea? Is there a more efficient way? Have I explained all the concepts correctly?

**2/** **@AgileJebrim** ^2058532143576334428

**@brainage19**

Not really sure why you’re halving anything.

**3/** **@shrydar** ^2058583721079722406

**@AgileJebrim** **@brainage19**

please tell me you know you can’t in general just use an accumulator (or small set of accumulators) to collect a partial sum from streaming a significant subset of the data..

**4/** **@AgileJebrim** ^2058584367790788727

**@shrydar** **@brainage19**

You can use it for 99% of the time and only do the tree reduction at the very end.

**5/** **@shrydar** ^2058705598947201535

**@AgileJebrim** **@brainage19**

Even chunking into groups of 1000 you’re throwing away nine or ten bits of accuracy. Depending on the application that could be fine or it could be fatal.

**6/** **@AgileJebrim** ^2058707817314271710

**@shrydar** **@brainage19**

Why are you assuming floats?
https://x.com/agilejebrim/status/2058562643158352101?s=46&t=ZbNecpPBsBMrvteeaA6IcA

**7/** **@shrydar** ^2058709232938361308

**@AgileJebrim** **@brainage19**

I wasn’t assuming either way, but it’d be why Thomas was repeatedly halving the length of the list, so I was weirded out that you weren’t sure why he was even considering that. Clearly not needed for a 32 bit exact sum :)

**8/** **@AgileJebrim** ^2058711742843166954

**@shrydar** **@brainage19**

The only thing I can infer from him adding pairs and repeatedly halving is if he was attempting to perform a reduction every single iteration. This is needlessly expensive.  Cross-communication between lanes, warps, and SMs needs to be kept to a minimum and only occur at the end.

## Related

- Spine: [[archive/threads/AgileJebrim/2026-05-24-ive-taken-to-using-a-simple-interview-question]]
