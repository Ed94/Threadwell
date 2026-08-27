---
title: "@SebAaltonen I like how Jai solved this."
type: archive
source: twitter
source_url: "https://x.com/SergeyLerg/status/1698365089701642504"
author: "Sergey Lerg"
handle: SergeyLerg
post_id: "1698365089701642504"
date: 2023-09-03
archived: 2026-08-27
draft: false
tags:
  - archive
  - twitter
  - SebAaltonen
description: "@SebAaltonen I like how Jai solved this."
in_reply_to: ""
parent_post_id: "1698355711422476302"
---

## Source

- URL: https://x.com/SergeyLerg/status/1698365089701642504
- Author: Sergey Lerg (@SergeyLerg)
- Posted: 2023-09-03 15:59:26

## Branch

**1/** **@SergeyLerg** ^1698365089701642504

**@SebAaltonen**

I like how Jai solved this. You can return dynamically allocated data just fine because every function has access to a temporary allocator (linear block of reserved heap memory). Most data is short lived and the temporary storage is cleaned at e.g. the end of a game render frame

**2/** **@SebAaltonen** ^1698366857537794256

**@SergeyLerg**

Yes. That's how C/C++ based game engines tend to do it as well. You just use linear temp allocator (reset at end of frame). But a stack based temp allocator would be even better here. Even better if integrated to the language. Would be easy to use = would be the default for all.

## Related

- Spine: [[archive/threads/SebAaltonen/2023-09-03-somebody-asked-why-you-cant-return-arrays-dynamic]]
