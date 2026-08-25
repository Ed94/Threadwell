---
title: "When using arrays of resources/bindless, it's worth paying attention to index divergence."
type: archive
source: twitter
source_url: "https://x.com/KostasAAA/status/1781724275159728279"
author: "Kostas Anagnostou"
handle: KostasAAA
post_id: "1781724275159728279"
date: 2024-04-20
archived: 2026-08-25
draft: false
tags:
  - archive
  - twitter
  - KostasAAA
description: "When using arrays of resources/bindless, it's worth paying attention to index divergence."
in_reply_to: ""
---

## Source

- URL: https://x.com/KostasAAA/status/1781724275159728279
- Author: Kostas Anagnostou (@KostasAAA)
- Posted: 2024-04-20 16:39:04

## Thread

**1/** **@KostasAAA** ^1781724275159728279

When using arrays of resources/bindless, it's worth paying attention to index divergence. Even if using thread divergent indices, the compiler will use the index from the first active thread to access a resource, for all threads in the wave, which can cause hard to find bugs 1/3

![](https://pbs.twimg.com/media/GLnsaWeWoAA0c-x?format=jpg&name=orig)

**2/** **@KostasAAA** ^1781724277747613724

This happens even when compiler knows that the index varies per thread. To fix this you need to use the NonUniformResourceIndex qualifier. The compiler will then add a waterfall loop to batch wave threads by resource index and ensure that each thread accesses the correct one. 2/3

![](https://pbs.twimg.com/media/GLntvM6W0AEVe0L?format=jpg&name=orig)

**3/** **@KostasAAA** ^1781724279798686001

This can have a performance impact though, with the worst case being each thread indexing a different resource, both in terms of thread coherence (looping over each thread individually) and texture cache. For more info https://www.asawicki.info/news_1734_which_values_are_scalar_in_a_shader 3/3

Branches: [[archive/threads/KostasAAA/2024-04-20-when-using-arrays-of-resources-bindless-its-worth/2024-04-24-jaap_null-its-a-silly-thing-on-many-levels-the-entire-arch]], [[archive/threads/KostasAAA/2024-04-20-when-using-arrays-of-resources-bindless-its-worth/2024-04-24-matiasgoldberg-whats-the-value-of]]
