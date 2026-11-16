---
title: "TIL: you can increase hot loop performance by 20x by properly exploiting store forwarding property on modern CPUs."
type: archive
source: twitter
source_url: "https://x.com/valyala/status/2118349666911768669"
author: "Aliaksandr Valialkin"
handle: valyala
post_id: "2118349666911768669"
date: 2026-11-05
archived: 2026-11-16
draft: false
tags:
  - archive
  - twitter
  - valyala
description: "TIL: you can increase hot loop performance by 20x by properly exploiting store forwarding property on modern CPUs."
in_reply_to: ""
---

## Source

- URL: https://x.com/valyala/status/2118349666911768669
- Author: Aliaksandr Valialkin (@valyala)
- Posted: 2026-11-05 14:28:12

## Thread

**1/** **@valyala** ^2118349666911768669

TIL: you can increase hot loop performance by 20x by properly exploiting store forwarding property on modern CPUs. And Go better fits than Rust for achieving this performance boost, since it doesn't automatically reorder struct fields.

Branches: [[archive/threads/valyala/2026-11-05-til-you-can-increase-hot-loop-performance-by-20x/2026-11-05-VictoriqueM-go-preserving-struct-field-order-gives-more]], [[archive/threads/valyala/2026-11-05-til-you-can-increase-hot-loop-performance-by-20x/2026-11-05-DmytroKrasun-a-bit-off-topic-but-have-you-ever-considered-to]], [[archive/threads/valyala/2026-11-05-til-you-can-increase-hot-loop-performance-by-20x/2026-11-05-JosepiBuildsIt-rust-can-preserve-field-order-too-with-repr-c]], [[archive/threads/valyala/2026-11-05-til-you-can-increase-hot-loop-performance-by-20x/2026-11-06-theodorvaryag-race-me]], [[archive/threads/valyala/2026-11-05-til-you-can-increase-hot-loop-performance-by-20x/2026-11-06-bitnxs-a-great-reminder-to-benchmark-the-generated-code]]

**2/** **@pskocik** ^2118742360083546486

**@valyala**

If you only access the memory through non-union struct fields, field order doesn't matter for this.

**3/** **@valyala** ^2118783308847018146

**@pskocik**

If a struct contains fields with sizes smaller than a word (8 bytes on 64-bit CPUs) or smaller than a cache line (64 bytes on AMD64 CPUs), then writing to these fields and then reading adjacent fields may result in stalls described in the article.

**4/** **@pskocik** ^2118791696544674247

**@valyala**

You're mixing that up with false sharing which resolves in slowdowns with multithreaded access. Store buffer forwarding speeds up loads for local stores that haven't reached the cache yet, but it needs exact overlap and size match ...

**5/** **@pskocik** ^2118792868563210292

**@valyala**

... Like if you store a 4-byte with a movl & then you try to get the highest byte of it, you want to reload the full 4-byte & bitshift, not do `movb 3(%ptr), %al;`. Unfortuntely compilers (saw this on clang) will sometimes "optimize" a C-based int-load+shift into such a byteload.

**6/** **@pskocik** ^2118793806900293782

**@valyala**

Observed this with bitfield codegen too. It unfortunately blocks this  store-buffer forwarding (as it's documented in Intel Optimization Manuals too) and the effect is well measurable. Discrete adjacent fields shouldn't have an effect here, only on false sharing.

**7/** **@forked_franz** ^2119028978841432328

**@pskocik** **@valyala**

That means that first init of memory, which could be zeroed, for small object, is better happen with separate mov with 0 immediate instead of memset-like calls (4 or more based on issue width ^^)

**8/** **@pskocik** ^2119049923102720143

**@forked_franz** **@valyala**

I had originally gotten the rules slightly wrong. Smaller loads following bigger stores is OK as long as the starting address is the same.
But I just did my benchmarks on my Comet Lake CPU and I the offsetted loads were surprisingly on par with offset-0 loads...

![](https://pbs.twimg.com/media/HWhel_9XsAAY4aR?format=png&name=orig)

Branches: [[archive/threads/valyala/2026-11-05-til-you-can-increase-hot-loop-performance-by-20x/2026-11-07-pskocik-only-rule42-violations-produced-a-significant]]

**9/** **@forked_franz** ^2119058837994938500

**@pskocik** **@valyala**

So that applies by reading a byte out of a 64bit written value? I have to check on old good SO Peter Cordes answers on where it actually haplen and how eheh

**10/** **@pskocik** ^2119063268861886562

**@forked_franz** **@valyala**

More on this: https://x.com/pskocik/status/2119054050536640526
TL;DR: Rule 41 obsolete since Sandy Bridge; Rule 42 continues to be *very* valid.
