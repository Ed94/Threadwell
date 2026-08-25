---
title: "Hopefully with this last atomic workaround I'm almost done with cleaning and fixing the 'bind-everything-once' style Vulkan engine design."
type: archive
source: twitter
source_url: "https://x.com/NOTimothyLottes/status/1870342724538204320"
author: "NOTimothyLottes"
handle: NOTimothyLottes
post_id: "1870342724538204320"
date: 2024-12-21
archived: 2026-08-24
draft: false
tags:
  - archive
  - twitter
  - NOTimothyLottes
description: "Hopefully with this last atomic workaround I'm almost done with cleaning and fixing the 'bind-everything-once' style Vulkan engine design."
in_reply_to: ""
---

## Source

- URL: https://x.com/NOTimothyLottes/status/1870342724538204320
- Author: NOTimothyLottes (@NOTimothyLottes)
- Posted: 2024-12-21 05:37:09

## Thread

**1/**

Hopefully with this last atomic workaround I'm almost done with cleaning and fixing the 'bind-everything-once' style Vulkan engine design. Work in progress in the images that follow. Setting up the macros to get all the format aliasing is well quite ugly.

![](https://pbs.twimg.com/media/GfTKfZpWMAAifu3?format=png&name=orig)

**2/**

I end up doing a lot of duplication via macros since memory qualifiers are on the layout aliasing (instead of an argument to the operation like they should be) ...

**3/**

Vulkan is missing the streaming qualifiers, but I write the code like they exist for future compat
W ... writeonly coherent (all writes)
R ... readonly (all reads)
A ... coherent (atomics)
E ... streaming readonly (aka [E]xclusive)
F ... streaming writeonly (aka [F]inal)

**4/**



![](https://pbs.twimg.com/media/GfTMGj2WcAAoneG?format=png&name=orig)

**5/**

Texture layout aliasing is well the easy stuff since it's just readonly effectively

![](https://pbs.twimg.com/media/GfTMbIVXEAAqSaA?format=png&name=orig)

**6/**

STORAGE_TEXEL_BUFFER is well complex for aliasing and how to best use. Here is what I'm doing for setup (macro heavy). I have a define for each format descriptor index if I want to reorder them by usage for better cache layout. I only keep 32/64/128 bit types

![](https://pbs.twimg.com/media/GfTM36hXwAANxQl?format=png&name=orig)

**7/**

I didn't put in support for 16-bit <U,S>NORM yet because  it tends not to get used (bad match for FP16). Likewise no buffer access to 9E5 or sRGB due to HW portability support issues

**8/**

So todays HW
(1.) At least for AMD buffer atomics get the signage from the OPCODE so in theory one can use a UINT32 typed TEXEL buffer with both aliased as r32ui and r32i

![](https://pbs.twimg.com/media/GfTOBhyWEAAmNzY?format=png&name=orig)

**9/**

(2.) No buffer compression HW, so unlike images, there is no point in using separate types if the layout aliasing trick works. One could get by with just 32/64/128 bit type descriptors and extra ones for anything with format conversion

**10/**

(3.) In cases like <FP16,UINT16>x<2,4> actually probably better to alias those at UINTx<1,2> because then one is sure the compiler doesn't screw up the implicit NOPing of the undo the the format conversion!

**11/**

(4.) There is a strong desire to keep the number of descriptors down to avoid extra work in SMEM ops and extra SGPR pressure. So that also favors aliasing.

**12/**

(5.) Ideally I'd want TBUFFER support with the HW grabbing the index width from the type in the opcode instead of the descriptor (but I don't think the HW does that, so probably would always need 3 descriptors minimum).

**13/**

(6.) The future? Image compression relies on having the right type info in the descriptor to choose the right compression mode for decorrelation of the data. What happens if GPUs get buffer compression some day and everyone is just type aliasing all the time like SSBOs do?

**14/**

(7.) What is the "right answer"? Even signed vs unsigned could be important for data decorrelation. Certainly float vs int is. But no one wants to burn perf today based on a guess of what is needed in an unknown future.

**15/**

(8.) So my compromise is to have all the types, but write the code to use type aliasing (the fast path on todays HW) when I don't think data compression would help. And only use the right type (slower) if there is a prediction it might help some day if buffer compression shows up

**16/**

(9.) In cases where I need compression today, then I use explicit 2D images (assuming 1D images don't get compression on some HWs). But note this is not great, because often I need that data back in SGPRs (expensive, SMEM doesn't to image loads)

**17/**

Combining the STORAGE_TEXEL_BUFFER tricks (for something a good compiler could optimize from last week or so), I'm down to a few hundred macros for STB access. Showing a few here. It's ugly but the only way to actually implement well.

![](https://pbs.twimg.com/media/GfTSkwZWIAAgV-q?format=png&name=orig)

**18/**

Not sure if this is the end of this story yet, but hopefully the holidays I get this back online and can get back to using it. Probably have it down to as optimal as it can get while being as portable and future looking as possible
