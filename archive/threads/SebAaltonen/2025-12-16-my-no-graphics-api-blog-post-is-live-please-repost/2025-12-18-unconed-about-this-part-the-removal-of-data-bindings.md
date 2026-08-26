---
title: "About this part:"
type: archive
source: twitter
source_url: "https://x.com/unconed/status/2001622483024196083"
author: "unconed 🛸💫🌞"
handle: unconed
post_id: "2001622483024196083"
date: 2025-12-18
archived: 2026-08-26
draft: false
tags:
  - archive
  - twitter
  - SebAaltonen
description: "About this part:"
in_reply_to: ""
parent_post_id: "2001000839574643138"
---

## Source

- URL: https://x.com/unconed/status/2001622483024196083
- Author: unconed 🛸💫🌞 (@unconed)
- Posted: 2025-12-18 11:56:02

## Branch

**1/** **@unconed** ^2001622483024196083

About this part:

>The removal of data bindings makes vertex and pixel shaders simpler to use. All of the complex data bindings APIs are replaced by a 64-bit GPU pointer. Users are able to write flexible vertex fetch code to avoid creating a PSO permutation per vertex layout.

If there is no PSO permutation, then the `varying` attributes have to be identical, no? If so, what would be the use case for writing flexible vertex fetch code, if the data to be fetched is still all the same?

**2/** **@SebAaltonen** ^2001670094389186605

**@unconed**

Depends on what you want to achieve. You can load pixel data often in pixel shader directly. Don't need to pass it through the vertex shader.

**3/** **@unconed** ^2001674041078301046

That seems somewhat contradictory as you said "writing flexible vertex fetch code". I can see a use-case for e.g. procedural vertex gen here, but flexible fetching seems to imply flexible attributes in practice.

What you propose here would instead mean having a few general purpose attributes like UV and material ID, with perhaps an extra "wildcard" vec of u32 and f32 to make it 'extensible'. That seems like the opposite of what you are arguing for in the post, which is use-specific structs and union-type polymorphism.

**4/** **@SebAaltonen** ^2001682534887764338

Many modern renderers use V-buffer or similar. Texturing and lighting is fully deferred. Nanite for example does it like this.

If you need different varyings then you need a different PSO, because the hardware needs to reserve different amount of space for the varyings. The allocation happens before your shader runs, so you can't configure it inside your shader.

## Related

- Spine: [[archive/threads/SebAaltonen/2025-12-16-my-no-graphics-api-blog-post-is-live-please-repost]]
