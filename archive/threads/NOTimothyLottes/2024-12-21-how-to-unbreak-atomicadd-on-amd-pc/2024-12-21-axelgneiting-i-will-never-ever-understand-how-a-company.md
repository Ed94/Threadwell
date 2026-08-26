---
title: "@NOTimothyLottes I will never ever understand how a company literally spends hundreds of millions on hardware R&D and tapeouts and then squanders half the performance with its absymal compiler."
type: archive
source: twitter
source_url: "https://x.com/axelgneiting/status/1870567002127179929"
author: "Axel Gneiting"
handle: axelgneiting
post_id: "1870567002127179929"
date: 2024-12-21
archived: 2026-08-26
draft: false
tags:
  - archive
  - twitter
  - NOTimothyLottes
description: "@NOTimothyLottes I will never ever understand how a company literally spends hundreds of millions on hardware R&D and tapeouts and then squanders half the performance with its absymal compiler."
in_reply_to: ""
parent_post_id: "1870329223455334599"
---

## Source

- URL: https://x.com/axelgneiting/status/1870567002127179929
- Author: Axel Gneiting (@axelgneiting)
- Posted: 2024-12-21 20:28:21

## Branch

**1/** **@axelgneiting** ^1870567002127179929

**@NOTimothyLottes**

I will never ever understand how a company literally spends hundreds of millions on hardware R&D and tapeouts and then squanders half the performance with its absymal compiler. This has been going on for at least a decade.

**2/** **@DaveAirlie** ^1870567643197149531

**@axelgneiting** **@NOTimothyLottes**

Even worse when another company writes a replacement compiler and they don't adopt it :-)

**3/** **@b_nieuwen** ^1870568658470355181

**@DaveAirlie** **@axelgneiting** **@NOTimothyLottes**

tbh this problem is also kinda messy. Like as a compiler introducing the subgroupElect on uniform addresses makes sense in general. Detecting all the myriad ways in which the app could be doing the same already is the hard part. I'm pretty sure we'd be missing some in ACO.

**4/** **@NOTimothyLottes** ^1870594133880103116

**@b_nieuwen** **@DaveAirlie** **@axelgneiting**

Having a "[preoptimized]" that one places in the source to disable these compiler workarounds for bad programmer behavior, that would be a good start.

**5/** **@olson_dan** ^1870719552247550362

**@axelgneiting** **@NOTimothyLottes**

I don't think this is the only case, either.

**6/** **@NOTimothyLottes** ^1870841084265496647

**@olson_dan** **@axelgneiting**

It isn't the worst compiler. They are just brave enough to have a public {disassembly extension and compiler+disassembly analysis tool}, paired with an audience who actually uses it.

## Related

- Spine: [[archive/threads/NOTimothyLottes/2024-12-21-how-to-unbreak-atomicadd-on-amd-pc]]
