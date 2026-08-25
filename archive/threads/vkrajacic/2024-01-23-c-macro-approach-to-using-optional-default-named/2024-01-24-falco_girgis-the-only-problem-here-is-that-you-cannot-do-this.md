---
title: "The only problem here is that you cannot do this in a header file that is going to be included within a C++ source file..."
type: archive
source: twitter
source_url: "https://x.com/falco_girgis/status/1750088968681750741"
author: "Falco Girgis"
handle: falco_girgis
post_id: "1750088968681750741"
date: 2024-01-24
archived: 2026-08-25
draft: false
tags:
  - archive
  - twitter
  - vkrajacic
description: "The only problem here is that you cannot do this in a header file that is going to be included within a C++ source file..."
in_reply_to: ""
parent_post_id: "1749816169736073295"
---

## Source

- URL: https://x.com/falco_girgis/status/1750088968681750741
- Author: Falco Girgis (@falco_girgis)
- Posted: 2024-01-24 09:31:39

## Branch

**1/** **@falco_girgis** ^1750088968681750741

The only problem here is that you cannot do this in a header file that is going to be included within a C++ source file... However, what you can do is macro out the compound literal and provide a C++20 temporary object initializer with slightly different syntax if __cplusplus is defined..

**2/** **@vkrajacic** ^1750226315876122748

**@falco_girgis**

Yeah, I haven't tested that because my codebase is purely C nowadays.
I'm not concerned about compatibility with C++. I understand that this is not always a choice, especially when working with a codebase you didn't start.

**3/** **@falco_girgis** ^1750239118867546281

Tbh, I've never encountered a scenario with supporting C++ where you couldn't still pull all the tricks like this with modern C, if you are willing to invest in the infrastructure... That includes using _Generic() switches, which aren't supported in C++... I have a macro layer which you use to declare each type and its associated call which will compile to a _Generic statement in C or... a to C++20 anonymous generic lambda doing a series of compile-time conditionals on the generic type argument and mapping it to the appropriate logic based on its type... Yeah, it's a shitshow, but you write it once and it just works. lol. https://github.com/gyrovorbis/libgimbal/blob/79722a270d2a80651d08eb0158e803c9e4a2de6e/lib/api/gimbal/utils/gimbal_scanner.h#L366

## Related

- Spine: [[archive/threads/vkrajacic/2024-01-23-c-macro-approach-to-using-optional-default-named]]
