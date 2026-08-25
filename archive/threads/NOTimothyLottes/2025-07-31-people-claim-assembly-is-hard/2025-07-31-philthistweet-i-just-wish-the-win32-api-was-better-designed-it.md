---
title: "@NOTimothyLottes I just wish the win32 API was better designed."
type: archive
source: twitter
source_url: "https://x.com/philthistweet/status/1950918943834620235"
author: "phil bohun"
handle: philthistweet
post_id: "1950918943834620235"
date: 2025-07-31
archived: 2026-08-25
draft: false
tags:
  - archive
  - twitter
  - NOTimothyLottes
description: "@NOTimothyLottes I just wish the win32 API was better designed."
in_reply_to: ""
parent_post_id: "1950866703342088407"
---

## Source

- URL: https://x.com/philthistweet/status/1950918943834620235
- Author: phil bohun (@philthistweet)
- Posted: 2025-07-31 13:58:17

## Branch

**1/** **@philthistweet** ^1950918943834620235

**@NOTimothyLottes**

I just wish the win32 API was better designed. It would essentially be perfect for cross dev then.

**2/** **@NOTimothyLottes** ^1950927467645894968

**@philthistweet**

Certainly it could be, but as is, it's easy to use and not strictly limiting. Id be curious what people don't like about it. Maybe the winproc interface?

**3/** **@philthistweet** ^1950932301187346833

Just a few examples:
1) thread/process creation and management 
2) file system interface (e.g. listing files in a directory)
3) interprocess communication 

I know you can wrap these in your own library, but I'd end up wrapping almost the entire win32. 

Whoever sat down to create it probably said: "How can I create the most annoying, unintuitive API possible?"

Honestly, I may start a wrapper project though, because it's the only stable API that works

**4/** **@NOTimothyLottes** ^1950933470802215318

**@philthistweet**

Clone is nicer and having ability to own cores should be great. But at least you get affinity and schedule priority. Yeah agree the file interface is poor, but I just memmap and manually page warm to bypass most of that.

## Related

- Spine: [[archive/threads/NOTimothyLottes/2025-07-31-people-claim-assembly-is-hard]]
