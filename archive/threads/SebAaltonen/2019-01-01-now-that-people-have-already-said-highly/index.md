---
title: "Now that people have already said highly controversial stuff like ”debugger is useless for C++ development”, I think I can share my own controversial thoughts about unit testing, DRY, copy-paste coding and function length, etc..."
type: archive
source: twitter
source_url: "https://x.com/SebAaltonen/status/1080069784644059139"
author: "Sebastian Aaltonen"
handle: SebAaltonen
post_id: "1080069784644059139"
date: 2019-01-01
archived: 2026-08-27
draft: false
tags:
  - archive
  - twitter
  - SebAaltonen
description: "Now that people have already said highly controversial stuff like ”debugger is useless for C++ development”, I think I can share my own controversial thoughts about unit testing, DRY, copy-paste coding and function length, etc..."
in_reply_to: ""
---

## Source

- URL: https://x.com/SebAaltonen/status/1080069784644059139
- Author: Sebastian Aaltonen (@SebAaltonen)
- Posted: 2019-01-01 11:54:38

## Thread

**1/** **@SebAaltonen** ^1080069784644059139

Now that people have already said highly controversial stuff like ”debugger is useless for C++ development”, I think I can share my own controversial thoughts about unit testing, DRY, copy-paste coding and function length, etc... with 20 years of C++ programming experience.

Branches: [[archive/threads/SebAaltonen/2019-01-01-now-that-people-have-already-said-highly/2019-01-01-grumpyboy-is-that-really-highly-controversial-i-can-think]], [[archive/threads/SebAaltonen/2019-01-01-now-that-people-have-already-said-highly/2019-01-01-gavanw-there-is-a-useful-term-for-what-you-describe-as]], [[archive/threads/SebAaltonen/2019-01-01-now-that-people-have-already-said-highly/2019-01-01-justinhj-please-send-this-tweet-back-in-time-20-years-it]], [[archive/threads/SebAaltonen/2019-01-01-now-that-people-have-already-said-highly/2019-01-01-lukaszsawickiwx-funny-how-install-base-changes-architecture-all]], [[archive/threads/SebAaltonen/2019-01-01-now-that-people-have-already-said-highly/2019-01-01-noop_dev-sorry-but-for-many-people-this-is-going-to-look]], [[archive/threads/SebAaltonen/2019-01-01-now-that-people-have-already-said-highly/2019-01-01-TVogiannou-o-surprise-that-most-game-devs-had-similar]], [[archive/threads/SebAaltonen/2019-01-01-now-that-people-have-already-said-highly/2019-01-02-adrian_irwin-thank-you-for-this-youve-given-words-to-many]], [[archive/threads/SebAaltonen/2019-01-01-now-that-people-have-already-said-highly/2019-01-02-ifandbut01-man-threads-like-this-reminded-me-that-a-im-glad]], [[archive/threads/SebAaltonen/2019-01-01-now-that-people-have-already-said-highly/2019-01-02-MadOWatt-please-someone-put-this-in-an-article-or-blog]], [[archive/threads/SebAaltonen/2019-01-01-now-that-people-have-already-said-highly/2019-01-02-Reg__-thats-a-great-read-i-only-disagree-with-1-unique]], [[archive/threads/SebAaltonen/2019-01-01-now-that-people-have-already-said-highly/2019-01-02-sean_of_w-absolutely-love-this-thread-ive-repeated-these]], [[archive/threads/SebAaltonen/2019-01-01-now-that-people-have-already-said-highly/2019-01-02-Superlokkus-nice-thread-altougth-much-can-be-generalized-to]], [[archive/threads/SebAaltonen/2019-01-01-now-that-people-have-already-said-highly/2019-01-03-protopop-i-didnt-understand-everything-but-what-i-did]], [[archive/threads/SebAaltonen/2019-01-01-now-that-people-have-already-said-highly/2019-01-04-mxtnr-we-in-my-team-practice-exact-rules-in-our]]

**2/** **@SebAaltonen** ^1080071372603342848

I want to start this rant by telling that I have made (or allowed my team to make) countless of programming mistakes during my career: Textbook OOP (bird is animal), template monsters, too much codegen, over-engineered solutions, overly generic code, overuse of raw sync prims...

**3/** **@SebAaltonen** ^1080073388570411009

Each unit test is an additional dependency. Another call site that uses your function/class/data. Adding a dependency to code/data that has zero dependencies is not free. It adds inertia. Further changes of that code slow down and some refactorings/optimizations become infeasible

**4/** **@SebAaltonen** ^1080075056007532545

Adding an extra dependency (test case) for common library code (math, containers, etc) doesn’t add intertia, since code like this already has lots of dependencies and well defined API that doesn’t change. Test cases bring high benefit and very little downsides for code like this.

**5/** **@SebAaltonen** ^1080076144089665537

A good practice is to copy-paste code three times, and then refactor (extract) if all three instances are still doing the same thing. Before this, you don’t want to add unit tests, because your code has no dependencies. Code without dependencies is the best code. Safe to modify.

**6/** **@SebAaltonen** ^1080077641477226496

#1 problem in big code bases is entangled code dependencies. If you make code too generic or extract code too soon, you end up with more dependencies. Code used by 2+ call sites tends to eventually bloat with complex control flow. Bad performance, hard to understand and modify.

**7/** **@SebAaltonen** ^1080090864473554946

There are two types of long functions. Entangled and linear. If you avoid dependencies (see above), you can often write long functions which progress perfectly linearly. Trivial to read, modify and understand. No jumping around the code base. Minimal brain load.

**8/** **@SebAaltonen** ^1080091638628794368

It might seem like a good idea at first to split several such long functions to small functions and reuse some pieces of shared code. But this adds dependency between these functions and reading experience is no longer linear. Modifications affect many functions -> higher risk.

**9/** **@SebAaltonen** ^1080104439049011200

Programs transform data. Data dependencies are the actual dependencies and define which data you need to process in which order, how you can parallelize the processing and which invariants need to be maintained. Code dependencies are often false dependencies.

**10/** **@SebAaltonen** ^1080105687370383361

As said above, large functions aren’t usually a problem. The same is not true for large classes/structs containing lots of data unrelated to each other (Baseobject syndrome). You should never use real world object abstractions when you decide where you put each piece of data...

**11/** **@SebAaltonen** ^1080107022169894915

Instead, you should split your data according to all transforms you performed to that data. Data commonly accessed together go together. Fields not accessed at most call sites get split to separate structures. This avoids false dependencies and improves data cache utilization.

**12/** **@SebAaltonen** ^1080108724738576384

Critical section (mutex, etc) teaches a wrong way to think about synchronization. You don’t want to synchronize code. Code is immutable. Race conditions (RAW, WAR, WAW) are all pure data hazards. Shared sync primitive guarding one function/class is often a code smell.

**13/** **@SebAaltonen** ^1080109315279765505

Instead of fine grained sync primitives, you want to split your data so that you remove false dependencies. This often allows trivial parallel work and at the same time makes your code base much easier to modify and maintain. And improves your performance too (cache utilization).

**14/** **@SebAaltonen** ^1080122452129255424

You can’t multithread your code if you can’t ensure no data races. Processing of objects filled with pointers and references to other objects are hard to parallelize. Virtual functions are even worse. How can you know which data is accessed, if the call target is not known?

**15/** **@SebAaltonen** ^1080123406132092930

Most of your perf bottlenecks are in loops. No function is slow if you don’t call it many times. If you fully understand all data used inside a loop, you can often use parallel loop to scale it to all cores. Abstractions, virtual funcs and data dependencies make this hard.

**16/** **@SebAaltonen** ^1080127759513456641

Parallel for loop is one of the safest multithreaded optimizations you can make if you use simple data structures with no hidden data. Parallel for loop can be self contained inside a function. No need to modify other code. Works well with task/job schedulers too.

**17/** **@SebAaltonen** ^1080128337199202307

”Primature optimization is root of all evil” is the most misunderstood sentence in CS. Planning your data structures is part of the architecture design, not an optimization. Good data layout both improves performance dramatically, and also improves code maintainability.

**18/** **@SebAaltonen** ^1080128974032916481

Better version ”Do not micro-optimize unless profiler shows a bottleneck in that code”. Use profiling tools from the beginning of the project to react to problems before it is too late. Profile often and automate profiling for QA.

**19/** **@SebAaltonen** ^1080151287193202689

Best way to make future proof code: Make simplest possible code meeting current requirements. Minimize code/data dependencies. Overly generic code is not future proof. It handles some extra cases, but is overly complex. More refactoring to make it do what you actually need next.

**20/** **@SebAaltonen** ^1080152872522862594

Predicting future is hard. Try delaying decisions and writing code as late as possible. This way you make decisions and write code that better suits the actual needs. Coding a feature that nobody uses is waste of time. Coding a feature too early often leads to big refactoring.

**21/** **@SebAaltonen** ^1080210248898658307

Callbacks/delegates/listeners/events are dangerous in multithreaded environment. Destructor unregisters from all objs = modify all those objs (see next tweet). Firing an event = virtual call to N unknown targets. Impossible to make safe, unless you forbid parallelism during it.

**22/** **@SebAaltonen** ^1080211744910442499

Unknown object life time or owner is a code smell (ref count, shared_ptr). In most cases you should be able to define a clear owner for each object. In multithreaded environment custom destructors are very dangerous with ref count schemes. Hard to know when destructor is called.

**23/** **@SebAaltonen** ^1080216282912509953

I don’t personally hate unique_ptr or other non-refcounted RAII. But beware of memory allocation cost, mem fragmentation (on consoles and mobile) and pointer indirection cost (cache miss). Prefer value members instead of separate alloc for a member and use custom allocators...

**24/** **@SebAaltonen** ^1080216852578603009

The best way to allocate objects of certain type is to allocate a big block of storage for all of them and put them next to each other. Linear memory access pattern is much more cache friendly than allocating separate memory for each object. Big performance difference.

**25/** **@SebAaltonen** ^1080235671883841541

Most important custom allocator (in gamedev) is the frame temp allocator. It’s a fast (per thread) bump allocator that gets reset between each frame. Use it for all temporary allocs that have life time <= end of current frame. Big reduction in fragmentation and mem alloc cost.

**26/** **@SebAaltonen** ^1080240284548648960

If you use manual new/delete, use a memory leak detection tool. It’s also simple to wrap global new/delete to create your own leak tracker. Keep leak tracker active in daily dev builds. Once you have a custom mem tracker, you can use it to dump memory stats too. Very useful.

**27/** **@SebAaltonen** ^1080363421604950021

Not C++ related, but worth noting: Not all game features are equal. Features such as online multiplayer and deterministic simulation need consideration in data and processing model design. Can’t add features like these late in development. Agile doesn’t mean no planning at all.

**28/** **@SebAaltonen** ^1080365009392361472

When refactoring code, make a local branch (git) or shelve (P4). This makes it easier to ”throw away” your changes if you don’t like the result. Code will still be available for later use if you want to revisit. Don’t push refactorings to dev main unless you are 100% happy.

**29/** **@SebAaltonen** ^1080366081179635712

Every refactoring attempt gives you information. Never consider a failed attempt as useless work. However, focus your refactoring efforts to code that is actively in development. Code that works fine and doesn’t need any near future change doesn’t need to be touched.

**30/** **@SebAaltonen** ^1080368015462551552

Write well performing code by default, but don’t micro-optimize without profiling. When optimizing code, benchmark result on all target platforms and don’t push to dev main unless result is 100% clear (no regressions) and you are happy about code quality. Branch/shelve if unclear

**31/** **@SebAaltonen** ^1080377879697997824

Store profile trace/capture files for all platforms to maintain history. Name files after latest optimization/change. Do before/after compare after every optimization on all platforms. Write email + brief info to commit about gains. Automate regression tests for QA.

**32/** **@SebAaltonen** ^1080392769665929216

Pure ALU instruction count is not the most common performance bottleneck. Use platform specific low level profiling tools to find out the actual bottleneck instead of wasting time doing wrong optimizations. In CPU code, memory latency and cache are the most common bottlenecks.

**33/** **@SebAaltonen** ^1080394774971060224

Memory load->addr->load dependency chains (such as linked lists) are #1 poison for modern out-of-order CPUs. Prefer breadth first over depth first tree traversal to expose more parallelism for the CPU. CPU starts loading memory of all siblings concurrently, amortizing latency.

**34/** **@SebAaltonen** ^1080403941962194945

Before adopting a new C++ standard ensure that all target platform compilers have robust support. Investigate codegen and compile times for every feature you want to use on all compilers. It’s OK to ban certain feature if you feel it’s too risky to adapt at current state.

**35/** **@SebAaltonen** ^1081180113830666240

C++ has constructs that can make it a weakly-typed language. Avoid features such as implicit user defined conversion operators and implicit constructors. Use explicit keyword and concrete types whenever possible. Lean on compiler to catch type errors early and consistently.

**36/** **@SebAaltonen** ^1081181514413555712

Enable ”warnings as errors”. Prefer higher warning level and manually disable over-excessive warnings on platform/compiler basis. Review warning disable list after updating each compiler. Catching bugs at compile time is always better than runtime.

**37/** **@SebAaltonen** ^1081184460509495296

Use both static_assert (compile time) and assert (runtime) to validate assumptions. You should create separate assert_slow macro that is only enabled in debug config. This way you can reduce cost of slow asserts in hot code. Shipping config of course has all asserts disabled.

**38/** **@SebAaltonen** ^1081628712951578627

It’s a good idea to process things one ”type” (functionality) at a time, instead of one (aggregate) ”object” at a time. Loops become much simpler to understand as you don’t need lots of branches and don’t need indirect calls. Parallelizing your code becomes much easier.

**39/** **@SebAaltonen** ^1082172243050983425

Don’t repeat your code in your comments. Focus on things that code doesn’t tell you directly: why is code like this (workarounds, optimizations, API peculiarities), describe algorithm (or link to paper). If long function, add some comments as separators.

![](https://pbs.twimg.com/media/DwSl6hdX4AAZl8Y?format=jpg&name=orig)

**40/** **@SebAaltonen** ^1082177088289943552

Avoid writing code that your collegues can’t understand or modify. Maintenance of code requiring special skill set is problematic. Usually a lot simpler ”90%” solution is a far better choice in the long run. Writing tricky algos/structures/code isn’t a proof of skill. It’s a trap

**41/** **@SebAaltonen** ^1082971147753439233

If a piece of code works fine as is, and there’s no imminent changes that require modifying it, don’t refactor that code. Even if you don’t like the style of that code. Plenty of old code is perfectly functional and will remain so, unless requirements change.
