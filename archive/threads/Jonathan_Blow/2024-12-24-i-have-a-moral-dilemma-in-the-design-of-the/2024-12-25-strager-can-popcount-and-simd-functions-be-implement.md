---
title: "@Jonathan_Blow @rflaherty71 Can popcount and SIMD functions be implement using inline assembly? It sounds like they're built into the compiler right now rather than the standard library."
type: archive
source: twitter
source_url: "https://x.com/strager/status/1871740861048140288"
author: "strager"
handle: strager
post_id: "1871740861048140288"
date: 2024-12-25
archived: 2026-08-26
draft: false
tags:
  - archive
  - twitter
  - Jonathan_Blow
description: "@Jonathan_Blow @rflaherty71 Can popcount and SIMD functions be implement using inline assembly? It sounds like they're built into the compiler right now rather than the standard library."
in_reply_to: ""
parent_post_id: "1871638900554317934"
---

## Source

- URL: https://x.com/strager/status/1871740861048140288
- Author: strager (@strager)
- Posted: 2024-12-25 02:12:51

## Branch

**1/** **@strager** ^1871740861048140288

**@Jonathan_Blow** **@rflaherty71**

Can popcount and SIMD functions be implement using inline assembly? It sounds like they're built into the compiler right now rather than the standard library.

**2/** **@Jonathan_Blow** ^1871779516584165382

**@strager** **@rflaherty71**

They are currently implemented as inline assembly, but I don’t really like this, and especially don’t like the vision of how this looks when supporting many platforms.

**3/** **@AgileJebrim** ^1871780076150550779

**@Jonathan_Blow** **@strager** **@rflaherty71**

Have you considered using SPIR-V as an IR to target instead? It lacks the bloat of LLVM but one can conceivably design something with it to target various other SIMD backends.

**4/** **@Jonathan_Blow** ^1872380932617105796

**@AgileJebrim** **@strager** **@rflaherty71**

That is a pretty weird idea...

**5/** **@AgileJebrim** ^1872386383861756205

**@Jonathan_Blow** **@strager** **@rflaherty71**

You’d be able to run on GPUs too.

## Related

- Spine: [[archive/threads/Jonathan_Blow/2024-12-24-i-have-a-moral-dilemma-in-the-design-of-the]]
