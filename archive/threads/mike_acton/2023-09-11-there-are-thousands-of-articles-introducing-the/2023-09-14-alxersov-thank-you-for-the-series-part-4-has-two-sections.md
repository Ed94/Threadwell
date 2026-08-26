---
title: "@mike_acton Thank you for the series."
type: archive
source: twitter
source_url: "https://x.com/alxersov/status/1702411411740061997"
author: "Alexei Ersov"
handle: alxersov
post_id: "1702411411740061997"
date: 2023-09-14
archived: 2026-08-25
draft: false
tags:
  - archive
  - twitter
  - mike_acton
description: "@mike_acton Thank you for the series."
in_reply_to: ""
parent_post_id: "1701337922157596901"
---

## Source

- URL: https://x.com/alxersov/status/1702411411740061997
- Author: Alexei Ersov (@alxersov)
- Posted: 2023-09-14 19:58:04

## Branch

**1/** **@alxersov** ^1702411411740061997

**@mike_acton**

Thank you for the series. Part 4 has two sections with the same header: “Lossless compression”. The first sentence in Take-away seems to have a typo: “a form a compression” probably should be “a form of compression”.

**2/** **@mike_acton** ^1702412517019197919

**@alxersov**

Thanks! fixed.

**3/** **@alxersov** ^1702783283396751781

**@mike_acton**

The compression routine in Part 5 produces strange results. If I compress 0.00015259 by running compress(0x5), I get 0:00010:0000000001, I expect to get 0:00010:0100000000. At the same time if I compress 2.00781250 and run compress(0x10100), I get 0:10000:0000000100 as expected.

**4/** **@mike_acton** ^1702805908940820618

**@alxersov**

Ok. I fixed up the pattern and added a note that hopefully clarifies.

**5/** **@alxersov** ^1702849157654868304

**@mike_acton**

I am sorry Mike, I am still confused 🙂 After compressing 0.00015259 I get 0:00010:0000000001 (0x0801). It is one of the samples, but it has value 0.000122 in the table. By IEEE 754 0x0801 decodes as 0.000122

https://float.exposed/0x0801

**6/** **@mike_acton** ^1702898141983555823

**@alxersov**

I think you're saying the approx. values aren't matching what's in the table there when printing as decimal. Ok, I changed that table now to match. The larger table below that already matched.

Appreciate you pointing out any confusing things or errors. Happy to fix.

**7/** **@alxersov** ^1702981784768503967

**@mike_acton**

Because 'compress' aligns bits to the right and IEEE 754 - to the left, there is a discrepancy in the binary outcomes for smaller values. It appears that the 'compress' results are being interpreted as IEEE 754, resulting in a slight inaccuracy in smaller numbers.

![](https://pbs.twimg.com/media/F6I058hWAAAYZLF?format=jpg&name=orig)

**8/** **@mike_acton** ^1703164787792945535

**@alxersov**

Not so much inaccurate as differently compressed, but that might be a confusing distinction for the article. It’s tough to display an approximate real without having introduced the details on how to convert to decimal format yet. Maybe I should add that here to reduce confusion?

## Related

- Spine: [[archive/threads/mike_acton/2023-09-11-there-are-thousands-of-articles-introducing-the]]
