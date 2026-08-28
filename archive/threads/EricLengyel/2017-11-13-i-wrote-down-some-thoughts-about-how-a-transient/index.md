---
title: "I wrote down some thoughts about how a \"transient\" qualifier may have been a much better way to achieve move semantics in C++ compared to the awfulness of rvalue references."
type: archive
source: twitter
source_url: "https://x.com/EricLengyel/status/930222017441251330"
author: "Eric Lengyel"
handle: EricLengyel
post_id: "930222017441251330"
date: 2017-11-13
archived: 2026-08-27
draft: false
tags:
  - archive
  - twitter
  - EricLengyel
description: "I wrote down some thoughts about how a \"transient\" qualifier may have been a much better way to achieve move semantics in C++ compared to the awfulness of rvalue references."
in_reply_to: ""
---

## Source

- URL: https://x.com/EricLengyel/status/930222017441251330
- Author: Eric Lengyel (@EricLengyel)
- Posted: 2017-11-13 23:53:06

## Thread

**1/** **@EricLengyel** ^930222017441251330

I wrote down some thoughts about how a "transient" qualifier may have been a much better way to achieve move semantics in C++ compared to the awfulness of rvalue references.

http://ericlengyel.blogspot.com/2017/11/some-thoughts-about-rvalue-references.html

**2/** **@TimSweeneyEpic** ^930265529641824256

**@EricLengyel**

Propagating transience to a member is unsound in general. You could access the same value twice and the second copy could be bogus due to someone having already moved it.

**3/** **@EricLengyel** ^930267127524683777

**@TimSweeneyEpic**

I'd think that cases where the enclosing object wants to access a subobject that was already moved are less common and justify an explicit copy of the subobject as opposed to the current system where everything is explicitly moved.

**4/** **@TimSweeneyEpic** ^930269154346721280

**@EricLengyel**

That’s a crazy default. You’d write what looks like fine code, and find that variables are corrupted when used more than once because the compiler defaults to moving them.

**5/** **@EricLengyel** ^930280425850732544

**@TimSweeneyEpic**

It's likely we're not thinking in the same way. I don't see a problem with this since transience can never be implicitly added. Moving would continue to occur only after you're inside a context that has move semantics.
