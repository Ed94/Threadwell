---
title: "Following the succession (thanks) of re-trying WASAPI using this example which has been pre-minimized and de-C++'ed: https://gist.github.com/mmozeiko/5a5b168e61aff4c1eaec0381da62808f#file-win32_wasapi-h - But I'm missing something on how to get the C++ as C linking to function (cross compiling), doesn't easily work out of the box."
type: archive
source: twitter
source_url: "https://x.com/NOTimothyLottes/status/2073096069529907441"
author: "NOTimothyLottes"
handle: NOTimothyLottes
post_id: "2073096069529907441"
date: 2026-07-03
archived: 2026-08-23
draft: false
tags:
  - archive
  - twitter
  - NOTimothyLottes
description: "Following the succession (thanks) of re-trying WASAPI using this example which has been pre-minimized and de-C++'ed: https://gist.github.com/mmozeiko/5a5b168e61aff4c1eaec0381da62808f#file-win32_wasapi-h - But I'm missing something on how to get the C++ as C linking to function (cross compiling), doesn't easily work out of the box."
in_reply_to: ""
---

## Source

- URL: https://x.com/NOTimothyLottes/status/2073096069529907441
- Author: NOTimothyLottes (@NOTimothyLottes)
- Posted: 2026-07-03 17:26:33

## Thread

**1/**

Following the succession (thanks) of re-trying WASAPI using this example which has been pre-minimized and de-C++'ed: https://gist.github.com/mmozeiko/5a5b168e61aff4c1eaec0381da62808f#file-win32_wasapi-h - But I'm missing something on how to get the C++ as C linking to function (cross compiling), doesn't easily work out of the box.

![](https://pbs.twimg.com/media/HMUdajFXEAAiaQE?format=png&name=orig)
**2/**

Of course I'm missing the magic header that does the real work ... curious how messy this will get

![](https://pbs.twimg.com/media/HMUgZcyWQAA263a?format=jpg&name=orig)
**3/**

So instead of the massive "mmdeviceapi.h" mess-ware, I defined a stupid CPP_(object,virtual_function_number) macro. This way I just have to write down the index in the VT table for the specific virtual function ...

![](https://pbs.twimg.com/media/HMUqNm_XIAA0JEP?format=png&name=orig)
**4/**

Here is initial bring up, function call by function call. No headers, and no C++. The magic of typecasting at usage IC4_(CPP_(... is that I don't ever have to build the headers. That is at least working out well. I do line by line to test in Wine, defer fail handling until later

![](https://pbs.twimg.com/media/HMUrDz2XsAA9JLP?format=png&name=orig)
**5/**

More on bring-up. I just run and check visually for output in the console (this time 'B055'). Since compile times are under a second, it is super fast to check as I go. Easy to see how much code bloat there is for C++ this way (doing it manually).

![](https://pbs.twimg.com/media/HMUs9oLWUAAaHx9?format=png&name=orig)
**6/**

Example below of how much header bloat I'm factoring out using my simple macros

![](https://pbs.twimg.com/media/HMUujnwWoAAUQd1?format=png&name=orig)