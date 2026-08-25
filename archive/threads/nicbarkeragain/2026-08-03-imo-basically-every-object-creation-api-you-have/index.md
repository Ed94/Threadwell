---
title: "IMO basically every \"object creation API\" you have should take a string label that is for internal use only."
type: archive
source: twitter
source_url: "https://x.com/nicbarkeragain/status/2084072929780998198"
author: "Nic Barker"
handle: nicbarkeragain
post_id: "2084072929780998198"
date: 2026-08-03
archived: 2026-08-25
draft: false
tags:
  - archive
  - twitter
  - nicbarkeragain
description: "IMO basically every \"object creation API\" you have should take a string label that is for internal use only."
in_reply_to: ""
---

## Source

- URL: https://x.com/nicbarkeragain/status/2084072929780998198
- Author: Nic Barker (@nicbarkeragain)
- Posted: 2026-08-03 00:24:41

## Thread

**1/** **@nicbarkeragain** ^2084072929780998198

IMO basically every "object creation API" you have should take a string label that is for internal use only. You can ifdef them out in release, but it will save you so much grief when debugging. UI elements, mem allocations, input actions, just tag them all with a label / name.

Branches: [[archive/threads/nicbarkeragain/2026-08-03-imo-basically-every-object-creation-api-you-have/2026-08-03-exacoustics-iirc-sokol-gfx-does-this-its-really-nice-ive]], [[archive/threads/nicbarkeragain/2026-08-03-imo-basically-every-object-creation-api-you-have/2026-08-03-RealOtisCrune-isnt-this-just-a-python-style-docstring-with]], [[archive/threads/nicbarkeragain/2026-08-03-imo-basically-every-object-creation-api-you-have/2026-08-03-_can1357-https-learn-microsoft-com-en-us-windows-hardware]], [[archive/threads/nicbarkeragain/2026-08-03-imo-basically-every-object-creation-api-you-have/2026-08-03-petey_fo_really-ya-tagging-allocations-and-frames-to-actual]], [[archive/threads/nicbarkeragain/2026-08-03-imo-basically-every-object-creation-api-you-have/2026-08-03-joseph_h_garvin-when-ive-seen-this-they-usually-require-unique]], [[archive/threads/nicbarkeragain/2026-08-03-imo-basically-every-object-creation-api-you-have/2026-08-03-RazorSharpFang-i-dont-suppose-you-could-demonstrate-this-with-a]], [[archive/threads/nicbarkeragain/2026-08-03-imo-basically-every-object-creation-api-you-have/2026-08-03-BurnZeZ-i-do-and-access-it-via-9p]], [[archive/threads/nicbarkeragain/2026-08-03-imo-basically-every-object-creation-api-you-have/2026-08-03-DjMolehill-brb-adding-this-to-my-codebase]], [[archive/threads/nicbarkeragain/2026-08-03-imo-basically-every-object-creation-api-you-have/2026-08-03-onepopcorn-thats-actually-a-smart-idea-do-you-have-an]], [[archive/threads/nicbarkeragain/2026-08-03-imo-basically-every-object-creation-api-you-have/2026-08-03-Leonardo_Temp-you-can-also-implicitly-pass-the-source-code]], [[archive/threads/nicbarkeragain/2026-08-03-imo-basically-every-object-creation-api-you-have/2026-08-03-MikeyBally-this-is-the-way]], [[archive/threads/nicbarkeragain/2026-08-03-imo-basically-every-object-creation-api-you-have/2026-08-04-codeshaunted-webgpu-has-this-and-its-a-life-saver-for-debugging]], [[archive/threads/nicbarkeragain/2026-08-03-imo-basically-every-object-creation-api-you-have/2026-08-04-Mallchad-i-accidentally-discovered-this-myself-it-just]], [[archive/threads/nicbarkeragain/2026-08-03-imo-basically-every-object-creation-api-you-have/2026-08-04-Tomi_Tapio-function-draw-string-for-debug-in-my-games-3d]], [[archive/threads/nicbarkeragain/2026-08-03-imo-basically-every-object-creation-api-you-have/2026-08-08-Drainyard-this-just-saved-me-from-hours-of-debugging]]

**2/** **@nicbarkeragain** ^2084072932293386379

There's seriously nothing like going from "we have this memory leak every frame and don't know where tf it is" to "I paused the debugger and inspected the list of allocations, and there are 10,000 of them all labelled 'FormattedUnitName', so I grepped it in 5 seconds"

Branches: [[archive/threads/nicbarkeragain/2026-08-03-imo-basically-every-object-creation-api-you-have/2026-08-03-borrowck_novel-can-you-post-an-example-of-how-you-would]]
