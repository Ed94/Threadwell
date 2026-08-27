---
title: "Why do we spend so much effort to encode programming language semantics into a textual form just so a parser can go through the error-prone process of ripping that same exact information back out? Why not work directly on a program's abstract-syntax tree? (1/8)"
type: archive
source: twitter
source_url: "https://x.com/rfleury/status/1166970972882128896"
author: "Ryan Fleury"
handle: rfleury
post_id: "1166970972882128896"
date: 2019-08-29
archived: 2026-08-26
draft: false
tags:
  - archive
  - twitter
  - rfleury
description: "Why do we spend so much effort to encode programming language semantics into a textual form just so a parser can go through the error-prone process of ripping that same exact information back out? Why not work directly on a program's abstract-syntax tree? (1/8)"
in_reply_to: ""
---

## Source

- URL: https://x.com/rfleury/status/1166970972882128896
- Author: Ryan Fleury (@rfleury)
- Posted: 2019-08-29 07:08:55

## Thread

**1/** **@rfleury** ^1166970972882128896

Why do we spend so much effort to encode programming language semantics into a textual form just so a parser can go through the error-prone process of ripping that same exact information back out? Why not work directly on a program's abstract-syntax tree? (1/8)

**2/** **@rfleury** ^1166970974463377408

This would speed up builds and tools by preventing a parsing step entirely. It would also allow tools to more easily work within the semantics of the language, both because of the lack of a parsing requirement, and also because of the form of the modifications. (2/8)

**3/** **@rfleury** ^1166970975834927104

You wouldn't need to use strings to reference other pieces of the code, you could just *actually* reference them. Say goodbye to needing to fix up identifier usage sites when you change something, or having to ever care about a symbol table when writing a code tool. (3/8)

**4/** **@rfleury** ^1166970977470705665

This also has the property of decoupling code representation from code semantics. Zooming out in an editor could produce dynamic code LODs. Visualization of parallelized code becomes as easy as visually seeing two execution streams down two execution paths. (4/8)

**5/** **@rfleury** ^1166970978670301184

A debugger could visually show a piece of code writing into visually-represented memory. The memory could also be represented in different forms. Why not hit a button and have it visualized as 3D geometry, or a texture? Writing the wrong result would instantly be knowable. (5/8)

**6/** **@rfleury** ^1166970979861422082

Instead, right now, we're stuck looking at static text that: Constantly breaks and does not reflect a valid program without constant modification and maintenance, fundamentally couples representation with semantics, and innately prevents better tooling from easily existing. (6/8)

**7/** **@rfleury** ^1166970981006508032

Can you imagine if "find the definition for this type" in a large codebase didn't take *in the order of seconds* to complete, because your editor wouldn't need to search for it? Or, maybe you want to search for every function in the program *without* waiting 10 seconds. (7/8)

**8/** **@rfleury** ^1166970982155767808

I argue that this is the natural next step in computing. Artists do not manually write down a set of pixels, vertex data, or musical notes to get the results that they want, as we've decided there can be better tools for that. Why do we think that's untrue for programming? (8/8)

Branches: [[archive/threads/rfleury/2019-08-29-why-do-we-spend-so-much-effort-to-encode/2019-08-29-William_Bundy-for-a-moment-i-thought-you-were-revealing-your]], [[archive/threads/rfleury/2019-08-29-why-do-we-spend-so-much-effort-to-encode/2019-08-31-hmn_riscy-many-people-seem-skeptical-of-this-idea-with]]
