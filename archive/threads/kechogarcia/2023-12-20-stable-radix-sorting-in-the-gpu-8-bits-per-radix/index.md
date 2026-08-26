---
title: "Stable radix sorting in the GPU (8 bits per radix)."
type: archive
source: twitter
source_url: "https://x.com/kechogarcia/status/1737288025107816560"
author: "Kecho"
handle: kechogarcia
post_id: "1737288025107816560"
date: 2023-12-20
archived: 2026-08-26
draft: false
tags:
  - archive
  - twitter
  - kechogarcia
description: "Stable radix sorting in the GPU (8 bits per radix)."
in_reply_to: ""
---

## Source

- URL: https://x.com/kechogarcia/status/1737288025107816560
- Author: Kecho (@kechogarcia)
- Posted: 2023-12-20 01:45:17

## Thread

**1/** **@kechogarcia** ^1737288025107816560

Stable radix sorting in the GPU (8 bits per radix). Not many accessible resources to do it stable. Here it goes:

    1. Count & Scatter
    2. Prefix batch table
    3. Global Prefix
    4. Scatter Output
    5. Repeat 1-4 for each radix.

(Details & code in thread)

**2/** **@kechogarcia** ^1737288026416398688

Step1 (Count & Scatter).
Split input in batches. Have a thread group in your compute shader tackle a set of batches:

for (uint i = groupThreadID ; i < totalInBatch; i+= GROUPSIZE)
{
          //do some work
}

![](https://pbs.twimg.com/media/GBwMbVqWAAAL2-l?format=png&name=orig)

**3/** **@kechogarcia** ^1737288028081598820

The work in this kernel involves filling a "local offset buffer" (LOB) (source of stability) and a "radix count batch table" ) RBT 

RBT is a 256 table of dwords (histogram for each batch) and the LOB has 1 entry for each input entry.

**4/** **@kechogarcia** ^1737288029423747502

The LOB's goal is to have the local offset for each element with respect to its radix.
i.e. a list that has [0, 1, 3, 1, 3, 4] will have a lob of [0,0,0,1,1,0]. The 1's are there because these are the stable offsets for repeated radixes.

**5/** **@kechogarcia** ^1737288030744920498

To compute the LOB, we first have a Local Thread Bit Cache (LTBC) in LDS. This LTBC is 256 elements (1 for each radix) and gets initialized to 0 on each iteration of the loop.
Each LTBC will have 1 bit for each thread in the group. So if a group has 64 threads, its 2 dwords.

**6/** **@kechogarcia** ^1737288032149967144

On each iteration of the loop, we will InterlockOr the bit of the corresponding thread for the corresponding entry. We sync groups, then do a prefix popcnt (countbits in hlsl) to count the number of previous elements seen for that particular radix, at that iteration.

**7/** **@kechogarcia** ^1737288033651642415

g_threadBit to 0
InterlockOr(g_threadBit[radix], 1 << groupThreadID); 
Sync();
g_lobOutput[i] = g_lobOffset[radix] + countbits(g_threadBit[radix] - 1);
g_lobOffset[radix] += countbits(g_localRadix[radix]);

**8/** **@kechogarcia** ^1737288035111260177

Step 2 (Prefix batch table) 
We do a Hillis Steele Scan on the RBT of step 1, and spit out a prefix batch table (PBT) and a Global Radix count (GRC)

![](https://pbs.twimg.com/media/GBwUua9WcAA7pyp?format=jpg&name=orig)

**9/** **@kechogarcia** ^1737288036700787084

Step 3 global prefix table (GPT), this holds the global offset of each radix. Again a hillis steele scan.

![](https://pbs.twimg.com/media/GBwVSwTXUAAqqEl?format=png&name=orig)

**10/** **@kechogarcia** ^1737288038307213755

Step 4: Scatter ouput.

outputIndex = 
      GPT[radix] + 
      PBT[radix*batchCount + batchIndex] +
      LOB[inputIndex];

g_output[outputIndex] = g_input[iputIndex]

**11/** **@kechogarcia** ^1737288039603269648

Go to the next radix, use the output as the new input and repeat steps 1 through 4.

Code can be found here: 
https://github.com/kecho/gpu_algorithms/blob/main/gpu_algorithms/gpu/radix_sort.hlsl

Kernel scheduling in coalpy:
https://github.com/kecho/gpu_algorithms/blob/main/gpu_algorithms/gpu/radix_sort.py

Perf numbers for 20 million items on a RTX 2070 Super

![](https://pbs.twimg.com/media/GBwWOXJXAAESwoQ?format=png&name=orig)

Branches: [[archive/threads/kechogarcia/2023-12-20-stable-radix-sorting-in-the-gpu-8-bits-per-radix/2023-12-20-SebAaltonen-i-like-the-single-pass-per-pass-approach-but]], [[archive/threads/kechogarcia/2023-12-20-stable-radix-sorting-in-the-gpu-8-bits-per-radix/2023-12-20-aras_p-noice-any-ideas-how-it-compares-to-say-amd]]
