---
title: "I dev with the debugger attached 100% of the time, and unless I'm doing something visual like UI, I literally always put a breakpoint at the beginning of the new code I've just written and step through it before I ever let it \"run\"."
type: archive
source: twitter
source_url: "https://x.com/nicbarkeragain/status/2090577570916184127"
author: "Nic Barker"
handle: nicbarkeragain
post_id: "2090577570916184127"
date: 2026-08-20
archived: 2026-08-28
draft: false
tags:
  - archive
  - twitter
  - nicbarkeragain
description: "I dev with the debugger attached 100% of the time, and unless I'm doing something visual like UI, I literally always put a breakpoint at the beginning of the new code I've just written and step through it before I ever let it \"run\"."
in_reply_to: ""
---

## Source

- URL: https://x.com/nicbarkeragain/status/2090577570916184127
- Author: Nic Barker (@nicbarkeragain)
- Posted: 2026-08-20 23:11:48

## Thread

**1/** **@nicbarkeragain** ^2090577570916184127

I dev with the debugger attached 100% of the time, and unless I'm doing something visual like UI, I literally always put a breakpoint at the beginning of the new code I've just written and step through it before I ever let it "run". About half the time I find a bug immediately.

**2/** **@MrJayLC** ^2090913197964341464

**@nicbarkeragain**

idk if you've seen @NOTimothyLottes video on C, but the "talk" function really *speaks* to me.

It's essentially what I do: Log statements everywhere and run the code (usually debugger attached). Either it all works, or I get some exception and iterate.

**3/** **@NOTimothyLottes** ^2090964526325731761

**@MrJayLC** **@nicbarkeragain**

Oh the classic problem. New programmer hired into a mountain of technical dept with no documentation and code that obfusticates meaning (like say Unreal). So yeah you'd use that debugger as an archaeologist tool to try to understand enough of a subset of it to make changes ->

**4/** **@NOTimothyLottes** ^2090965834185211915

**@MrJayLC** **@nicbarkeragain**

Some lucky people get good code bases with good docs and transcend the need for classic debuggers, typically need a new subset of tooling because the issues being solved are parallel or timing related optimizations -> need to run on a release build, etc

**5/** **@NOTimothyLottes** ^2090966335710732378

**@MrJayLC** **@nicbarkeragain**

And then need to see the relationship of behavior between parallel things. Then you want effectively minimal cost reporting or manual injection. Not 'printf' because that is a boat anchor, and writing to console screws timing ->

**6/** **@NOTimothyLottes** ^2090966786950807966

**@MrJayLC** **@nicbarkeragain**

Instead as minimal runtime effect as possible -> one atomic to pick the next line, and a store to a fixed size cacheline in a mapped page that could say be mapped even across multiple processes (so relationship between host and client is order accurate)

**7/** **@NOTimothyLottes** ^2090967640550289917

**@MrJayLC** **@nicbarkeragain**

No kernel calls or even page misses (mlockall) on runtime messaging, and when your project recompiles at runtime without exit, or even restarts in less than a second, you can track down issues faster than it takes to load visual studio.

**8/** **@NOTimothyLottes** ^2090968558394061175

**@MrJayLC** **@nicbarkeragain**

Seriously pro devs build the tooling into the engine, so they always know the timing and runtime behavior and work with eyes open, a full understanding of what is happening, ability to reason about why something might fail without even loading a debugger
