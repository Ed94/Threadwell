---
title: "Why do we spend so much effort to encode programming language semantics into a textual form just so a parser can go through the error-prone process of ripping that same exact information back out? Why not work directly on a program's abstract-syntax tree? (1/8)"
type: archive
source: twitter
source_url: "https://x.com/rfleury/status/1166970972882128896"
author: "Ryan Fleury"
handle: rfleury
post_id: "1166970972882128896"
date: 2019-08-29
archived: 2026-08-27
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

Branches: [[archive/threads/rfleury/2019-08-29-why-do-we-spend-so-much-effort-to-encode/2019-08-29-SasLuca-you-can-still-have-the-representation-be-textual]], [[archive/threads/rfleury/2019-08-29-why-do-we-spend-so-much-effort-to-encode/2019-08-29-marcos_don-would-you-consider-tools-like-unreals-blueprints]], [[archive/threads/rfleury/2019-08-29-why-do-we-spend-so-much-effort-to-encode/2019-08-29-saidalattrach-i-was-having-similar-thoughts-about-this-i-am]], [[archive/threads/rfleury/2019-08-29-why-do-we-spend-so-much-effort-to-encode/2019-08-29-stbachmann-why-arent-we-working-straight-in-assembly-code]], [[archive/threads/rfleury/2019-08-29-why-do-we-spend-so-much-effort-to-encode/2019-08-29-azmreece-are-you-familiar-with-stevekrouse-and-his-http]]

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

Branches: [[archive/threads/rfleury/2019-08-29-why-do-we-spend-so-much-effort-to-encode/2019-08-29-William_Bundy-for-a-moment-i-thought-you-were-revealing-your]]

**9/** **@hmn_riscy** ^1167764451724017664

**@rfleury**

Many people seem skeptical of this idea with regards to alternative ways to render or edit the AST but I think there is a pretty clear path forward there personally...

**10/** **@hmn_riscy** ^1167765299166437377

**@rfleury**

What hula is going to have is a kind of hybrid token/text based editor with autocomplete, think TI-BASIC meets colorForth. Multiple rendering modes, panels that show different things. You've got a node editor that is visualising the AST as code on the left, next panel is asm,

**11/** **@hmn_riscy** ^1167765816017899520

**@rfleury**

next panel is data section, you could have plenty of other things/configure this but basically if you want to add a global variable, you pop it over in the data section which is where it literally lives in the executable, that kind of thing has such an obvious representation

**12/** **@hmn_riscy** ^1167766237939732480

**@rfleury**

If you start typing a string in the code that matches the var, it appears in the autocomplete and lets you directly reference that node, or you can just keyboard shortcut over to the data panel and visually select where you are referencing

**13/** **@hmn_riscy** ^1167766952288370688

**@rfleury**

the asm output updates in real time, think godbolt's code explorer except a standard part of your code editor. Compiler doesn't do optimisation, instead you interact with the optimiser more intimately integrated with profiling tools and optimisations are kept like patch files...

**14/** **@hmn_riscy** ^1167767360935251968

**@rfleury**

which provide transformations over the ast to be applied before compiling the ast for a target, a file for each target profile basically

**15/** **@hmn_riscy** ^1167768102651797505

**@rfleury**

People jump to thinking about lisp because s-expressions are a direct representation of an AST, but that's really not the correct way to think about this concept, that's not how you want it rendered (unless you love your parens and RPN I guess!)
