---
title: "@nicbarkeragain this particular case though is easily solved with `defer` or even `closures`"
type: archive
source: twitter
source_url: "https://x.com/hasen_95dx/status/2084868526515634252"
author: "ハセン حسن"
handle: hasen_95dx
post_id: "2084868526515634252"
date: 2026-08-05
archived: 2026-08-25
draft: false
tags:
  - archive
  - twitter
  - nicbarkeragain
description: "@nicbarkeragain this particular case though is easily solved with `defer` or even `closures`"
in_reply_to: ""
parent_post_id: "2084851804224004329"
---

## Source

- URL: https://x.com/hasen_95dx/status/2084868526515634252
- Author: ハセン حسن (@hasen_95dx)
- Posted: 2026-08-05 05:06:06

## Branch

**1/** **@hasen_95dx** ^2084868526515634252

**@nicbarkeragain**

this particular case though is easily solved with `defer` or even `closures`

    Container(...., func() {
        // container is closed when this func exits
    })

**2/** **@nicbarkeragain** ^2084876136631419246

**@hasen_95dx**

Yes, I tend to use the "single iteration for loop" macro trick in C to do this exact thing with scope, but there are still a bunch of cases where you might want to have a direct API that you can use to call open / close:

![](https://pbs.twimg.com/media/HO73smTacAAYau2?format=jpg&name=orig)

**3/** **@nicbarkeragain** ^2084876247570813090

**@hasen_95dx**

I've also found explicit open / close to be very useful in rendering tree views / arbitrary recursive hierarchy etc.

**4/** **@hasen_95dx** ^2084883855505604792

**@nicbarkeragain**

Right. With the closure approach it would have to change.

body := func() { ... }

if condition { Container(...., body) }
else { body() }

## Related

- Spine: [[archive/threads/nicbarkeragain/2026-08-05-an-example-of-this-a-classic-way-to-construct-a]]
