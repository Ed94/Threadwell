---
title: "@rfleury A function explicitly limits the variables that its code depends on."
type: archive
source: twitter
source_url: "https://x.com/ndwork/status/2061896821023383829"
author: "Nicholas Dwork"
handle: ndwork
post_id: "2061896821023383829"
date: 2026-06-02
archived: 2026-08-25
draft: false
tags:
  - archive
  - twitter
  - rfleury
description: "@rfleury A function explicitly limits the variables that its code depends on."
in_reply_to: ""
parent_post_id: "2061619837877780961"
---

## Source

- URL: https://x.com/ndwork/status/2061896821023383829
- Author: Nicholas Dwork (@ndwork)
- Posted: 2026-06-02 19:44:44

## Branch

**1/** @ndwork

@rfleury

A function explicitly limits the variables that its code depends on.

For many functions, they can be independently tested. When possible, that also seems useful. If there’s a bug, it’s highly likely not to be inside the function.

These things make functions extremely useful.

**2/** @rfleury

No. By adding entry points which are independently tested (e.g. in a vacuum, removed from context), you are combinatorially increasing the number of possible test cases. It’s vastly easier to exercise one single codepath than several thousands.

Second of all, sub-scopes also allow limiting exposed variables to other scopes. If a scope fairly far into a function depends on the entire set of exposed variables that came before, functions do not stop that, because you’d simply need to pass them all. There is way less boilerplate and way less complexity in the single codepath version.

**3/** @ndwork

@rfleury

I’m taking the fact that you didn’t tell me to delete my account as a huge mark of success.  :)

All the best Ryan.

## Related

- Spine: [[archive/threads/rfleury/2026-06-02-the-first-way-people-usually-learn-code]]
