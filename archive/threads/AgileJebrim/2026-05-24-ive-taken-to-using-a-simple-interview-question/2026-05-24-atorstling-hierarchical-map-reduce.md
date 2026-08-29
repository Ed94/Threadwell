---
title: "@AgileJebrim Hierarchical map reduce?"
type: archive
source: twitter
source_url: "https://x.com/atorstling/status/2058449690572501039"
author: "Alexander Torstling"
handle: atorstling
post_id: "2058449690572501039"
date: 2026-05-24
archived: 2026-08-29
draft: false
tags:
  - archive
  - twitter
  - AgileJebrim
description: "@AgileJebrim Hierarchical map reduce?"
in_reply_to: ""
parent_post_id: "2058420153348391346"
---

## Source

- URL: https://x.com/atorstling/status/2058449690572501039
- Author: Alexander Torstling (@atorstling)
- Posted: 2026-05-24 07:27:05

## Branch

**1/** **@atorstling** ^2058449690572501039

**@AgileJebrim**

Hierarchical map reduce?

**2/** **@AgileJebrim** ^2058531652595253265

**@atorstling**

Okay. Now explain how that works.

**3/** **@atorstling** ^2058614306871067052

**@AgileJebrim**

Use shared memory for in-batch coordination, and global memory for intra-batch coordination. Each batch takes a set of numbers and produce a sum. Next round of batches operates on the output of the previous round. If fancy, you could encode the problem in kernels/registers.

**4/** **@atorstling** ^2058614911580701084

**@AgileJebrim**

Since you can use output of batches from different rounds as input, you can keep the pipeline full by starting new rounds eagerly

**5/** **@AgileJebrim** ^2058616473262641450

**@atorstling**

I’m not really satisfied with this answer.

**6/** **@atorstling** ^2058638219365818830

**@AgileJebrim**

You don't need to be, all good :)

## Related

- Spine: [[archive/threads/AgileJebrim/2026-05-24-ive-taken-to-using-a-simple-interview-question]]
