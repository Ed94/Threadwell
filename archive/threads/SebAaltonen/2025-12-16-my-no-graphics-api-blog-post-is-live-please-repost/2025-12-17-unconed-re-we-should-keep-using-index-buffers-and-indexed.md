---
title: "Re: we should keep using index buffers and indexed vertices"
type: archive
source: twitter
source_url: "https://x.com/unconed/status/2001358742877503601"
author: "unconed 🛸💫🌞"
handle: unconed
post_id: "2001358742877503601"
date: 2025-12-17
archived: 2026-08-26
draft: false
tags:
  - archive
  - twitter
  - SebAaltonen
description: "Re: we should keep using index buffers and indexed vertices"
in_reply_to: ""
parent_post_id: "2001000839574643138"
---

## Source

- URL: https://x.com/unconed/status/2001358742877503601
- Author: unconed 🛸💫🌞 (@unconed)
- Posted: 2025-12-17 18:28:02

## Branch

**1/** **@unconed** ^2001358742877503601

Re: we should keep using index buffers and indexed vertices

Having every single vertex attribute be indexed means you need duplicate vertices to handle cases where you have attribute seams (e.g. flipped tangents). This requires data-dependent splitting and reprocessing, which may not be feasable at runtime.

I would much prefer a model that supports mixing "welded" and "unwelded" data instead. Do you think such a model can work? Or is it not feasible to cache partial vertices?

I wonder because both driver devs and engine devs seem to be converging on the same sorts of shader preprocessing steps anyway (dead code elimination, attribute grouping, etc). If the vertex/fragment pipeline is a facade, couldn't we model this as a more directly in user-space instead?

## Related

- Spine: [[archive/threads/SebAaltonen/2025-12-16-my-no-graphics-api-blog-post-is-live-please-repost]]
