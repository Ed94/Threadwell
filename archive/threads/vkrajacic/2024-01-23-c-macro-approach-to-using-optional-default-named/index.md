---
title: "C macro approach to using optional / default / named function params, using struct designated initializers."
type: archive
source: twitter
source_url: "https://x.com/vkrajacic/status/1749816169736073295"
author: "Vjekoslav Krajačić"
handle: vkrajacic
post_id: "1749816169736073295"
date: 2024-01-23
archived: 2026-08-25
draft: false
tags:
  - archive
  - twitter
  - vkrajacic
description: "C macro approach to using optional / default / named function params, using struct designated initializers."
in_reply_to: ""
---

## Source

- URL: https://x.com/vkrajacic/status/1749816169736073295
- Author: Vjekoslav Krajačić (@vkrajacic)
- Posted: 2024-01-23 15:27:39

## Thread

**1/** **@vkrajacic** ^1749816169736073295

C macro approach to using optional / default / named function params, using struct designated initializers.
Mandatory values are passed first as standard function params (rect in the example).
Especially useful when a zero value can be made a valid value.

![](https://pbs.twimg.com/media/GEiYTeEbgAAXuRo?format=jpg&name=orig)

Branches: [[archive/threads/vkrajacic/2024-01-23-c-macro-approach-to-using-optional-default-named/2024-01-23-alurmanc-i-love-this]], [[archive/threads/vkrajacic/2024-01-23-c-macro-approach-to-using-optional-default-named/2024-01-23-alurmanc-shouldnt-it-be-transformarguments-parameters-are]], [[archive/threads/vkrajacic/2024-01-23-c-macro-approach-to-using-optional-default-named/2024-01-23-MrJayLC-neat]], [[archive/threads/vkrajacic/2024-01-23-c-macro-approach-to-using-optional-default-named/2024-01-23-DanielcHooper-nice-when-you-combine-this-with-all-the-other]], [[archive/threads/vkrajacic/2024-01-23-c-macro-approach-to-using-optional-default-named/2024-01-23-endu06-how-does-default-work-do-variable-args-bypass]], [[archive/threads/vkrajacic/2024-01-23-c-macro-approach-to-using-optional-default-named/2024-01-23-luis_reyes_x-very-cool-designated-initializers-is-one-thing-i]], [[archive/threads/vkrajacic/2024-01-23-c-macro-approach-to-using-optional-default-named/2024-01-24-falco_girgis-the-only-problem-here-is-that-you-cannot-do-this]], [[archive/threads/vkrajacic/2024-01-23-c-macro-approach-to-using-optional-default-named/2025-08-13-YehorAvramenko-this-one-is-amazing-to-be-honest]], [[archive/threads/vkrajacic/2024-01-23-c-macro-approach-to-using-optional-default-named/2025-08-13-peach2k2-really-cool-but-this-doesnt-mean-c-is-a-good-or]], [[archive/threads/vkrajacic/2024-01-23-c-macro-approach-to-using-optional-default-named/2025-08-13-gretzky00-havent-gotten-to-this-place-i-gotta-keep-pushing]], [[archive/threads/vkrajacic/2024-01-23-c-macro-approach-to-using-optional-default-named/2025-08-13-heyitsvaishnav-this-is-soo-good-i-did-it-in-typescript-as-well]], [[archive/threads/vkrajacic/2024-01-23-c-macro-approach-to-using-optional-default-named/2025-08-13-JLakness-c-functor-method]], [[archive/threads/vkrajacic/2024-01-23-c-macro-approach-to-using-optional-default-named/2025-08-14-emh203-bravo]], [[archive/threads/vkrajacic/2024-01-23-c-macro-approach-to-using-optional-default-named/2025-08-14-etozheya42-lets-go-10k-likes]], [[archive/threads/vkrajacic/2024-01-23-c-macro-approach-to-using-optional-default-named/2025-08-14-siddhantCodes-this-is-so-cool]], [[archive/threads/vkrajacic/2024-01-23-c-macro-approach-to-using-optional-default-named/2025-08-14-EskilSteenberg-am-i-the-only-one-who-thinks-this-is-terrible-its]], [[archive/threads/vkrajacic/2024-01-23-c-macro-approach-to-using-optional-default-named/2025-08-14-FrawaMudi-honestly-i-dont-know-what-i-am-looking-at-anymore]], [[archive/threads/vkrajacic/2024-01-23-c-macro-approach-to-using-optional-default-named/2025-08-14-quantized_state-instantly-rewriting-everything]], [[archive/threads/vkrajacic/2024-01-23-c-macro-approach-to-using-optional-default-named/2025-08-15-k00lagin-i-may-be-just-one-like-but-together-we-build-the]], [[archive/threads/vkrajacic/2024-01-23-c-macro-approach-to-using-optional-default-named/2025-12-29-CarloIlCugino-thank-you]]

**2/** **@pATjako** ^1749816924685672759

**@vkrajacic**

I started experimenting with that in my imgui as well, it is kinda neat, also you can make the same code work for C & C++ (with some limitation in argument ordering)
