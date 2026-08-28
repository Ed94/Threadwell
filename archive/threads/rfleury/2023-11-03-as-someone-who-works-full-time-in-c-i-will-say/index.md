---
title: "@Madisonkanna As someone who works full-time in C, I will say that a lot of the traditional educational material around learning C is not very good, because it was made in such a different hardware landscape."
type: archive
source: twitter
source_url: "https://x.com/rfleury/status/1720480382905385130"
author: "Ryan Fleury"
handle: rfleury
post_id: "1720480382905385130"
date: 2023-11-03
archived: 2026-08-27
draft: false
tags:
  - archive
  - twitter
  - rfleury
description: "@Madisonkanna As someone who works full-time in C, I will say that a lot of the traditional educational material around learning C is not very good, because it was made in such a different hardware landscape."
in_reply_to: "1720453068553351643"
---

## Source

- URL: https://x.com/rfleury/status/1720480382905385130
- Author: Ryan Fleury (@rfleury)
- Posted: 2023-11-03 16:37:42

## Thread

**1/** **@rfleury** ^1720480382905385130

**@Madisonkanna**

As someone who works full-time in C, I will say that a lot of the traditional educational material around learning C is not very good, because it was made in such a different hardware landscape. Programming in C today is so different (and better) than how it’s normally taught.

**2/** **@0xclodagh** ^1720481474669924818

**@rfleury** **@Madisonkanna**

so what would someone in her position do to learn C in today's landscape

**3/** **@rfleury** ^1720482349958463960

**@0xclodagh** **@Madisonkanna**

Handmade Hero remains the most transformative programming educational experience in my life. I recommend anyone interested in C to go follow the first 30 or so episodes. You will learn more than in several years of college education.

**4/** **@zeRusski** ^1720492435413876954

**@rfleury** **@0xclodagh** **@Madisonkanna**

I’m willing to believe that but it is muddled in Win trivia n setup and IIRC says nothing about handling e.g. strings - stuff Python et al hides from u but C learning resources say nothing about. K&R is all \0 and UTF8 oblivious

**5/** **@rfleury** ^1720493339303379256

**@zeRusski** **@0xclodagh** **@Madisonkanna**

K&R is exactly what I mean when I say the traditional resources are extremely out of date and not good. Strings in C are easy with the right setup. I don’t have a blog on strings yet—the short answer is “never null-terminate, use immutable slices everywhere”—but I have a post…

**6/** **@zeRusski** ^1720493902753313188

**@rfleury** **@0xclodagh** **@Madisonkanna**

Right, at which point u realize .. oh wait I haven’t even the basic functions to work with strings and most prople would get stuck n give up

**7/** **@rfleury** ^1720494624668840209

**@zeRusski** **@0xclodagh** **@Madisonkanna**

Yes I agree, the CRT & out-of-the-box code you get with a C compiler is terrible. But that’s a descriptor of the ecosystem, not the language. This is why one aim of my codebase is to provide a better C “standard” library. Just look at something like Raylib as an open example.

**8/** **@pATjako** ^1720739266043515068

**@rfleury** **@zeRusski** **@0xclodagh** **@Madisonkanna**

The toolkit that C itself provides is barren and often it is even bad. With my own base lib, I have the same goal. But these are no good fits for a single header library or really any kind of shared code that is used outside of your own codebase.
