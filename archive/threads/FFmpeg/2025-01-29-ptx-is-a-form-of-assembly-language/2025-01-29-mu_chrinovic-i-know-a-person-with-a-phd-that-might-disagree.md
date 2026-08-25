---
title: "@FFmpeg I know a person with a PhD that might disagree with you"
type: archive
source: twitter
source_url: "https://x.com/mu_chrinovic/status/1884733082474775028"
author: "Chrinovic Mukanya"
handle: mu_chrinovic
post_id: "1884733082474775028"
date: 2025-01-29
archived: 2026-08-25
draft: false
tags:
  - archive
  - twitter
  - FFmpeg
description: "@FFmpeg I know a person with a PhD that might disagree with you"
in_reply_to: ""
parent_post_id: "1884730404587909544"
---

## Source

- URL: https://x.com/mu_chrinovic/status/1884733082474775028
- Author: Chrinovic Mukanya (@mu_chrinovic)
- Posted: 2025-01-29 22:39:18

## Branch

**1/**

@FFmpeg I know a person with a PhD that might disagree with you

**2/**

@mu_chrinovic @FFmpeg Yeah PTX is not assembly, it's a mid level language that is closer to a 1:1 match for the HW ISA --- BUT --- the actual register allocation and management is still done by a high-level compiler ...

**3/**

@NOTimothyLottes @mu_chrinovic @FFmpeg That's almost semantics at this point though? If you're writing x86 assembly it gets translated to microcode in the CPU as well, and will do register remapping etc. Only difference in Nvidia case that's happening in the driver, right?

**4/**

@janekm @mu_chrinovic @FFmpeg Sounds like you are trying to claim software compiler register allocation is the same as HW runtime register renaming? No. CPU register renaming maps a small set of registers to a larger set to get IPC. Compiler GPU reg allocation maps a massive SSA mess to a small set.

**5/**

@NOTimothyLottes @mu_chrinovic @FFmpeg Fair point, my argument was merely that both cases of assembly language are really an intermediate language that gets translated to the final instructions executed by the CPU/GPU. Feels quite pedantic to claim that PTX assembly is not assembly, merely because of reg allocation 🤷‍♂️

**6/**

@janekm @mu_chrinovic @FFmpeg SOFTWARE
Assembler = human writes the physical HW instructions
Compiler = program figures out the instructions from some other form
----DIFFERENT-THINGS----
HW
Instruction-reordering / wave-scheduling
Register renaming

**7/**

@NOTimothyLottes @mu_chrinovic @FFmpeg We've been calling it Assembly since at least when JVM byte code was first a thing. Doesn't matter that a JIT compiler will still do register allocation.

**8/**

@janekm @mu_chrinovic @FFmpeg Sure people have been incorrectly labeling stuff for a long time

## Related

- Spine: [[archive/threads/FFmpeg/2025-01-29-ptx-is-a-form-of-assembly-language]]
