---
title: "@rfleury Do you suggest to do it right after main, and continue throughout the entire program?"
type: archive
source: twitter
source_url: "https://x.com/wookash_podcast/status/1976605001762877467"
author: "Łukasz | Wookash Podcast"
handle: wookash_podcast
post_id: "1976605001762877467"
date: 2025-10-10
archived: 2026-08-25
draft: false
tags:
  - archive
  - twitter
  - rfleury
description: "@rfleury Do you suggest to do it right after main, and continue throughout the entire program?"
in_reply_to: ""
parent_post_id: "1976458516325073141"
---

## Source

- URL: https://x.com/wookash_podcast/status/1976605001762877467
- Author: Łukasz | Wookash Podcast (@wookash_podcast)
- Posted: 2025-10-10 11:05:30

## Branch

**1/** **@wookash_podcast** ^1976605001762877467

**@rfleury**

Do you suggest to do it right after main, and continue throughout the entire program?

Or for the explicit sections that you want to make parallel

**2/** **@rfleury** ^1976610334338396547

I do it immediately, so that the entire program—from start to finish—is parallel like this.

The one caveat is when you want many thread groups for a variety of “timelines”. For example, in the debugger, I can’t have the UI thread run in lockstep with the control thread. So those get different thread groups. (I wrote both threads before I knew everything in the article, so those are just single threads right now…)

I just recently rewrote the PDB -> RDI converter in this style, and the very first thing the program does is kick off a bunch of threads which run the “actual” entry point.

**3/** **@octocamo_bc** ^1976901884003991816

**@rfleury** **@wookash_podcast**

So the whole RAD debugger codebase transitioned/is transitioning to multi-core by default?

Amazing article by the way.

## Related

- Spine: [[archive/threads/rfleury/2025-10-10-new-post-multi-core-by-default]]
