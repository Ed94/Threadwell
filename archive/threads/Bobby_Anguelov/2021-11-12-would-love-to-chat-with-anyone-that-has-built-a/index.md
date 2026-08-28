---
title: "Would love to chat with anyone that has built a property grid with dearImgui with undo/redo support."
type: archive
source: twitter
source_url: "https://x.com/Bobby_Anguelov/status/1459186881749565442"
author: "Bobby Anguelov"
handle: Bobby_Anguelov
post_id: "1459186881749565442"
date: 2021-11-12
archived: 2026-08-27
draft: false
tags:
  - archive
  - twitter
  - Bobby_Anguelov
description: "Would love to chat with anyone that has built a property grid with dearImgui with undo/redo support."
in_reply_to: ""
---

## Source

- URL: https://x.com/Bobby_Anguelov/status/1459186881749565442
- Author: Bobby Anguelov (@Bobby_Anguelov)
- Posted: 2021-11-12 15:50:37

## Thread

**1/** **@Bobby_Anguelov** ^1459186881749565442

Would love to chat with anyone that has built a property grid with dearImgui with undo/redo support. I'd like to pick your brain on perhaps better solutions to the issues I'm having. I have a solution but its a lot of boilerplate code and backend machinery...

**2/** **@flaxed** ^1459187491194478604

**@Bobby_Anguelov**

Undo/redo might be orthogonal to a property grid editor. Which issues are you currently facing?

**3/** **@Bobby_Anguelov** ^1459189682403688448

**@flaxed**

What do you mean orthogonal?! It's an editor, most editors offer undo/redo...

I'm basically having headaches trying to only modify the source data when an edit operation completes. Right now it looks like I need to make a duplicate of the source data as a working copy.

**4/** **@ocornut** ^1459246121931390979

**@Bobby_Anguelov** **@flaxed**

Ihmo there’s some form of orthogonal from actual widgets events, successive uses of a sliders with release ought to be merged anyway.

**5/** **@Bobby_Anguelov** ^1459247944746549252

**@ocornut** **@flaxed**

Not sure about that, many times a user will set the slider to something, then set it to something else, then a third time. 

After that, they often use undo/redo to jump between edits to visualize the different options. This is a pretty common usage as far as I'm aware.

**6/** **@Bobby_Anguelov** ^1459248261278146563

**@ocornut** **@flaxed**

What you dont want is to track intermediate changes while dragging, only the "committed" edit action (for a slider = on release).

**7/** **@ocornut** ^1459260149663678465

**@Bobby_Anguelov** **@flaxed**

The thing is even with this it often becomes a lots of changes, the “commit” often happens several times in a row, but i understand its more logical.
