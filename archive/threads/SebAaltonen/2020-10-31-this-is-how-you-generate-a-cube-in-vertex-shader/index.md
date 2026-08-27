---
title: "This is how you generate a cube in vertex shader."
type: archive
source: twitter
source_url: "https://x.com/SebAaltonen/status/1322594445548802050"
author: "Sebastian Aaltonen"
handle: SebAaltonen
post_id: "1322594445548802050"
date: 2020-10-31
archived: 2026-08-27
draft: false
tags:
  - archive
  - twitter
  - SebAaltonen
description: "This is how you generate a cube in vertex shader."
in_reply_to: ""
---

## Source

- URL: https://x.com/SebAaltonen/status/1322594445548802050
- Author: Sebastian Aaltonen (@SebAaltonen)
- Posted: 2020-10-31 17:41:03

## Thread

**1/** **@SebAaltonen** ^1322594445548802050

This is how you generate a cube in vertex shader. Works with any amount of cubes. Also includes the backface culling trick (only include the positive cube faces to index buffer). 

Backface culling trick relies on the fact that only 3 faces of a cube can be visible at once.

![](https://pbs.twimg.com/media/ElrMOuxXIAMu09A?format=jpg&name=orig)

**2/** **@SebAaltonen** ^1322594883757027329

Measured performance advantage of the backface culling trick. On Intel Gen 11 GPU. 1 million untextured cubes.

6 face cube = 16.1 ms
3 face cube (mirror faces at runtime) = 10.5 ms

53% performance increase!

**3/** **@SebAaltonen** ^1322595624714407942

If you use the mirroring trick, you need to disable the backface culling from the rasterizer state. Mirroring also flips the faces (except when mirrored even times as that brings the determinant back to positive).

**4/** **@SebAaltonen** ^1322599526318964736

Shader Playground link to my vertex shader:

http://shader-playground.timjones.io/efcd86ce6a954d91ac0a4355f38bb7d4

**5/** **@SebAaltonen** ^1322599989336514561

The cost of the backface mirroring:
9 full rate instructions in the box vertex shader.

I think I can optimize this further if needed. Let's try...

![](https://pbs.twimg.com/media/ElrRUwzX0AEbs_1?format=png&name=orig)

**6/** **@SebAaltonen** ^1322605838624792576

If you are scared that the compiler can't get rid of the branches. Try this. On AMD compiler it results in 1 full rate ALU more than the trivial implementation. On Intel Gen 11 the frame time is identical with 1M cubes. So yeah.

![](https://pbs.twimg.com/media/ElrWr01WoAEzOxF?format=png&name=orig)

**7/** **@SebAaltonen** ^1322819025047605248

For completeness: This is the index buffer I use. Repeat the same 3 or 6 faces for max cubes supported (add 8 for each iteration).

Full index buffer generation code also included...

![](https://pbs.twimg.com/media/EluYJ2SXUAAjwOb?format=png&name=orig)
![](https://pbs.twimg.com/media/EluY0_LW0AENiLp?format=jpg&name=orig)

**8/** **@SebAaltonen** ^1322821076448124928

ARM Mali compiler results: 11.5 ALU cycles. 12 L/S cycles. Thus ALU is free. Without backface culling trick, it's 10.5 ALU cycles. Insignificant difference.

http://shader-playground.timjones.io/2b3fd2d6a2e6f6bd1100283fbe956677

![](https://pbs.twimg.com/media/EluaZUTX0AY0IK6?format=png&name=orig)

**9/** **@SebAaltonen** ^1322822548137062400

Image of the cube is here. The Y and Z arrows should actually point to the other direction. Oops :)

https://x.com/SebAaltonen/status/1315982782439591938?s=20

**10/** **@SebAaltonen** ^1335872884464640000

If you are using this cube rendering trick to render actual concrete cube faces (with normals), you need to use SV_IsFrontFace input in pixel shader to detect whether a backface is rendered and flip the normal.

Branches: [[archive/threads/SebAaltonen/2020-10-31-this-is-how-you-generate-a-cube-in-vertex-shader/2020-12-07-Wunkolo-i-ended-up-going-with-an-approach-where-i-read]]
