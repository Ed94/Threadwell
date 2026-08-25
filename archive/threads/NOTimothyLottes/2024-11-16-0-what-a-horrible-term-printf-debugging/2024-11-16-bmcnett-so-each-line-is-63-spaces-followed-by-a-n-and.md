---
title: "@NOTimothyLottes So each line is 63 spaces followed by a \\n, and those 63 spaces get replaced by printable characters dynamically? I have long dreamed of a text format with a fixed 128 byte line width, and cache line size is gradually switching over from 64 to 128"
type: archive
source: twitter
source_url: "https://x.com/bmcnett/status/1857815519166112244"
author: "bmcnett"
handle: bmcnett
post_id: "1857815519166112244"
date: 2024-11-16
archived: 2026-08-25
draft: false
tags:
  - archive
  - twitter
  - NOTimothyLottes
description: "@NOTimothyLottes So each line is 63 spaces followed by a \\n, and those 63 spaces get replaced by printable characters dynamically? I have long dreamed of a text format with a fixed 128 byte line width, and cache line size is gradually switching over from 64 to 128"
in_reply_to: ""
parent_post_id: "1857813028349128825"
---

## Source

- URL: https://x.com/bmcnett/status/1857815519166112244
- Author: bmcnett (@bmcnett)
- Posted: 2024-11-16 15:58:30

## Branch

**1/** **@bmcnett** ^1857815519166112244

**@NOTimothyLottes**

So each line is 63 spaces followed by a \n, and those 63 spaces get replaced by printable characters dynamically? I have long dreamed of a text format with a fixed 128 byte line width, and cache line size is gradually switching over from 64 to 128

**2/** **@NOTimothyLottes** ^1857818622271332607

**@bmcnett**

Yes fixed character[63]='\n', string fills until then or spaces out. I did 128-char once, but still sometimes use small VGA resolutions. Also written a source editor a few times with this fixed line size, makes for a very simple implementation ...

**3/** **@bmcnett** ^1857819880600531261

**@NOTimothyLottes**

Variable line width ASCII text files made a lot of sense when storage was 100KB or 100MB or 100GB, but now that it's in the terabytes, why even bother

**4/** **@NOTimothyLottes** ^1857820858162753661

**@bmcnett**

That line of thinking is universal solution to most self-inflicted problems of the modern era.

## Related

- Spine: [[archive/threads/NOTimothyLottes/2024-11-16-0-what-a-horrible-term-printf-debugging]]
