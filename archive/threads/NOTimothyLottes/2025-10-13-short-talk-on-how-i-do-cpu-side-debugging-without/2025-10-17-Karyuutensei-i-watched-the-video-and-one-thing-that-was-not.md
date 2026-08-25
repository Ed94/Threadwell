---
title: "@NOTimothyLottes I watched the video and one thing that was not clear to me is why is half of the file wasted."
type: archive
source: twitter
source_url: "https://x.com/Karyuutensei/status/1979085608040489019"
author: "Nick Tasios"
handle: Karyuutensei
post_id: "1979085608040489019"
date: 2025-10-17
archived: 2026-08-25
draft: false
tags:
  - archive
  - twitter
  - NOTimothyLottes
description: "@NOTimothyLottes I watched the video and one thing that was not clear to me is why is half of the file wasted."
in_reply_to: ""
parent_post_id: "1977570893309321268"
---

## Source

- URL: https://x.com/Karyuutensei/status/1979085608040489019
- Author: Nick Tasios (@Karyuutensei)
- Posted: 2025-10-17 07:22:33

## Branch

**1/** **@Karyuutensei** ^1979085608040489019

**@NOTimothyLottes**

I watched the video and one thing that was not clear to me is why is half of the file wasted. Aren’t you using all upper 16 bits of the counter for the lines? Also, what do you mean with “no retries”?

**2/** **@NOTimothyLottes** ^1979208516733698451

**@Karyuutensei**

Could have just used pow2 pages + 1 page for counter, but I got lazy. Yes could use more than 16-bits for line counter too. Reload counter could be 4-bits. Lock-free typically implies a retry-loop (non-wait-free). This however is wait-free (no retry-loop).

## Related

- Spine: [[archive/threads/NOTimothyLottes/2025-10-13-short-talk-on-how-i-do-cpu-side-debugging-without]]
