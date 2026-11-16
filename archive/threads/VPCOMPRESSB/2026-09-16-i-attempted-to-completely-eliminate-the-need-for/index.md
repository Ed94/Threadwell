---
title: "i attempted to completely eliminate the need for functions in C via inline/embedded functions within the main function, with very minimal assembly, while being able to define variables, types, constants, and other symbols once locally around the relevant code."
type: archive
source: twitter
source_url: "https://x.com/VPCOMPRESSB/status/2100097964240773122"
author: "/i:'mɪər/"
handle: VPCOMPRESSB
post_id: "2100097964240773122"
date: 2026-09-16
archived: 2026-11-16
draft: false
tags:
  - archive
  - twitter
  - VPCOMPRESSB
description: "i attempted to completely eliminate the need for functions in C via inline/embedded functions within the main function, with very minimal assembly, while being able to define variables, types, constants, and other symbols once locally around the relevant code."
in_reply_to: ""
---

## Source

- URL: https://x.com/VPCOMPRESSB/status/2100097964240773122
- Author: /i:'mɪər/ (@VPCOMPRESSB)
- Posted: 2026-09-16 05:42:27

## Thread

**1/** **@VPCOMPRESSB** ^2100097964240773122

i attempted to completely eliminate the need for functions in C via inline/embedded functions within the main function, with very minimal assembly, while being able to define variables, types, constants, and other symbols once locally around the relevant code.

![](https://pbs.twimg.com/media/HSUL-AXWcAACcOM?format=jpg&name=orig)
![](https://pbs.twimg.com/media/HSUL-AYWMAA4DD0?format=jpg&name=orig)

**2/** **@VPCOMPRESSB** ^2100097967482892579

i ended up encountering annoying compiler bugs and gimmicks from GCC and Clang, especially with explicit register variables.

Clang doesn't support local explicit register variables, and GCC's is broken, plus its debug info (-g).

ultimately, i went back to assembly.

**3/** **@VPCOMPRESSB** ^2100098273474138224

i had it working with GCC, but debugging (-g) is broken.

i definitely see the value of having a builtin debugger embedded in the program itself rather than an external once.
