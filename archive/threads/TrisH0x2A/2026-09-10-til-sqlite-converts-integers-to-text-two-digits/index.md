---
title: "TIL SQLite converts integers to text two digits at a time"
type: archive
source: twitter
source_url: "https://x.com/TrisH0x2A/status/2098135741075497111"
author: "trish"
handle: TrisH0x2A
post_id: "2098135741075497111"
date: 2026-09-10
archived: 2026-11-16
draft: false
tags:
  - archive
  - twitter
  - TrisH0x2A
description: "TIL SQLite converts integers to text two digits at a time"
in_reply_to: ""
---

## Source

- URL: https://x.com/TrisH0x2A/status/2098135741075497111
- Author: trish (@TrisH0x2A)
- Posted: 2026-09-10 19:45:16

## Thread

**1/** **@TrisH0x2A** ^2098135741075497111

TIL SQLite converts integers to text two digits at a time

converting an integer to text usually means a loop of /10 and %10

sqlite avoids most of those divisions by keeping a 200-byte string of every two-digit pair from 00 to 99, and pulling two digits at a time out of it by direct index instead of computing them

![](https://pbs.twimg.com/media/HR4TS3nbAAASl7c?format=png&name=orig)

Branches: [[archive/threads/TrisH0x2A/2026-09-10-til-sqlite-converts-integers-to-text-two-digits/2026-09-10-onetyone_a-did-you-solve-the-hyphen-problem]], [[archive/threads/TrisH0x2A/2026-09-10-til-sqlite-converts-integers-to-text-two-digits/2026-09-10-MaiHoonHira-200-bytes-to-halve-the-divides-good-trade]], [[archive/threads/TrisH0x2A/2026-09-10-til-sqlite-converts-integers-to-text-two-digits/2026-09-11-Dark_Goldenrod-thats-pretty-cool-in-writing-my-upcoming-database]], [[archive/threads/TrisH0x2A/2026-09-10-til-sqlite-converts-integers-to-text-two-digits/2026-09-11-silenceofnight-heres-how-to-convert-an-integer-to-a-number-with]], [[archive/threads/TrisH0x2A/2026-09-10-til-sqlite-converts-integers-to-text-two-digits/2026-09-11-mathtician-ithkuil-is-base-100-coincidence]], [[archive/threads/TrisH0x2A/2026-09-10-til-sqlite-converts-integers-to-text-two-digits/2026-09-11-max_conradt-this-is-how-rust-does-it-as-well-if-you-run]], [[archive/threads/TrisH0x2A/2026-09-10-til-sqlite-converts-integers-to-text-two-digits/2026-09-11-da_miao_zi-using-sqlite3digitpairs]], [[archive/threads/TrisH0x2A/2026-09-10-til-sqlite-converts-integers-to-text-two-digits/2026-09-11-istartedi-thats-actually-a-fairly-standard-tactic-theres-an]], [[archive/threads/TrisH0x2A/2026-09-10-til-sqlite-converts-integers-to-text-two-digits/2026-09-11-jannone-funny-i-had-to-do-that-when-programming-a-game]], [[archive/threads/TrisH0x2A/2026-09-10-til-sqlite-converts-integers-to-text-two-digits/2026-09-11-minusYCore-most-meaning-half]], [[archive/threads/TrisH0x2A/2026-09-10-til-sqlite-converts-integers-to-text-two-digits/2026-09-11-noop_dev-no-you-do-zero-a-actual-divisions-those-are-slow]], [[archive/threads/TrisH0x2A/2026-09-10-til-sqlite-converts-integers-to-text-two-digits/2026-09-11-zaafonin-can-also-be-found-in-factorio]], [[archive/threads/TrisH0x2A/2026-09-10-til-sqlite-converts-integers-to-text-two-digits/2026-09-12-yashv_singh-and-how-does-it-pull-out-2-digits-from-the-number]]

**2/** **@QuadooScript** ^2098137931236176156

**@TrisH0x2A** **@grok**

What are the real world metrics on this performance design?
