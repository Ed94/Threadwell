---
title: "Shading language standardization for the web is completely f'ed."
type: archive
source: twitter
source_url: "https://x.com/cmuratori/status/1473406996577615874"
author: "Casey Muratori"
handle: cmuratori
post_id: "1473406996577615874"
date: 2021-12-21
archived: 2026-08-28
draft: false
tags:
  - archive
  - twitter
  - cmuratori
description: "Shading language standardization for the web is completely f'ed."
in_reply_to: ""
---

## Source

- URL: https://x.com/cmuratori/status/1473406996577615874
- Author: Casey Muratori (@cmuratori)
- Posted: 2021-12-21 21:36:17

## Thread

**1/** **@cmuratori** ^1473406996577615874

Shading language standardization for the web is completely f'ed. Even trying to follow the development process is basically impossible. Consider this post from 2018 (https://webkit.org/blog/8482/web-high-level-shading-language/), which is now completely false and all of the projects linked are now github 404's.

Branches: [[archive/threads/cmuratori/2021-12-21-shading-language-standardization-for-the-web-is/2021-12-21-datgame-how-would-you-feel-about-writing-shaders-in-rust]], [[archive/threads/cmuratori/2021-12-21-shading-language-standardization-for-the-web-is/2021-12-22-Aidiakapi-yeah-the-state-is-awful-and-the-shader-language]]

**2/** **@cmuratori** ^1473407239125757952

I guess originally they were going to do a sensible thing which was a modified HLSL for security guarantees, with a compiler. Now they are doing a text format that is "trivially convertible to SPIR-V" but without the SPIR-V part and no binary rep, I think?

**3/** **@cmuratori** ^1473407785639444480

I also tried to understand WTF was being claimed in http://kvark.github.io/spirv/2021/05/01/spirv-horrors.html but literally nothing the OP discussed seemed like anything resembling a "horror". It just sounded like the learning process of someone who didn't know SPIR-V learning SPIR-V?

Branches: [[archive/threads/cmuratori/2021-12-21-shading-language-standardization-for-the-web-is/2021-12-21-Jonathan_Blow-i-read-this-page-and-its-very-bizarre-none-of-the]]
