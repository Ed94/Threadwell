---
title: "Before moving all GPU-side, I had source recompile while running."
type: archive
source: twitter
source_url: "https://x.com/NOTimothyLottes/status/1737499394633560366"
author: "NOTimothyLottes"
handle: NOTimothyLottes
post_id: "1737499394633560366"
date: 2023-12-20
archived: 2026-08-26
draft: false
tags:
  - archive
  - twitter
  - NOTimothyLottes
description: "Before moving all GPU-side, I had source recompile while running."
in_reply_to: ""
---

## Source

- URL: https://x.com/NOTimothyLottes/status/1737499394633560366
- Author: NOTimothyLottes (@NOTimothyLottes)
- Posted: 2023-12-20 15:45:11

## Thread

**1/** **@NOTimothyLottes** ^1737499394633560366

Before moving all GPU-side, I had source recompile while running. I'd place all global data in one structure, and pass that pointer to the DLL/SO on reload. This was done via self-including to make code layout easy. I still do that practice today:

![](https://pbs.twimg.com/media/GBzWN-cXAAAN_j_?format=png&name=orig)

**2/** **@NOTimothyLottes** ^1737500234870067342

Using {DEF_,TYP_,RAM_,ROM_} defines to denote what pass of the self include to place the code in. So anything in RAM_ for example gets dumped into the global data structure. Nice for keeping code concept locality in the source.

![](https://pbs.twimg.com/media/GBzWzoQXMAAeFdS?format=png&name=orig)
