---
title: "I have a moral dilemma in the design of the programming language."
type: archive
source: twitter
source_url: "https://x.com/Jonathan_Blow/status/1871638900554317934"
author: "Jonathan Blow"
handle: Jonathan_Blow
post_id: "1871638900554317934"
date: 2024-12-24
archived: 2026-08-26
draft: false
tags:
  - archive
  - twitter
  - Jonathan_Blow
description: "I have a moral dilemma in the design of the programming language."
in_reply_to: ""
---

## Source

- URL: https://x.com/Jonathan_Blow/status/1871638900554317934
- Author: Jonathan Blow (@Jonathan_Blow)
- Posted: 2024-12-24 19:27:41

## Thread

**1/** **@Jonathan_Blow** ^1871638900554317934

I have a moral dilemma in the design of the programming language.

We have an assembler built into the compiler, x86-only right now, written by @rflaherty71; it is high-level and nice to use if you program a lot in assembly, but, it is looking like that is a very rare use case.

Because the x64 instruction format is such a nightmare, the assembler uses this big table-driven system to generate instructions. There are 20,000 lines of tables and then a few thousand lines of code for the actual assembler ... but all together this comprises about 25% of the source code of the entire compiler, just to do assembly language on one platform.

And of course we want to do other CPUs -- at least ARM, certainly some other ones before too long. 

I had a plan I was excited about to externalize the assembler -- put it in userspace and provide a good convention by which arbitrary userspace assemblers could interoperate with the compiler.  I started working on this yesterday and it's partially done.

Then I realized, wait -- in the long term we don't want to depend on LLVM or any other backend to generate code, and in fact we would like to remove LLVM as soon as is feasible because it is such a horrifically cumbersome dependency. The main functionality we get out of LLVM right now is the ability to target various CPUs or WASM, and the ability to optimize very well. We have our own x64-only backend, but it doesn't optimize.

And here's the thing. If we want to generate good output machine code, that involves good instruction selection, which means ... we would have something like that 20,000 lines of tables compiled in anyway (??), which removes most of the complexity-reduction benefit in externalizing the compiler. We still gain from letting people have freedom in terms of doing assembly stuff, but realistically this is still a very small percentage of the audience, even among the hardcore programmers that are our intended user base. 

But if I externalize the assembler then we are *doubling* the amount of complexity we maintain, because now there are all these tables compiled into the compiler, and then there's also a user-level module.

So that seems like a bummer in the short-term where we are already limited in rate of progress by complexity of the compiler.

One other motivation for externalizing the assemblers is that it would seemingly solve one of the problems we have currently, which is that we only let you do assembly for x86. Day one as soon as we turn this on, people could do assembly for ARM etc, even if it was some janky assembler they wrote, and this could be improved over time.

But this is only true because we lean on LLVM to generate ARM code right now. As soon as we stop doing that, the compiler needs itself to generate ARM code with good instruction selection, and we are back to the problem I described before. If you imagine the long-term future of any compiler, it needs to be able to generate machine code for any platform you are targeting, so externalizing this ability is actually duplication of functionality in all cases.

So maybe it's better to keep the assembler inside the compiler and not do a userspace one. But there's also a problem with that -- our assembly language, while high-level in a really nice way (example, it lets you use variable names and those get mapped to registers, so you don't have to sweat over exactly what register holds what all the time), anyway, while nice, it's also kind of opinionated in terms of syntax etc, which means if you have some assembly code from some reference that you would like to use, you basically have to rewrite it, you can't just paste it in. That is a downside. (And I imagine that for something like WASM you would really want to be able to paste it in? Or maybe WASM is so broken this doesn't make sense either. I haven't investigated.)

Also it's unclear how similar the syntax would look for ARM, etc, and if you have to learn a totally different kinda-high-level syntax for every single target, that sucks too.

I feel like there is a market out there for a compiler backend component that takes upon itself the job of machine code generation *only*. In principle LLVM does this but it's a tremendous headache, in part because LLVM is extremely non-reality-based in some of the ways it does things (you would not believe the huge hassle we have to go through just to tell LLVM about pointers in global data -- something that you need to do when outputting data for almost any programming language. It is a bunch of complicated and potentially slow code that has to run every time you compile, when it *should* be trivial for us just to give LLVM a flat array of pointer positions and be done with it, BECAUSE THAT IS WHAT EVERY OPERATING SYSTEM WANTS).

If there were a useful long-term component we could integrate that solves some of these problems -- either a machine code generator or an assembler or both -- I would consider using it, if it does not cause us to fail at our long-term goals (LLVM cannot be a core component for this reason -- it is way too slow and would cause us to fail our performance goals).  

One more ingredient in all this is the changing role of assembly language. Back when we put an assembler into the compiler, I imagined that we would have almost no intrinsics, and if you want to do something very specific, even like SIMD or whatever, you would drop to the assembly language, and it would be nice enough to do a good job there.

But as things have played out, I don't like how this manifests itself in the 'standard library' that we provide, even just for x86 so far. If we start adding other CPUs it will really bloat the code and make it a lot less readable, and this starts to ruin one of the things I feel we have been very successful at: providing a readable, understandable standard library that does not make you feel sick when you look at it. (C and C++ veterans will know what I am talking about here). That's very valuable to me and I don't want to wreck it. 

So I am starting to think about, okay, maybe we pivot back toward having intrinsics for stuff like vector instructions, and we try to provide a base set that can target multiple CPUs so you don't have to do anything platform-specific in most code. And then if you want the absolute best performance maybe you do assembly.

But this also seems shortsighted, because x86-style vector instructions as we have them today seem like a very particular design that may not be what anyone wants in the future. (There are CPU designs where you do vectors of arbitrary length, and GPUs started with this assumption "we are going to do everything as 4-vectors" back in the early days, but as they got more sophisticated, as far as I know they completely devectorized and everything is scalars or is revectorized to particular sizes behind the scenes because this is how you actually make things fast. [But I am vaguely guessing here; this is not my area at all.] AI processors, I don't even know what they look like if you try to program them with general code, but it is probably not 4- or 8-wide SIMD.)

(That 20,000 lines of tables that I mentioned above is *mostly* filled with all the poopy SIMD instructions that were introduced in the past N years. Without them the table would be much smaller and I wouldn't feel so icky about it. Maybe we can compress the table because we have one entry per size/etc ... to pick a random instruction, pcmpeq has 15 elements in this table, and by the time the necessary data gets all defined, for about 180 lines of the table's source code. Just for that one instruction.)

But the point here is that if we pivot back toward intrinsics for SIMD and other stuff (popcount, bit seeks, etc), then we are getting much less use out of the assembler, which seems to imply we should choose a design where we invest less in it. But we still need to do good instruction selection, argh.

I probably forgot to mention several significant factors of this question, but there you go. I am trying to do the most functional and excellent thing for the user, and it's not obvious what that is, given the opportunity cost of any implementation work we do.

Comments welcome.

Branches: [[archive/threads/Jonathan_Blow/2024-12-24-i-have-a-moral-dilemma-in-the-design-of-the/2024-12-24-PhilAndrew61181-i-know-a-few-compiler-people-and-they-also-hate]], [[archive/threads/Jonathan_Blow/2024-12-24-i-have-a-moral-dilemma-in-the-design-of-the/2024-12-24-TylerGlaiel-iirc-your-language-lets-you-run-code-at-compile]], [[archive/threads/Jonathan_Blow/2024-12-24-i-have-a-moral-dilemma-in-the-design-of-the/2024-12-24-flaratt_ljos-for-graphics-apis-you-can-have-a-mapping-for-the]], [[archive/threads/Jonathan_Blow/2024-12-24-i-have-a-moral-dilemma-in-the-design-of-the/2024-12-24-spartacosan-as-an-embedded-dev-working-with-arm-and-some-dsps]], [[archive/threads/Jonathan_Blow/2024-12-24-i-have-a-moral-dilemma-in-the-design-of-the/2024-12-24-ken__maples-in-my-experience-writing-optimized-numerical]], [[archive/threads/Jonathan_Blow/2024-12-24-i-have-a-moral-dilemma-in-the-design-of-the/2024-12-24-NOTimothyLottes-suggestion-focus-on-compile-speed-and-small-size]], [[archive/threads/Jonathan_Blow/2024-12-24-i-have-a-moral-dilemma-in-the-design-of-the/2024-12-24-drathier-please-consider-the-data-communication-cost-of]], [[archive/threads/Jonathan_Blow/2024-12-24-i-have-a-moral-dilemma-in-the-design-of-the/2024-12-24-bottlecrow_-is-it-too-late-to-target-some-subset-of-c-for-the]], [[archive/threads/Jonathan_Blow/2024-12-24-i-have-a-moral-dilemma-in-the-design-of-the/2024-12-24-lemire-we-have-two-practical-variable-length-simd]], [[archive/threads/Jonathan_Blow/2024-12-24-i-have-a-moral-dilemma-in-the-design-of-the/2024-12-24-jitl-i-think-you-should-keep-the-assembler-in-tree]], [[archive/threads/Jonathan_Blow/2024-12-24-i-have-a-moral-dilemma-in-the-design-of-the/2024-12-24-RufeDotOrg-the-costs-of-dropping-simd-are-low-in-the-space]], [[archive/threads/Jonathan_Blow/2024-12-24-i-have-a-moral-dilemma-in-the-design-of-the/2024-12-24-joe_sweeney-if-the-plan-in-the-long-term-is-to-be-off-llvm]], [[archive/threads/Jonathan_Blow/2024-12-24-i-have-a-moral-dilemma-in-the-design-of-the/2024-12-24-binarybardo-i-feel-like-you-sort-of-answered-your-own]], [[archive/threads/Jonathan_Blow/2024-12-24-i-have-a-moral-dilemma-in-the-design-of-the/2024-12-24-nullspector-i-would-prefer-a-cool-assembler-and-intrinsics]], [[archive/threads/Jonathan_Blow/2024-12-24-i-have-a-moral-dilemma-in-the-design-of-the/2024-12-24-OlexGameDev-i-wonder-if-this-is-this-why-msvc-did-away-with]], [[archive/threads/Jonathan_Blow/2024-12-24-i-have-a-moral-dilemma-in-the-design-of-the/2024-12-25-bztree-could-you-keep-the-tables-in-userspace-but-mark]], [[archive/threads/Jonathan_Blow/2024-12-24-i-have-a-moral-dilemma-in-the-design-of-the/2024-12-25-5ms7ltr2-im-working-with-my-personal-language-with-some]], [[archive/threads/Jonathan_Blow/2024-12-24-i-have-a-moral-dilemma-in-the-design-of-the/2024-12-25-JBrooksBSI-it-might-be-worth-looking-at-spirv-v-as-it]], [[archive/threads/Jonathan_Blow/2024-12-24-i-have-a-moral-dilemma-in-the-design-of-the/2024-12-25-mvandevander-i-definitely-dont-see-a-reason-to-externalize-the]], [[archive/threads/Jonathan_Blow/2024-12-24-i-have-a-moral-dilemma-in-the-design-of-the/2024-12-25-strager-can-popcount-and-simd-functions-be-implement]], [[archive/threads/Jonathan_Blow/2024-12-24-i-have-a-moral-dilemma-in-the-design-of-the/2024-12-25-hasen_95dx-i-think-ffmpeg-is-one-of-the-large-prolific-open]], [[archive/threads/Jonathan_Blow/2024-12-24-i-have-a-moral-dilemma-in-the-design-of-the/2024-12-25-jimrandomh-my-last-serious-work-on-compilers-was-a-project]], [[archive/threads/Jonathan_Blow/2024-12-24-i-have-a-moral-dilemma-in-the-design-of-the/2024-12-25-stainless_code-as-the-solution-for-this-exact-dillema-in-my-lang]], [[archive/threads/Jonathan_Blow/2024-12-24-i-have-a-moral-dilemma-in-the-design-of-the/2024-12-25-slimRAWapp-i-do-lots-of-asm-intrinsics-i-like-the]], [[archive/threads/Jonathan_Blow/2024-12-24-i-have-a-moral-dilemma-in-the-design-of-the/2024-12-25-EskilSteenberg-id-consider-being-able-to-compile-to-c-then-you]], [[archive/threads/Jonathan_Blow/2024-12-24-i-have-a-moral-dilemma-in-the-design-of-the/2024-12-25-MrJayLC-with-incomplete-knowledge-and-opinions-i-believe]], [[archive/threads/Jonathan_Blow/2024-12-24-i-have-a-moral-dilemma-in-the-design-of-the/2024-12-25-nicbarkeragain-its-interesting-that-ive-seen-this-exact-issue-re]], [[archive/threads/Jonathan_Blow/2024-12-24-i-have-a-moral-dilemma-in-the-design-of-the/2024-12-25-_dtx___-feels-like-the-inevitable-path-down-to-creating-a]], [[archive/threads/Jonathan_Blow/2024-12-24-i-have-a-moral-dilemma-in-the-design-of-the/2024-12-26-prenex2-i-think-its-a-question-of-modularity-in-that-long]], [[archive/threads/Jonathan_Blow/2024-12-24-i-have-a-moral-dilemma-in-the-design-of-the/2024-12-26-neo_ar218-im-going-to-admit-my-radical-opinion-here-i-think]], [[archive/threads/Jonathan_Blow/2024-12-24-i-have-a-moral-dilemma-in-the-design-of-the/2024-12-26-LubaRaphael-ive-never-looked-at-a-real-world-optimizer-are]], [[archive/threads/Jonathan_Blow/2024-12-24-i-have-a-moral-dilemma-in-the-design-of-the/2024-12-26-clattner_llvm-llvm-does-what-you-want-you-just-need-to-learn]], [[archive/threads/Jonathan_Blow/2024-12-24-i-have-a-moral-dilemma-in-the-design-of-the/2024-12-26-akatatsu27-are-you-aware-of-fasmg-its-an-assembler-engine]], [[archive/threads/Jonathan_Blow/2024-12-24-i-have-a-moral-dilemma-in-the-design-of-the/2024-12-26-tannergooding-why-are-your-metadata-tables-so-large-ryujit-the]], [[archive/threads/Jonathan_Blow/2024-12-24-i-have-a-moral-dilemma-in-the-design-of-the/2024-12-28-auburnsounds-fwiw-i-implement-simd-for-dlang-d-has-inline]], [[archive/threads/Jonathan_Blow/2024-12-24-i-have-a-moral-dilemma-in-the-design-of-the/2024-12-26-Jonathan_Blow-yeah-avx512-seems-like-kind-of-a-waste-of-time]]
