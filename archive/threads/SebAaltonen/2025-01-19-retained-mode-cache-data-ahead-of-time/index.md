---
title: "Retained mode == cache data ahead of time."
type: archive
source: twitter
source_url: "https://x.com/SebAaltonen/status/1880888648377536631"
author: "Sebastian Aaltonen"
handle: SebAaltonen
post_id: "1880888648377536631"
date: 2025-01-19
archived: 2026-08-29
draft: false
tags:
  - archive
  - twitter
  - SebAaltonen
description: "Retained mode == cache data ahead of time."
in_reply_to: ""
---

## Source

- URL: https://x.com/SebAaltonen/status/1880888648377536631
- Author: Sebastian Aaltonen (@SebAaltonen)
- Posted: 2025-01-19 08:02:53

## Thread

**1/** **@SebAaltonen** ^1880888648377536631

Retained mode == cache data ahead of time. Delta update only the changed data.

It's good if the data update is slow. But it's often better just to optimize the data update to be fast instead of having complex caching. Vulkan PSOs and descriptor sets are "retained mode" too...

**2/** **@SebAaltonen** ^1880889196363251790

Vulkan and DX12 was initially slower in Unreal/Unity because their RHIs didn't match the retained mode grouping of Vulkan/DX12. Developers had to add hash maps under the RHI to map dynamic API to retained PSO and descriptor set APIs. Which added complexity and CPU cost a lot.

**3/** **@SebAaltonen** ^1880889514723524728

Persistence and caching are always a trade-off. If you require it, then the user has to manage the persistent data in some way. If their design is not 1:1 with your API design, then there will be hash maps and similar slow mapping data structures.

**4/** **@SebAaltonen** ^1880890128580948014

Also, if you need dynamic behavior, then Vulkan adds extra driver overhead to call various APIs to update the descriptors and especially recompile the PSOs.

I am talking about these issues in my forthcoming blog post. Higher performance obtained by persistent data is tricky.

**5/** **@SebAaltonen** ^1880891657622814740

Retained vs immediate mode always has these considerations. Both have advantages and disadvantages. Implementing retained mode as an optimization is tricky as it forces the user to deal with persistent data == caching. It's a win if data is mostly static, but a loss otherwise.

**6/** **@SebAaltonen** ^1880893631533600796

Another data point: GPU-driven rendering is retained mode. You have persistent scene data in GPU memory that you delta update from CPU. You need object persistence and change tracking. Well-optimized batched delta update is fast. But the whole system is quite complex.

**7/** **@AgileJebrim** ^1880983311746797576

**@SebAaltonen**

It’s not that complex nor are hash tables or descriptor changes needed. You divide your scene up into a large number of equally sized chunks of worst case size and can just leverage a pool for it. Stream in chunks on the leading edge to replace the chunks on the trailing edge.

**8/** **@AgileJebrim** ^1880983668979794003

**@SebAaltonen**

This approach enables a large open world. For dynamic entities that don’t remain in clear chunk borders and can wander globally, you have a separate global pool for such entities.

**9/** **@AgileJebrim** ^1880984066272690670

**@SebAaltonen**

This approach enables large open worlds to exist. I use it in pretty much every rendering project I do.

**10/** **@SebAaltonen** ^1881237090052317198

**@AgileJebrim**

Sure, it's not that complicated to keep data persistent in GPU memory. But it's more complicated than just bump allocating your draw data. No need for lifetime management. The biggest problem if you force everything to go through the persistent pipeline. That's what Vulkan does.

**11/** **@AgileJebrim** ^1881337796973285801

**@SebAaltonen**

Lifetime management isn’t that hard either. It’s a pool. If state is managed on the CPU side, it’s trivial to just spawn/kill only one fixed sized chunk per tick. Spawning is a single staging buffer and killing is just an identifier (pool index or some other group index).

**12/** **@AgileJebrim** ^1881338681056739657

Also constraining things to only one thing at a time has the benefit of not overloading the PCIs bus and causing a spike. Maintain a ring buffer queue on the CPU side as you feed it into the straw to stream these commands to the GPU. Not really that complicated.

If the spawn queue fills up, I just put the background thread to sleep until room is available. Nothing is getting in there any faster anyways so it doesn’t matter.

**13/** **@SebAaltonen** ^1881343516028371351

**@AgileJebrim**

Yes, it's definitely a benefit to keep the scene persistently in GPU memory. PCI-E traffic is definitely lower than pushing every visible draw call data there separately.

**14/** **@SebAaltonen** ^1881343848120832034

**@AgileJebrim**

But if you load big chunks of data, the PCI-E traffic can be higher on those frames compared to rendering a frame traditionally. You can throttle it, but that's more complexity. Also in UGC game, user could just make everything dynamic or something stupid like that :(

**15/** **@AgileJebrim** ^1881344233107583410

**@SebAaltonen**

Nope. As I said, it’s a FIXED-sized chunk. Everything has a defined cap. Even if they don’t utilize everything in said cap, you still stream the exact same size to the GPU every frame. Even if nothing is being spawned that tick, still send the same total number of bytes of nulls.

**16/** **@AgileJebrim** ^1881344631260184725

**@SebAaltonen**

The tools for UGC can simply restrict the amount of density that you allow in a given area. That’s my preference as it ensures a consistent rendering performance as well. However, many existing scenes were not created in that manner and I often have to adapt around that reality.

**17/** **@SebAaltonen** ^1881350092390887659

**@AgileJebrim**

Density limitation doesn't solve the case of lots of dynamic objects. People just spam 10,000 characters and make them all chase you :)

**18/** **@AgileJebrim** ^1881351201121595613

**@SebAaltonen**

If you want a large amount of dynamic entities that can go wherever they want in the scene, no chunk locking, then you just work with a large global pool.

**19/** **@AgileJebrim** ^1881353030899257808

**@SebAaltonen**

Honestly the biggest shock for me right now is that others in the industry seem to be unfamiliar with these techniques. Pretty much the only C++ code I’ve written over the past 2+ years has involved implementing generic systems for this strategy. Maybe I should write a blog?

**20/** **@SebAaltonen** ^1881353799929123123

**@AgileJebrim**

My team added GPU-resident scene data model to Unity. 4x perf increase in 2M object dense scene:
https://discussions.unity.com/t/gpu-driven-rendering-in-unity/930675

The title is misleading. It's not actually GPU-driven rendering. It has GPU-resident data structure.

**21/** **@Gadget_Games** ^1881561439217074582

**@SebAaltonen** **@AgileJebrim**

Your team made the GPU Resident Drawer? Thanks - it's one of the best new features Unity has shipped on the rendering side in a very long time. Stable, easy to use, well-integrated, instant benefits, etc.

**22/** **@SebAaltonen** ^1881612779112788435

**@Gadget_Games** **@AgileJebrim**

Yeah. It was based on my earlier experiment using our older BatchRendererGroup API. I tried how easy it would be to take all the MeshRenderers from the scene and render them using the BRG API. 

https://x.com/SebAaltonen/status/1407661348197175299

**23/** **@SebAaltonen** ^1881613327501242785

**@Gadget_Games** **@AgileJebrim**

This prototype spawned a full GPU-driven renderer prototype too, a bit similar to Nanite. But I left the company and many people from our team left too, so I don't know whether it will ship or not.
