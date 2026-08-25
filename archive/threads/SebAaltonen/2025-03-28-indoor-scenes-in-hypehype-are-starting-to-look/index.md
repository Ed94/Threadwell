---
title: "Indoor scenes in HypeHype are starting to look acceptable."
type: archive
source: twitter
source_url: "https://x.com/SebAaltonen/status/1905523331496828964"
author: "Sebastian Aaltonen"
handle: SebAaltonen
post_id: "1905523331496828964"
date: 2025-03-28
archived: 2026-08-25
draft: false
tags:
  - archive
  - twitter
  - SebAaltonen
description: "Indoor scenes in HypeHype are starting to look acceptable."
in_reply_to: ""
---

## Source

- URL: https://x.com/SebAaltonen/status/1905523331496828964
- Author: Sebastian Aaltonen (@SebAaltonen)
- Posted: 2025-03-28 07:32:19

## Thread

**1/** **@SebAaltonen** ^1905523331496828964

Indoor scenes in HypeHype are starting to look acceptable. This has no baked lighting. Only a single oct-map (conv.mips) for indirect specular and diffuse, masked with screen space AO (GTAO). No sunlight and no local lights (local lights are coming in a few months).

Game by Allu

<video controls src="https://video.twimg.com/ext_tw_video/1905521263075885056/pu/vid/avc1/720x1560/LEz0QMbFyKdz0Ph9.mp4?tag=12"></video>

Branches: [[archive/threads/SebAaltonen/2025-03-28-indoor-scenes-in-hypehype-are-starting-to-look/2025-03-28-VoxelBoy-any-tips-or-existing-solutions-on-achieving]]

**2/** **@SebAaltonen** ^1905523791322649077

We just shipped textures. This game is using older "pixart" assets only, which allows you to put diffuse-only textures in sprites. The ground and walls are 3d sprites in this game. The new material system allows full PBR texture sets (diffuse, normal, roughness, metallic, AO).

**3/** **@SebAaltonen** ^1905524218160132165

Local light system is shipping before summer. This will be a big improvement for indoor game visual quality. Direct lighting is important, especially when you can't bake lightmaps. Our local lights also have shadows. One big texture atlas caches all local light shadow maps.

**4/** **@SebAaltonen** ^1905524846559211822

Example of a game textured with the new PBR material system:
https://x.com/JohannesVuorine/status/1903305450969526504

Both games are running smoothly on dirt cheap <$99 phones with all the tech running.

Game by @DanielPalmiArt

**5/** **@SebAaltonen** ^1905527913341972664

**@DanielPalmiArt**

Old HypeHype indoor pictures before we landed screen space AO (GTAO) and oct-map indirect lighting. Old version had gradient based indirect lighting. Gradient is bad for indoors, since all wall normals face to horizon direction == same gradient color. And shadow masks sun out.

![](https://pbs.twimg.com/media/GnHLNt9WkAAabNR?format=jpg&name=orig)
![](https://pbs.twimg.com/media/GnHLO2zXEAAhygZ?format=jpg&name=orig)
![](https://pbs.twimg.com/media/GnHLQDVXEAAmBJ6?format=jpg&name=orig)

**6/** **@SebAaltonen** ^1905531104720724016

**@DanielPalmiArt**

Exactly one-year-old build versus the latest build. Quite a massive improvement in one year in visuals.

Still runs smoothly on the same devices.

Of course we are not happy with the current state either. It's going to look much better next year with all the new tech :)

![](https://pbs.twimg.com/media/GnHN9zuXgAAsS1Q?format=jpg&name=orig)
![](https://pbs.twimg.com/media/GnHOAL1WYAATQiF?format=jpg&name=orig)
