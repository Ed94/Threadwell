---
title: "@nicbarkeragain Hmmn."
type: archive
source: twitter
source_url: "https://x.com/geofflangdale/status/1945401263774162962"
author: "Geoff Langdale"
handle: geofflangdale
post_id: "1945401263774162962"
date: 2025-07-16
archived: 2026-08-25
draft: false
tags:
  - archive
  - twitter
  - nicbarkeragain
description: "@nicbarkeragain Hmmn."
in_reply_to: ""
parent_post_id: "1944913662499516737"
---

## Source

- URL: https://x.com/geofflangdale/status/1945401263774162962
- Author: Geoff Langdale (@geofflangdale)
- Posted: 2025-07-16 08:32:59

## Branch

**1/** **@geofflangdale** ^1945401263774162962

**@nicbarkeragain**

Hmmn. I feel most of the PL design community - who have many folks I have the greatest admiration for, to be clear - is really fundamentally not that interested in the reality of the actual instructions on the machine.

If the choice is to have SIMD ...

**2/** **@geofflangdale** ^1945401680868335902

**@nicbarkeragain**

programming smothered in a bureaucratic pile of type theory or some intrusive, hard-to-understand "magical autovec" system, my response to their help is, like the proverbial French merchants, "Laissez-nous faire".

What I'd really like to see - a small but modest step - is a ...

**3/** **@geofflangdale** ^1945402059345551381

**@nicbarkeragain**

run-time that pads out the start and end of every region (stack, globals, heap)  - *not* every data item - with 63 bytes of padding so that any SIMD access can be done without the weird risk that we're right next to a unmapped page or some device with weird semantics ("on ...

**4/** **@joseph_h_garvin** ^1945557778514215240

**@geofflangdale** **@nicbarkeragain**

I'm an aspiring PL+perf person that does care but I seem to be rare 😅 I think the situation is worse than this though...

**5/** **@joseph_h_garvin** ^1945557912790655000

**@geofflangdale** **@nicbarkeragain**

Even if your allocator/linker/etc guarantee there's always an extra 63 zero bytes the C(++)/Rust lang semantics still allow the optimizer to launch missiles when you go out of bounds. That's UB, so now it can do whatever it wants instead. So you need lang semantics to change too.

**6/** **@geofflangdale** ^1945608389754863630

**@joseph_h_garvin** **@nicbarkeragain**

Yes, I'd include this with the run-time changes. Personally, I think a good deal of UB (not all, of course) feels somewhat fatuous, but I don't really study the area closely enough to understand how much we could do without.

## Related

- Spine: [[archive/threads/nicbarkeragain/2025-07-15-i-cant-help-but-have-this-feeling-that-were]]
