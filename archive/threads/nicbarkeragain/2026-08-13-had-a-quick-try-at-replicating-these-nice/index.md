---
title: "Had a quick try at replicating these nice animations using clay's transition API, was a lot of fun and also helped me find a bug in the layout algo!"
type: archive
source: twitter
source_url: "https://x.com/nicbarkeragain/status/2087745896478101882"
author: "Nic Barker"
handle: nicbarkeragain
post_id: "2087745896478101882"
date: 2026-08-13
archived: 2026-11-16
draft: false
tags:
  - archive
  - twitter
  - nicbarkeragain
description: "Had a quick try at replicating these nice animations using clay's transition API, was a lot of fun and also helped me find a bug in the layout algo!"
in_reply_to: ""
---

## Source

- URL: https://x.com/nicbarkeragain/status/2087745896478101882
- Author: Nic Barker (@nicbarkeragain)
- Posted: 2026-08-13 03:39:44

## Thread

**1/** **@nicbarkeragain** ^2087745896478101882

Had a quick try at replicating these nice animations using clay's transition API, was a lot of fun and also helped me find a bug in the layout algo!

<video controls src="https://video.twimg.com/amplify_video/2087745685139619840/vid/avc1/2156x1656/od9SOrVKDzYhC0xc.mp4?tag=29"></video>

Branches: [[archive/threads/nicbarkeragain/2026-08-13-had-a-quick-try-at-replicating-these-nice/2026-08-13-reybuzzed-sir-is-this-an-update-like-how]], [[archive/threads/nicbarkeragain/2026-08-13-had-a-quick-try-at-replicating-these-nice/2026-08-13-always_maap-would-be-nice-to-share-the-example-code]], [[archive/threads/nicbarkeragain/2026-08-13-had-a-quick-try-at-replicating-these-nice/2026-08-13-NateHelmig-https-github-com-nhlmg93-term-if-you-want-to]], [[archive/threads/nicbarkeragain/2026-08-13-had-a-quick-try-at-replicating-these-nice/2026-08-14-rismanrp26-clay-browser-when]], [[archive/threads/nicbarkeragain/2026-08-13-had-a-quick-try-at-replicating-these-nice/2026-08-15-SwirlsDefy-is-clay-officially-unmaintained-now-i-see-there]]

**2/** **@nicbarkeragain** ^2087746762081817013

I find it very easy to think about animations using this type of mental model, you just mark the properties for transition, declare two different layouts on two consecutive frames (with matching IDs), and the internal machinery figures out the tweens for you.

![](https://pbs.twimg.com/media/HPkqb2oaMAAphIV?format=jpg&name=orig)

**3/** **@nicbarkeragain** ^2087747024309604730

The above is about 175 lines of C btw, with 80% of that just being properties in the UI element config structs. Almost zero logic.

Branches: [[archive/threads/nicbarkeragain/2026-08-13-had-a-quick-try-at-replicating-these-nice/2026-08-13-coodeneko-this-in-the-clay-library-ive-been-thinking-about]], [[archive/threads/nicbarkeragain/2026-08-13-had-a-quick-try-at-replicating-these-nice/2026-08-13-borrowck_novel-would-it-be-possible-to-create-a-small-public]]
