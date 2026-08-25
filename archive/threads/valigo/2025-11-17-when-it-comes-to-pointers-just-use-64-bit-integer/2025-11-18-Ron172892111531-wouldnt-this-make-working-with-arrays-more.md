---
title: "@valigo Wouldn't this make working with arrays more difficult? Array[1] would have to be Array[sizeof(data)] etc"
type: archive
source: twitter
source_url: "https://x.com/Ron172892111531/status/1990816225815875661"
author: "maple zero-op"
handle: Ron172892111531
post_id: "1990816225815875661"
date: 2025-11-18
archived: 2026-08-25
draft: false
tags:
  - archive
  - twitter
  - valigo
description: "@valigo Wouldn't this make working with arrays more difficult? Array[1] would have to be Array[sizeof(data)] etc"
in_reply_to: ""
parent_post_id: "1990506460531601538"
---

## Source

- URL: https://x.com/Ron172892111531/status/1990816225815875661
- Author: maple zero-op (@Ron172892111531)
- Posted: 2025-11-18 16:15:50

## Branch

**1/** @Ron172892111531

@valigo Wouldn't this make working with arrays more difficult? Array[1] would have to be Array[sizeof(data)] etc

**2/** @valigo

@Ron172892111531 As I said somewhere else, it makes sense sizeof pointer math to be the default. I was just saying that it's confusing because "+1" is not actually "plus one"

**3/** @Ron172892111531

@valigo Ptr+1. It's not plus one byte (or int addition), it's plus one object. I think it's only confusing when people assume pointers are just fancy integers. They're meant to work with arrays, and they do flawlessly as long as one remembers that they are an extension of the array

## Related

- Spine: [[archive/threads/valigo/2025-11-17-when-it-comes-to-pointers-just-use-64-bit-integer]]
