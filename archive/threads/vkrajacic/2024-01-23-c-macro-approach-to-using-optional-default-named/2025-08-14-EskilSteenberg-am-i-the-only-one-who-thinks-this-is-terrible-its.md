---
title: "@vkrajacic @CaptainKraft Am i the only one who thinks this is terrible? Its incredibly confusing to read and you cant see what parameters you miss, the header file is a lot more complex to read too."
type: archive
source: twitter
source_url: "https://x.com/EskilSteenberg/status/1955882027997069711"
author: "Eskil Steenberg"
handle: EskilSteenberg
post_id: "1955882027997069711"
date: 2025-08-14
archived: 2026-08-25
draft: false
tags:
  - archive
  - twitter
  - vkrajacic
description: "@vkrajacic @CaptainKraft Am i the only one who thinks this is terrible? Its incredibly confusing to read and you cant see what parameters you miss, the header file is a lot more complex to read too."
in_reply_to: ""
parent_post_id: "1749816169736073295"
---

## Source

- URL: https://x.com/EskilSteenberg/status/1955882027997069711
- Author: Eskil Steenberg (@EskilSteenberg)
- Posted: 2025-08-14 06:39:48

## Branch

**1/** @EskilSteenberg

@vkrajacic @CaptainKraft

Am i the only one who thinks this is terrible? Its incredibly confusing to read and you cant see what parameters you miss, the header file is a lot more complex to read too. You lose the WYIWYG nature of C. If you want this kind of ”clever” syntax why not use C++?

**2/** @vkrajacic

It might be confusing the first time you encounter it, because it's not used often in C codebases. But that's true for a lot of things in C, since you often have to invent better solutions (like strings or memory arenas).
As I said, I use this sparingly, but where it is used, it has always provided a better API. Ideally, I strive for ZII, so I don’t need a way of setting default values and can use a designated initializers to override when needed. That’s the best case scenario, and most of my base layer functions work like that.
This will not work with C++, as far as I know, because they messed up designated initializers. There are probably other ways to do it there, but I don’t want C++.

**3/** @EskilSteenberg

@vkrajacic @CaptainKraft

I think its confusing every time you see it. If i read:

function(x, .param = 42);

The code does not communicate, what this function can do or if I'm missing a parameter.

You also have to read all parameters in the function with one more level of indirection and thats slow.

**4/** @vkrajacic

I don’t see how this is different from:
void PushTransform(Rect rect, TransformParams params);
or
void PushTransform(Rect rect, Vec2 pivot, Dim2 scale, f32 angle, b32 clip);
You still need to read the header (or docs) to see what each argument does, and how to pass in some default value to ignore it.

For what it’s worth, the pattern I use more commonly is to separate functions that take extra parameters:
void PushTransform(Rect rect);
void PushTransformEx(Rect rect, Vec2 pivot, Dim2 scale, f32 angle, b32 clip);
The first one just calls the Ex version with some reasonable defaults.

This works fine in most cases, but if you have a lot of arguments, you either have to make many such function permutations or force the caller to pass in all arguments, even the ones they don’t care about.

**5/** @EskilSteenberg

@vkrajacic @CaptainKraft

I don't like:

void func(StructOfInputs params);

You are hiding the input, and you are forcing a memory layout. I don't even like small structs like Dim2, and Rect because they force the caller to adopt the structures of the callee. Don't force me to live in your world.

**6/** @vkrajacic

There’s no hiding of any kind, it’s a public POD struct.

The "Don’t force me to live in your world" argument can only be made for library vendors, which I’m not. This is my codebase, and I control it. Vectors and rects are abstractions with their own API functions that operate on them. Manually passing individual components is just not worth it.

If you really wanted, you could add multiple versions of functions, which I sometimes do:
RectCreate(Vec2 min, Vec2 max);
vs
RectCreate(f32 minX, f32 minY, f32 maxX, f32 maxY);

Yes, it enforces memory layout, but that’s kind of the point of structs, bundling data that gets used together. And vectors are a prime example of that, especially in games and renderers, because they act as primitives and are ubiquitous throughout the code.

**7/** @vkrajacic

@EskilSteenberg @CaptainKraft

Another example in my codebase would be length based strings. I’ve built the whole API on top of those. I don’t want to go around passing char *value, int length. The point of that abstraction is that I don’t have to do that.

**8/** @nicbarkeragain

@vkrajacic @EskilSteenberg @CaptainKraft

I don't think I could ever go back to writing C with naked arrays / strings. It's such a small cost to pass length (and capacity) around, it's so simple and makes C feel like a different language.

**9/** @daniel_collin

@nicbarkeragain @vkrajacic @EskilSteenberg @CaptainKraft

Yeah, I'm building a whole new C codebase and I'm having a String type for sure. Makes things just nicer.

**10/** @NotAttained

@EskilSteenberg @vkrajacic @CaptainKraft

What is the alternative though if it’s a big struct, do you just manually type out the parameters each time, even if they are largely the same?

**11/** @EskilSteenberg

@NotAttained @vkrajacic @CaptainKraft

YES! Having to declare a variable of the struct an then assigning every member is far more cumbersome and error prone.

**12/** @vkrajacic

It is if you're typing them all out. But the whole point of the post was about when you DON'T want to do that.
Ideally, you'd have them zero initialized or set with some default arguments, and then just override the ones you want, via designated initializer syntax.
At that point, it becomes less cumbersome and less error prone, because the defaults are already set up for you. You don’t have to write them again.
If you have lots of parameters, it's almost always the case that you don't need to set each one at the call site. If you only have a few, then a struct is unnecessary.

**13/** @vkrajacic

@EskilSteenberg @NotAttained @CaptainKraft

For instance, old win APIs often take a long list of parameters. In many cases, you only need a couple of options and pass 0 to everything else, e.g. NtQueryDirectoryFile.

![](https://pbs.twimg.com/media/GyVoVhQWcAUqchq?format=png&name=orig)

**14/** @Karyuutensei

@vkrajacic @EskilSteenberg @NotAttained @CaptainKraft

To be honest, function parameters get confusing beyond 2-3. Named parameters are much better.

## Related

- Spine: [[archive/threads/vkrajacic/2024-01-23-c-macro-approach-to-using-optional-default-named]]
