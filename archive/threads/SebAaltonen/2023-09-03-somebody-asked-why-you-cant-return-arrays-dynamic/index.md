---
title: "Somebody asked why you can't return arrays (dynamic sized data) in C."
type: archive
source: twitter
source_url: "https://x.com/SebAaltonen/status/1698349154106274129"
author: "Sebastian Aaltonen"
handle: SebAaltonen
post_id: "1698349154106274129"
date: 2023-09-03
archived: 2026-08-27
draft: false
tags:
  - archive
  - twitter
  - SebAaltonen
description: "Somebody asked why you can't return arrays (dynamic sized data) in C."
in_reply_to: ""
---

## Source

- URL: https://x.com/SebAaltonen/status/1698349154106274129
- Author: Sebastian Aaltonen (@SebAaltonen)
- Posted: 2023-09-03 14:56:06

## Thread

**1/** **@SebAaltonen** ^1698349154106274129

Somebody asked why you can't return arrays (dynamic sized data) in C. There's a interesting technical limitation in stack based programming languages that prevents this. It's not possible to return dynamic amount of data using the stack.

Thread...

**2/** **@SebAaltonen** ^1698349426559893546

We all know that alloca exists. This allows you to allocate dynamic amount of data from top of the stack. This works like any static sized stack variable. It dies at return. No issues there. Why is the return then a problem?

**3/** **@SebAaltonen** ^1698349835110277381

The problem is that when you call functions, those functions go on stack on top of you. The stack will be rewinded at function return, so if you want to have storage for return value, you have to allocate it in the caller scope before the function call.

**4/** **@SebAaltonen** ^1698350535290609828

The problem is that the caller doesn't know how many bytes the called function wants to return. That function must run first. And that function's stack variables are on top of the caller's variables. Dynamic sized stack allocations must always be on top of the stack.

**5/** **@SebAaltonen** ^1698351276117901624

What if the called function could immediately call alloca before allocating local variables from the stack? That would actually work. The problem is that that function would need to calculate the return value size without using any temporary variables in the stack. Not easy!

**6/** **@SebAaltonen** ^1698351905229947197

There's no generic way to put a dynamic sized return value to the top of the stack in a way that it remains on top of the stack after the function has returned. That would be equal to alloca and would work, but it's not doable in most situations.

**7/** **@SebAaltonen** ^1698352650775847179

You could also think about reading the return value beyond the stack scope after function has returned with dynamic return size. This works only in case you don't call any other functions, since those would override the return value.

**8/** **@SebAaltonen** ^1698353875978178598

There's a way to make dynamic sized stack return work. You know how the top of the stack of the returned function and you alloca(N) where N is enough to cover that function. Now the dynamic return is safe to access. But you waste extra stack space equal to variables of that func.

**9/** **@SebAaltonen** ^1698354683096563868

The above works for multiple functions too, it's simply equal to calling alloca multiple times inside the same function. The problem of this kind of deferred stack popping is that it continues recursively if the called functions also receive some dynamic sized return values.

**10/** **@SebAaltonen** ^1698355711422476302

I don't know whether any languages have implement this kind of deferred stack popping for dynamic return values. It wastes a lot of stack space if dynamic size return is common, especially in deep chains. But it should never be worse than linear temp allocator.

Branches: [[archive/threads/SebAaltonen/2023-09-03-somebody-asked-why-you-cant-return-arrays-dynamic/2023-09-03-SergeyLerg-i-like-how-jai-solved-this-you-can-return]], [[archive/threads/SebAaltonen/2023-09-03-somebody-asked-why-you-cant-return-arrays-dynamic/2023-09-03-RepealTCPA1947-you-might-be-interested-in-https-2022-ecoop-org]], [[archive/threads/SebAaltonen/2023-09-03-somebody-asked-why-you-cant-return-arrays-dynamic/2023-09-03-_Glacia-ada-does-this]], [[archive/threads/SebAaltonen/2023-09-03-somebody-asked-why-you-cant-return-arrays-dynamic/2023-09-04-iiSatana-what-if-we-had-some-kind-of-special-syntax-sugar]], [[archive/threads/SebAaltonen/2023-09-03-somebody-asked-why-you-cant-return-arrays-dynamic/2023-09-04-DasGurke-unroll]]
