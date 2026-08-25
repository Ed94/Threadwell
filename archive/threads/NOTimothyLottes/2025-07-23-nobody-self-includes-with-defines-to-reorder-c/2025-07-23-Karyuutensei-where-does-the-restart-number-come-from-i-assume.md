---
title: "@NOTimothyLottes Where does the restart number come from? I assume this is how many times you exited the code and started again automatically using your batch script?"
type: archive
source: twitter
source_url: "https://x.com/Karyuutensei/status/1948052805647782109"
author: "Nick Tasios"
handle: Karyuutensei
post_id: "1948052805647782109"
date: 2025-07-23
archived: 2026-08-23
draft: false
tags:
  - archive
  - twitter
  - NOTimothyLottes
description: "@NOTimothyLottes Where does the restart number come from? I assume this is how many times you exited the code and started again automatically using your batch script?"
in_reply_to: ""
parent_post_id: "1948009807161721332"
---

## Source

- URL: https://x.com/Karyuutensei/status/1948052805647782109
- Author: Nick Tasios (@Karyuutensei)
- Posted: 2025-07-23 16:09:16

## Branch

**1/** @Karyuutensei

@NOTimothyLottes

Where does the restart number come from? I assume this is how many times you exited the code and started again automatically using your batch script?

**2/**

@Karyuutensei Yeah exactly that. The log file is a fixed size, and memory mapped (+page warming), and lines are a fixed size, so writing a message is lock free (fast just one atomic add, no file or system calls). When it fills it wraps around, and to clear just delete the file (it recreates it

**3/**

@NOTimothyLottes Thanks for sharing. I’ve never thought of doing logging like this.

## Related

- Spine: [[archive/threads/NOTimothyLottes/2025-07-23-nobody-self-includes-with-defines-to-reorder-c]]
