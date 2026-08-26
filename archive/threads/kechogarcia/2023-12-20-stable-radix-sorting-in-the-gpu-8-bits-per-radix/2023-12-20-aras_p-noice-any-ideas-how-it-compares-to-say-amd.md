---
title: "@kechogarcia Noice! Any ideas how it compares to say AMD FidelityFX radix sort? I have ported it to unity for gaussian splat needs (hlsl https://github.com/aras-p/UnityGaussianSplatting/blob/fded9c0/package/Shaders/GpuSortFidelityFX.hlsl and c# https://github.com/aras-p/UnityGaussianSplatting/blob/fded9c0/package/Runtime/GpuSorting.cs ) but I don't know if it's \"good\" compared to any other impls."
type: archive
source: twitter
source_url: "https://x.com/aras_p/status/1737463905922830691"
author: "Aras Pranckevičius 🇺🇦🇱🇹"
handle: aras_p
post_id: "1737463905922830691"
date: 2023-12-20
archived: 2026-08-26
draft: false
tags:
  - archive
  - twitter
  - kechogarcia
description: "@kechogarcia Noice! Any ideas how it compares to say AMD FidelityFX radix sort? I have ported it to unity for gaussian splat needs (hlsl https://github.com/aras-p/UnityGaussianSplatting/blob/fded9c0/package/Shaders/GpuSortFidelityFX.hlsl and c# https://github.com/aras-p/UnityGaussianSplatting/blob/fded9c0/package/Runtime/GpuSorting.cs ) but I don't know if it's \"good\" compared to any other impls."
in_reply_to: ""
parent_post_id: "1737288039603269648"
---

## Source

- URL: https://x.com/aras_p/status/1737463905922830691
- Author: Aras Pranckevičius 🇺🇦🇱🇹 (@aras_p)
- Posted: 2023-12-20 13:24:10

## Branch

**1/** **@aras_p** ^1737463905922830691

**@kechogarcia**

Noice! Any ideas how it compares to say AMD FidelityFX radix sort? I have ported it to unity for gaussian splat needs (hlsl https://github.com/aras-p/UnityGaussianSplatting/blob/fded9c0/package/Shaders/GpuSortFidelityFX.hlsl and c# https://github.com/aras-p/UnityGaussianSplatting/blob/fded9c0/package/Runtime/GpuSorting.cs ) but I don't know if it's "good" compared to any other impls.

**2/** **@kechogarcia** ^1737464880964206908

**@aras_p**

I haven't done a deep optimization yet. But I saw their code yesterday from your post, and from the looks is not stable, so likely theirs is faster because they use less LDS on Step 1 and give up on stableness.

## Related

- Spine: [[archive/threads/kechogarcia/2023-12-20-stable-radix-sorting-in-the-gpu-8-bits-per-radix]]
