---
title: "@valigo if by \"hardware locks\" you mean things like x86's `lock` prefix then there's a difference - that guarantees atomicity but unlike SW locks it can't deadlock etc so forward progress and correctness are both guaranteed."
type: archive
source: twitter
source_url: "https://x.com/SheriefFYI/status/2032522450622447636"
author: "Sherief, FYI"
handle: SheriefFYI
post_id: "2032522450622447636"
date: 2026-03-13
archived: 2026-08-26
draft: false
tags:
  - archive
  - twitter
  - valigo
description: "@valigo if by \"hardware locks\" you mean things like x86's `lock` prefix then there's a difference - that guarantees atomicity but unlike SW locks it can't deadlock etc so forward progress and correctness are both guaranteed."
in_reply_to: ""
parent_post_id: "2032270128524537899"
---

## Source

- URL: https://x.com/SheriefFYI/status/2032522450622447636
- Author: Sherief, FYI (@SheriefFYI)
- Posted: 2026-03-13 18:21:29

## Branch

**1/** **@SheriefFYI** ^2032522450622447636

**@valigo**

if by "hardware locks" you mean things like x86's `lock` prefix then there's a difference - that guarantees atomicity but unlike SW locks it can't deadlock etc so forward progress and correctness are both guaranteed. you're still susceptible to False Sharing etc

**2/** **@valigo** ^2032531081874784319

**@SheriefFYI**

There's a difference, yes, but calling them "lock-free" feels like a marketing shtick still. Kinda like "UB". Maybe I'm too autistic, so to speak, but I don't like when words do not mean what they supposed to mean, even though I sometimes do the same.

## Related

- Spine: [[archive/threads/valigo/2026-03-13-human-nature-is-to-oversell-things]]
