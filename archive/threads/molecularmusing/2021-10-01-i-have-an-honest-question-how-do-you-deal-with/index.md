---
title: "I have an honest question: how do *you* deal with all the broken software if it seriously impedes your daily work?"
type: archive
source: twitter
source_url: "https://x.com/molecularmusing/status/1443886672001765393"
author: "Stefan Reinalter"
handle: molecularmusing
post_id: "1443886672001765393"
date: 2021-10-01
archived: 2026-08-27
draft: false
tags:
  - archive
  - twitter
  - molecularmusing
description: "I have an honest question: how do *you* deal with all the broken software if it seriously impedes your daily work?"
in_reply_to: ""
---

## Source

- URL: https://x.com/molecularmusing/status/1443886672001765393
- Author: Stefan Reinalter (@molecularmusing)
- Posted: 2021-10-01 10:33:03

## Thread

**1/** **@molecularmusing** ^1443886672001765393

I have an honest question: how do *you* deal with all the broken software if it seriously impedes your daily work?
I mean, this week alone I filed 7 bugs in total, with 3 major companies.
How do you cope? What's your strategy if this hinders you in getting work done?

**2/** **@rfleury** ^1443929965850857474

**@molecularmusing**

I prefer to minimize dependencies, keep everything local (libraries, tools) when possible, and upgrading when *I* choose to do so. Libraries, ideally, are simply-built source files included directly into the codebase.

**3/** **@molecularmusing** ^1443932063086923776

**@rfleury**

The three biggest dependencies for me are Windows, VS, and Qt.
All are monolithic behemoths where fixing stuff myself is either impossible (Win10, VS), or tiresome to report bugs (all 3 of them).
I would love to actually be able to fix stuff myself, eventhough I shouldn't have to

**4/** **@molecularmusing** ^1443932330381414401

**@rfleury**

Maybe I should look more at OSS stuff, use the Clang toolchain and other editors for my dev work, but then I'm still stuck with having to support VS for my software.

**5/** **@rfleury** ^1443951646250205187

**@molecularmusing**

Yeah VS is unfortunate, sounds like you’re not exactly in the best situation :( I think of all dependent technologies as a foundation, and so I want it to be as static and predictable as possible. Sometimes that’s not possible, though, unfortunately…
