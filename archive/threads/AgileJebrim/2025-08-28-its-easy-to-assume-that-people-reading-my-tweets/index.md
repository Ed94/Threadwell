---
title: "It’s easy to assume that people reading my tweets are already familiar with the context of the problems I aim to solve, but clearly this post took off with a new audience, so let me try to rewind a bit to focus on why I do what I do."
type: archive
source: twitter
source_url: "https://x.com/AgileJebrim/status/1961045175687397728"
author: "Jebrim"
handle: AgileJebrim
post_id: "1961045175687397728"
date: 2025-08-28
archived: 2026-08-29
draft: false
tags:
  - archive
  - twitter
  - AgileJebrim
description: "It’s easy to assume that people reading my tweets are already familiar with the context of the problems I aim to solve, but clearly this post took off with a new audience, so let me try to rewind a bit to focus on why I do what I do."
in_reply_to: ""
---

## Source

- URL: https://x.com/AgileJebrim/status/1961045175687397728
- Author: Jebrim (@AgileJebrim)
- Posted: 2025-08-28 12:36:18

## Thread

**1/** **@AgileJebrim** ^1961045175687397728

It’s easy to assume that people reading my tweets are already familiar with the context of the problems I aim to solve, but clearly this post took off with a new audience, so let me try to rewind a bit to focus on why I do what I do.

Firstly, I am a software engineer by training, meaning I think in terms of only writing software and having constraints that resolve a customer’s problem. If code cannot be traced to requirements that accomplish this, then it’s a waste of time and resources.

Secondly, there is a distinction between real-time and deterministic execution times that I must make clear. The former has a well-bounded execution time; it cares about worst-case. The latter is an even stricter definition that focuses on fixed execution times for any given input, minimizing the gap between max and min execution times. I go one step further and target deterministic execution times independent of the specific contents of the input data, which is what invalidates hash maps for me.

Now the big question is why?

To start, verifying worst-case execution time (WCET) in traditional real-time code is very hard and very expensive. You must somehow prove that you’ve identified the most expensive branch and every cache miss and misprediction and hardware interrupt and context switch and tested it to verify you meet the requirements. Yuck. It’s simply not feasible for most budgets and timelines and isn’t particularly portable across hardware either.

By instead targeting fixed-execution times independent of data contents, similar to the compile-time approach used for secret data in cryptography, and can just prove that data contents cannot cause fluctuations in timing, especially algorithmically, then I can remove a whole class of expensive effort in WCET analysis and make achieving real-time more economically achievable. Especially if this is transformed into a special compiler able to provide these guarantees for other programmers.

Basically it’s a serious cost-cutting measure. So now I’ve explained why I do deterministic execution times regardless of data inputs as a means of helping more cheaply verify real-time deadline guarantees, but I haven’t explained why to care about real-time. What customer problem(s) does real-time solve?

Here’s a list of some of them:

- Hardware and software must be synchronized in many safety-critical embedded systems or else hardware will do something the software doesn’t expect. This is the traditional case for real-time.

- Having late frames when rendering in a wide field-of-view (e.g. VR, domes, etc.) can quite literally result in the user getting sick. Determinism is important in the flight sim industry that I work in as everything is wide FOV.

- User-generated content in a synchronized stateful backend service, such as Roblox, X, Facebook, Twitch, Minecraft, or JebScape. If the inputs from one set of users are able to impact the performance experience or server stability for other users, then it can prevent achieving desired SLA guarantees. It also makes you more vulnerable to DDOS and similar attacks. Minimize the attack surface to provide the best experience for your users.

- Disabling the ability for end users to drive how much money comes out of your wallet when you pay for hosting. Better financial predictability. If you have workloads that dynamically spin up worker instances as needed, then you might find yourself with an unexpectedly large bill after an attack.

- Many other general problems across a wide range of interactive software that involve responsiveness to user input. All else being equal, an application that can provide reliable fast responses is better quality than one that is occasionally laggy and stuttering. Customers will be happier with the former than the latter.

- Inferencing with AI, JIT compiling, ACH bank transfers, video processing, etc. People don’t like sitting around waiting for a result and value both sooner and more predictable completion times.

**2/** **@valigo** ^1961071117780799501

I wonder, how do you approach something like the following with restrictions from your original post:

Let's say you want to make a text editor, or a code analysis system. And you want it to support both big codebases (say, Unreal Engine, or Chromium), and small projects. 

Like, if you want to have a feature that shows references for some common type, and you want to have a count of how many are there. You also want a very fast navigation, which means you need to index the codebase ahead of time, and then have this index readily available (preferably, in RAM).

With approach of not having any dynamic allocations, do you just say "ok Unreal Engine codebase is how much memory you must have" and load everything, or do you slice it of somehow? I personally would prefer the program to eat as much RAM as it wants if it makes everything fast (we are assuming a good faith well-written program that actually utilizes it efficiently, not some web slop lol). Do you reserve a fuck ton of address space and then try to organize your memory patterns in a way that it never reallocates and only adds additional pages after those already used?

I overall understand your take about dynamic reallocs and hash table collisions introducing random delays and hurting realtime-ness of the system. It's just not intuitive to me how (if at all) you can be this strict about these principles (as opposed to using them as an overall good rule of thumb) in some general sense like this.

**3/** **@AgileJebrim** ^1961092844216521185

The tl;dr is that you have a small view buffer allocated with only as much room for data that you need right now and in the near future. You then stream in everything else as you need it, ensuring things are sized large enough to that the bandwidth can support it in the target tick rate you want.

You can know the context of your streaming/paging needs within your application way better than the OS ever could with just a generic LRU cache.

**4/** **@valigo** ^1961105858860855533

Feel free to not answer if this is too much text

But let's say I search for a symbol in my codebase, and I want to display candidates in real time. This means that I need to either pre-index everything in the codebase and have it in RAM for faster filtering, or I need to do it on the fly, and go to the disk on every key press, if I only have a small static buffer to hold information about my codebase. Yes, in this case I will surely have consistent performance, but it will be consistently bad. 

So my question is not as much as how to statically allocate memory that I will display on the screen - this is somewhat realistic to know upfront, because there's only this much pixels in the monitor, but I'm more talking about background information that I need to query like a database. Having a small buffer that you constantly repopulate from disk sounds like it will give worse experience than letting it scan the whole data and dump it to RAM in processed and search-friendly way.

Maybe you mean to do it in two passes - for example, first part is non-realtime, when I scan the whole database, process it, allocate/reallocate as much as I want. And yeah it might take some time, but then after it's done I can switch to "real-time" mode, where all sizes are already known, and I can work with the codebase without allocating anything new. But then how do I handle situations where I add new stuff to the codebase, so it might need to grow.

I know this goes too much into databases realm and things they do to incorporate disk usage but in a way that's not morbidly slow, but I'm specifically talking about cases that are small enough to fit to ram, but large enough to just preallocate everything up-front.

**5/** **@AgileJebrim** ^1961208259383103942

**@valigo**

If you were to consider just the cpp and hpp files, how many bytes do you think it would be for UE5 or Chromium if we just threw every single file into memory at startup?

Let’s just assume for this case that we’re allowing malloc once for loading these files to meet that size.

**6/** **@AgileJebrim** ^1961208776658194779

**@valigo**

Even if you’re talking a couple million lines of code at an average of 40 chars per line, that would only be 800MB. You wouldn’t even need streaming at that point. Just keep everything in DRAM.

**7/** **@valigo** ^1961210612844810254

I think 10x editor uses something like 1.5gigs for UE5 codebase, so I guess makes sense. I also read your other thread where the idea is to go from strings to array indices as fast as you can in your apis, and I see what you mean, and it makes sense to me.

I once went this rabbit hole of linear array search -> generic hash table of [string, struct] -> my own purpose-built "hash function" (it's not really hash function, it's just a simple transformation of predefined string to a static array index) so I can do array access without any possible collisions. My array is a bit sparse now, but it's the best by far performance wise.

Unfortunatly, the industry I work in, doesn't let me do things like that to the max (I mostly work in outsource contracting, and most of my job is maintaining and improving existing codebases), but these principles are definitely good.

**8/** **@AgileJebrim** ^1961211708741161259

**@valigo**

If you really want to do a linear search, it’s actually extremely trivial in the SIMD/GPU world. Define a cap as to how many chars a token can be, which on a GPU could be 128 bytes to represent a single token within a warp, and then scan through every single token in parallel.

**9/** **@AgileJebrim** ^1961212145674117379

**@valigo**

Different warps and later SMs can then locally accumulate their own totals for each token/symbol within their subset of the dataset and you just reduce add at each level as you converge into global space.

Branches: [[archive/threads/AgileJebrim/2025-08-28-its-easy-to-assume-that-people-reading-my-tweets/2025-08-28-AgileJebrim-this-is-assuming-youre-still-keeping-everything]]
