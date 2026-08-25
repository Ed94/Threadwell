---
title: "Working through rough draft of assembly for a different idea for a micro macro-forth."
type: archive
source: twitter
source_url: "https://x.com/NOTimothyLottes/status/2079742177370841105"
author: "NOTimothyLottes"
handle: NOTimothyLottes
post_id: "2079742177370841105"
date: 2026-07-22
archived: 2026-08-24
draft: false
tags:
  - archive
  - twitter
  - NOTimothyLottes
description: "Working through rough draft of assembly for a different idea for a micro macro-forth."
in_reply_to: ""
---

## Source

- URL: https://x.com/NOTimothyLottes/status/2079742177370841105
- Author: NOTimothyLottes (@NOTimothyLottes)
- Posted: 2026-07-22 01:35:49

## Thread

**1/**

Working through rough draft of assembly for a different idea for a micro macro-forth.
1. 8-bit/word (color to relay meaning)
2. Roughly 62 useful dictionary entries/page
3. Supports paging (to extend dictionary)
4. Supports call/return - but compiler inlines everything
...

![](https://pbs.twimg.com/media/HNy5A_uW0AAj1cU?format=png&name=orig)

**2/**

5. Compile step is branch-free
6. Compiles to branch-free x86-64 source
7. Which is then executed

Noticed that I can pre-compile all the dictionary words into a lookup table. So actual compile just writes unaligned 8-bytes but only advances the write pointer by the actual size

**3/**

The interesting bits about this micro project was factoring out all branches, using branch-free interpreter loop to inline all calls so later execution is linear. Got messy doing a branch free software return stack. But costs are relatively low (40 ops/character)

**4/**

Intended usage would be for tiny-gramming programs in self contained chunks that include their own code generation (effectively a macro-forth used to generate machine code).

**5/**

A language that you author in a compressed space directly. So Whitney-esk in using lots of single character variables (or double character with page characters) -BUT- very non-Whitney in that it has no higher order array constructs
