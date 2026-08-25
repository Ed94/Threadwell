---
title: "SPC: RDNA2 ASSEMBLER [thread] ..."
type: archive
source: twitter
source_url: "https://x.com/NOTimothyLottes/status/1688275737692815360"
author: "NOTimothyLottes"
handle: NOTimothyLottes
post_id: "1688275737692815360"
date: 2023-08-06
archived: 2026-08-24
draft: false
tags:
  - archive
  - twitter
  - NOTimothyLottes
description: "SPC: RDNA2 ASSEMBLER [thread] ..."
in_reply_to: ""
---

## Source

- URL: https://x.com/NOTimothyLottes/status/1688275737692815360
- Author: NOTimothyLottes (@NOTimothyLottes)
- Posted: 2023-08-06 19:47:57

## Thread

**1/** **@NOTimothyLottes** ^1688275737692815360

SPC: RDNA2 ASSEMBLER [thread] ... Did initial design plan this weekend. The aim is a GPU-side assembler+editor, building RDNA2 binary images for Steam Deck. Live edit, live data view, etc. Assembler and editor running in massive vectorized shader code.

**2/** **@NOTimothyLottes** ^1688276271619248129

Good reason not to use text input for assembler, instead will use a custom binary format, and treat all 32-bit words in the binary the exact same way (so massively parallel assembly step). This is parallel design 101.

**3/** **@NOTimothyLottes** ^1688277538571755520

Some basics: RDNA2 instructions are 1-N 32-bit words. Each of the 32-bit components have a bunch of fields. Will typically need 1-6 fields per 32-bit word, as will be joining some fields into one argument (like DLC/GLC) below.

![](https://pbs.twimg.com/media/F232wWkX0AAZWPh?format=jpg&name=orig)
![](https://pbs.twimg.com/media/F233F_sWMAAqHBo?format=png&name=orig)

**4/** **@NOTimothyLottes** ^1688278083684421632

Could argue that MIMG has the most fields, but in practice many of those fields will be joined (see example), and I'm not likely to be using NSA encoding. So still will only need maximum 6 arguments to build a 32-bit value.

![](https://pbs.twimg.com/media/F233qJyWQAAjmOo?format=jpg&name=orig)
![](https://pbs.twimg.com/media/F2333WKXEAAc2fZ?format=png&name=orig)

**5/** **@NOTimothyLottes** ^1688278959711272960

Custom editor, using a custom font, designed for vintage CRTs. Wanted 5-character symbol names for easy packing in 30-bit values. So setup a 6-bit character table. This is using a modified 'right-angle-only' font (like the one below). So some glyphs alias, and only upper case.

![](https://pbs.twimg.com/media/F234Y1IXcAECWTB?format=png&name=orig)

**6/** **@NOTimothyLottes** ^1688280670764756992

Will need some kind of symbol table, what ends up providing the arguments to the rules that build the 32-bit words that comprise the final binary. The symbol indirection provides a way to name registers for example, and then change the register mapping later.

![](https://pbs.twimg.com/media/F2357mwXUAAC6O6?format=png&name=orig)

**7/** **@NOTimothyLottes** ^1688281231954161664

Notice SMEM ops have 21-bit immediate offsets. I'll use 20-bits of that for an absolute positive offset from KART base. 1 MiB of easy data. The editor will relink tagged symbols that represent offsets automatically.

![](https://pbs.twimg.com/media/F236eA_XkAAc8-_?format=jpg&name=orig)

**8/** **@NOTimothyLottes** ^1688281975210041344

Next will need a collection of rules, how to join the 6 possible symbol arguments together. Rules for example for each of the RDNA2 instruction encodings (VOPC, etc). This reduces to just a 6 entry 5-bit left shift amount associated with each argument.

![](https://pbs.twimg.com/media/F237AEiWgAAkzD0?format=png&name=orig)

**9/** **@NOTimothyLottes** ^1688282613914492928

But will need a 7th argument, hard coded to a signed 16-bit *4 relative offset as this is how RDNA2 does all it's relative branches. This will be setup inside the editor to auto relink as source is edited.

![](https://pbs.twimg.com/media/F237uqaXAAAKAFl?format=jpg&name=orig)

**10/** **@NOTimothyLottes** ^1688283094049021952

Source then is simple, two 128-bit values per 32-bit word in the binary. One to select {RULE, SYMBOLS, RELATIVE BRANCH}, and another for {LABEL, COMMENT}.

![](https://pbs.twimg.com/media/F238Q-zXYAAO1Eo?format=png&name=orig)

**11/** **@NOTimothyLottes** ^1688284090129084417

And then the source editor, shows a line per 32-bit value (so VOP3's for example would take 2 lines). So the 'assembler' is deceptively simple, but powerful enough to do everything required to generate GPU binary code. And all the opcode generation is in the data itself :)

![](https://pbs.twimg.com/media/F238wJ8WoAAtEfw?format=png&name=orig)

**12/** **@NOTimothyLottes** ^1688284962288537600

The editor itself will have 3 views {symbol table, rule table, source table}. The editor itself will use 2 copies of everything, so each edit, it's one entry/lane, reading prior state and updating to the new. Dead simple, dead parallel (not necessarily efficient) :)

**13/** **@NOTimothyLottes** ^1688286623375454208

Yeah, perhaps wildly alien. But for those who grew up with MOD-like trackers (like Impulse Tracker below), the interface will almost feel like home (those had simple {instrument, pattern, arangement} editors, with a very spreadsheet feel).

![](https://pbs.twimg.com/media/F23_OOhXgAUBtlb?format=png&name=orig)
