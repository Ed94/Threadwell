---
title: "I share the same unconventional # define type conventions in C and GLSL, decoder:"
type: archive
source: twitter
source_url: "https://x.com/NOTimothyLottes/status/1737493375392137233"
author: "NOTimothyLottes"
handle: NOTimothyLottes
post_id: "1737493375392137233"
date: 2023-12-20
archived: 2026-08-26
draft: false
tags:
  - archive
  - twitter
  - NOTimothyLottes
description: "I share the same unconventional # define type conventions in C and GLSL, decoder:"
in_reply_to: ""
---

## Source

- URL: https://x.com/NOTimothyLottes/status/1737493375392137233
- Author: NOTimothyLottes (@NOTimothyLottes)
- Posted: 2023-12-20 15:21:16

## Thread

**1/** **@NOTimothyLottes** ^1737493375392137233

I share the same unconventional # define type conventions in C and GLSL, decoder:
{H=half,F=float,D=double}
{P=predicate (aka bool)}
{S=signed, else unsigned} for ints
{B=8bit(byte),W=16bit(word),I=32bit(int),L=64bit(long)}
then number of components {1,2,3,4}

![](https://pbs.twimg.com/media/GBzQ7G9WcAELFkg?format=png&name=orig)

Branches: [[archive/threads/NOTimothyLottes/2023-12-20-i-share-the-same-unconventional-define-type/2023-12-20-misyltoad-i-much-prefer-i32-f32-f16-u32-u8-etc-doesnt-need]]

**2/** **@NOTimothyLottes** ^1737494663009804674

Pointers in C are always either {R=restrict, or V=volatile} so I'm typically casting a raw 64-bit address after doing byte addressing: L1V_(base+bytes)[0] ... as is how it would be done naturally on the machine (and in asm).
The '<type>_(x)' macros do broadcast typecasting.

![](https://pbs.twimg.com/media/GBzRnugWsAAJGrf?format=png&name=orig)
![](https://pbs.twimg.com/media/GBzR6mjWkAEJnsu?format=png&name=orig)
![](https://pbs.twimg.com/media/GBzSI4VW4AABPDX?format=png&name=orig)

**3/** **@NOTimothyLottes** ^1737496597863243868

I've used variations of these kinds of conventions for many years. Found them useful at various works. For example FSR1/CAS's ffx_a.h https://github.com/GPUOpen-Effects/FidelityFX-FSR/blob/master/ffx-fsr/ffx_a.h
