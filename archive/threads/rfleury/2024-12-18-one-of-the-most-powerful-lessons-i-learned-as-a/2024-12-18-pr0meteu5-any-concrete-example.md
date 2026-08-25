---
title: "@rfleury any concrete example?"
type: archive
source: twitter
source_url: "https://x.com/pr0meteu5/status/1869438149832946012"
author: "pr0meteu5"
handle: pr0meteu5
post_id: "1869438149832946012"
date: 2024-12-18
archived: 2026-08-25
draft: false
tags:
  - archive
  - twitter
  - rfleury
description: "@rfleury any concrete example?"
in_reply_to: ""
parent_post_id: "1869409243251827152"
---

## Source

- URL: https://x.com/pr0meteu5/status/1869438149832946012
- Author: pr0meteu5 (@pr0meteu5)
- Posted: 2024-12-18 17:42:42

## Branch

**1/** @pr0meteu5

@rfleury

any concrete example?

**2/** @rfleury

@saddev24

- https://www.rfleury.com/p/ui-part-3-the-widget-building-language
- https://www.rfleury.com/p/emergence-and-composition
- https://www.rfleury.com/p/the-codepath-combinatoric-explosion

**3/** @LazarTo42297588

@rfleury @saddev24

Let's say you're creating a generic table component, with different types of table columns. How will you design the cell render function so it handles all the different types of data that can be displayed: image, url, list, object, button.

**4/** @rfleury

The first thing I’d say is that this is not an architecture I even agree with. Any helpers for constructing a table should build *just the table*, with all UI & rendering capabilities being written by the user.

For instance, in my codebase it’d look like:

UI_Table(…)
{
  UI_TableRow
  {
    UI_TableCell { … }
  }
}

In that table cell block, the usage code can simply build whatever they want. The table constructs are completely orthogonal.

But in any case, in any codepath which can conceptually accept 1 of N things, it can also be reframed to accept any combination of those N things. Instead of N possibilities, you get 2^N possibilities. So if the codepath took an image AND a URL, rather than an image OR a URL, and you build the codepath to handle all 4 cases (with the same amount as that which would handle the OR case), then you get new features for free (e.g. image AND URL, standalone image, standalone URL).

## Related

- Spine: [[archive/threads/rfleury/2024-12-18-one-of-the-most-powerful-lessons-i-learned-as-a]]
