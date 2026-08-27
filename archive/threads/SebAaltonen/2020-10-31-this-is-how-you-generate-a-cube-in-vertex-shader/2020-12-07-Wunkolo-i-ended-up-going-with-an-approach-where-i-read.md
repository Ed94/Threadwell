---
title: "@SebAaltonen I ended up going with an approach where I read the \"chunk data\" and then emit to an indice+mesh buffer and write the indirect dispatch from a compute shader."
type: archive
source: twitter
source_url: "https://x.com/Wunkolo/status/1336028429997678592"
author: "wunk"
handle: Wunkolo
post_id: "1336028429997678592"
date: 2020-12-07
archived: 2026-08-27
draft: false
tags:
  - archive
  - twitter
  - SebAaltonen
description: "@SebAaltonen I ended up going with an approach where I read the \"chunk data\" and then emit to an indice+mesh buffer and write the indirect dispatch from a compute shader."
in_reply_to: ""
parent_post_id: "1335872884464640000"
---

## Source

- URL: https://x.com/Wunkolo/status/1336028429997678592
- Author: wunk (@Wunkolo)
- Posted: 2020-12-07 19:22:54

## Branch

**1/** **@Wunkolo** ^1336028429997678592

**@SebAaltonen**

I ended up going with an approach where I read the "chunk data" and then emit to an indice+mesh buffer and write the indirect dispatch from a compute shader.
Seems to run pretty fast for having varying per-face or per-vertex attributes(lighting/normals)
https://x.com/Wunkolo/status/1309657816269901825

## Related

- Spine: [[archive/threads/SebAaltonen/2020-10-31-this-is-how-you-generate-a-cube-in-vertex-shader]]
