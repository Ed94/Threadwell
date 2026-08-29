---
title: "Before mastering SIMD you have to master loop unswitching"
type: archive
source: twitter
source_url: "https://x.com/_Felipe/status/2092653743779069989"
author: "Felipe O. Carvalho"
handle: _Felipe
post_id: "2092653743779069989"
date: 2026-08-26
archived: 2026-08-29
draft: false
tags:
  - archive
  - twitter
  - _Felipe
description: "Before mastering SIMD you have to master loop unswitching"
in_reply_to: ""
---

## Source

- URL: https://x.com/_Felipe/status/2092653743779069989
- Author: Felipe O. Carvalho (@_Felipe)
- Posted: 2026-08-26 16:41:46

## Thread

**1/** **@_Felipe** ^2092653743779069989

Before mastering SIMD you have to master loop unswitching

![](https://pbs.twimg.com/media/HQqZfHiWAAAJmBs?format=jpg&name=orig)

**2/** **@nicbarkeragain** ^2092725850181607870

**@_Felipe**

The responses here saying the compiler does it for you are all assuming it’s a simple boolean in the conditional. If it’s remotely complex (function call etc) the compiler won’t touch it as it might produce different results each iteration.

**3/** **@Lucrecious_** ^2093132360388886820

Yes - it's better to unswitch loops, but looking at the metrics for this, it doesn't seem like it makes *that* much of a difference until you get into an absurd amount of iterations.

Still learning about this type of stuff, so I'm sorry if I'm off-base here or if I'm misunderstanding the purpose of the post. 

Here's the code I used:
https://pastecode.io/s/27hpiw45
(I'm open to this not being a great benchmarking technique, but if there are better ways to do this, would love to learn!)

I tried with different Ns, the highest being 1 billion iterations. In all cases, the overall processing time was pretty short; ~1 second.

For N = 1 billion I got:
Inner Loop Conditional: ~1600ms
Outer Loop Conditional: ~1400ms

That's like a ~10% performance win which, admittedly, is very good, but only 200ms faster total on a billion iterations.

With smaller Ns, the performance gained varied. At its best, outer conditional was 20% faster, but that was only ~20ms faster compared to the inner conditional.

These functions are also doing very little work - I feel like the conditional check could easily be overshadowed by the actual work being done in the branches, no?

OP doesn't specify what f and g are - they could be doing anything. Like, in a real program, wouldn't f and g be doing more work? 

I tried it by generating random numbers inside f and g and the difference between the outer and inner conditional was even smaller. We're talking <1% difference.

If you're doing a function call instead of a variable check for the flag, things would be different, but I think that's a different issue entirely. I thought OPs snippet was getting at unnecessary branching in a loop rather than unnecessary function calls in a loop.

If this is for optimizing for SIMD, this seems sort of obvious to anyone that knows anything about it? Not sure why it needs to "mastered".

Yes, one is better than the other, but in OP's example, it's very easy to pull the conditional outside the loop. In real code, it might not be so trivial to do; and without benchmarking your specific case, can we really say this is worth doing in a rule-of-thumb type of way? 

I'm genuinely curious in what scenarios we should care about this. It seems like it only matters in really trivial and obvious cases, like filling giant arrays or doing very simple high-iteration calculations. As soon as f or g is doing any significant amount of work, the conditional check seems inconsequential to the overall performance.

Where's my knowledge gap on this? Genuinely curious, because I see a lot of "you should do this instead of that" on here but without any metrics or real examples...

**4/** **@nicbarkeragain** ^2093150794032046345

Great that you're digging into it and questioning, that's super important 🙂
As with everything performance related, there's the lottery involved and it's very hard to microbench something trivial like this. Rather than only observing the test run time (which could be affected by a huge number of things) it's important to actually look at the compiler output - if both of your cases are being vectorised then the compiler is being smart and there's significantly less to gain from doing this manually, but that's not guaranteed.
Re: the post, I've personally found that it's almost impossible to get both meaningful and educational code samples into a single screenshot when it comes to performance, because in order to make it clear and easy to understand it needs to be simple, but the compiler works really well on trivial cases, and falls apart in unpredictable ways on more complex ones.
You're pretty much exactly on the right track in that the cost of the branch by definition won't be significant, because it needs to be invariant to be even possible to hoist out of the loop in the first place, but if it's invariant that means it's 100% predictable and will cost almost nothing. So my general assumption here was that "flag" was just a stand-in for "some expression inside a conditional", and at a higher level it's just advice to start to develop the pattern recognition for loop invariant reads (hoisting invariants also results in code that is easier to reason about IMO)
From a more realistic performance perspective:
- It's hard to know from just eyeballing whether a compiler is going to be able to successfully vectorise a loop body, you really need to be looking at the actual compiler output of your specific case while making tweaks until it looks how you expect
- If the data read by the rest of the loop body after the branch is enough to nuke your entire L1, the branch condition lookup is going to be (another) cache miss, and I really couldn't tell you for certain how that's going to interact with the branch prediction latency at high throughput. Maybe it would be hidden, maybe an l1 miss would still cause some stall. YMMV 🙂

> If this is for optimizing for SIMD, this seems sort of obvious to anyone that knows anything about it?

My read on this was to try to be a bit generous with the interpretation - removing loop invariant branches actually is an important step to getting the compiler to auto vectorise, and when I first learned it, it wasn't super obvious to me before someone more senior pointed it out 🙂

**5/** **@Lucrecious_** ^2093228771155329294

I appreciate the response!

You're right - the more I look into it, the more nuanced it becomes. Not so simple to measure.

Funnily enough, this post inspired me to experiment with performance optimization today (trying to learn).

I was trying to read 10GBs of data into memory as fast as possible, and, although my NVMe's theoretical read is 5GB/s, trying to get anywhere near the ballpark of 2 seconds to load does not seem trivial at all. Small adjustments, like read buffer size, can have quite significant effects on performance (like 20s to 13s type of stuff).

I mention that because despite me thinking I had a pretty good idea of what was going on behind the scenes, I was met with a lot of unexpected results. It put into question my benchmarks for this - are they even timing the right thing? Is there code in there that I think is inconsequential but actually isn't? Does the timing even mean anything?

All very interesting...
