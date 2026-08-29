---
title: "How does ASLR interact with PE relocations during Windows process startup? Suppose a DLL was linked with a preferred base address, but ASLR causes it to be mapped somewhere else."
type: archive
source: twitter
source_url: "https://x.com/OSdev_/status/2092211719628050708"
author: "OS Dev"
handle: OSdev_
post_id: "2092211719628050708"
date: 2026-08-25
archived: 2026-08-29
draft: false
tags:
  - archive
  - twitter
  - OSdev_
description: "How does ASLR interact with PE relocations during Windows process startup? Suppose a DLL was linked with a preferred base address, but ASLR causes it to be mapped somewhere else."
in_reply_to: ""
---

## Source

- URL: https://x.com/OSdev_/status/2092211719628050708
- Author: OS Dev (@OSdev_)
- Posted: 2026-08-25 11:25:20

## Thread

**1/** **@OSdev_** ^2092211719628050708

How does ASLR interact with PE relocations during Windows process startup? Suppose a DLL was linked with a preferred base address, but ASLR causes it to be mapped somewhere else. What exactly must the Windows loader change, and why? Also, what happens if the image has no relocation information?

**2/** **@HostOfMeta** ^2092224460384333945

I just realized this works like address fixups in loading certain data formats. But here instead of an engine knowing the file format and relying on content being baked for 32-bit or 64-bit, it uses the .reloc section to know every site in the binary where the base address gets used and inserts an offset, the delta between the original base address and the one being randomized.

When the .reloc is present, every use of the base address has a baked-in +0 offset in the binary, ready to be patched up. That leaves every relative addressing intact in the loaded binary. Only minimal work needed, the process just runs through a list of binary offsets and writes the base address delta there naively.

Without a .reloc, it works like loading an opaque blob of data: we can only guess, which is unsafe, load it as-is, or fail the load entirely. Similar to intermediate tools processing baked assets without touching their data. Or HTTP proxies leaving everything they don't know how to read as passthrough.

**3/** **@OSdev_** ^2092266048473166261

**@HostOfMeta**

Yep, that's basically right. ".reloc" gives the loader an explicit map of base-dependent sites to patch with the ASLR delta, while relative addressing stays intact. Without that metadata, the loader cannot safely know what should be treated as an address and modified.
