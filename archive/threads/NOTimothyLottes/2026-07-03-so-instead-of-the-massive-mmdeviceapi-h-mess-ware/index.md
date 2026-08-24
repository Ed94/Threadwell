---
title: "So instead of the massive \"mmdeviceapi.h\" mess-ware, I defined a stupid CPP_(object,virtual_function_number) macro."
type: archive
source: twitter
source_url: "https://x.com/NOTimothyLottes/status/2073110092447203466"
author: "NOTimothyLottes"
handle: NOTimothyLottes
post_id: "2073110092447203466"
date: 2026-07-03
archived: 2026-08-23
draft: true
tags:
  - archive
  - twitter
  - NOTimothyLottes
description: "So instead of the massive \"mmdeviceapi.h\" mess-ware, I defined a stupid CPP_(object,virtual_function_number) macro."
in_reply_to: ""
---

## Source

- URL: https://x.com/NOTimothyLottes/status/2073110092447203466
- Author: NOTimothyLottes (@NOTimothyLottes)
- Posted: 2026-07-03 18:22:17

## Thread

**1/**

So instead of the massive "mmdeviceapi.h" mess-ware, I defined a stupid CPP_(object,virtual_function_number) macro. This way I just have to write down the index in the VT table for the specific virtual function ...

![](https://pbs.twimg.com/media/HMUqNm_XIAA0JEP?format=png&name=orig)
**2/**

Here is initial bring up, function call by function call. No headers, and no C++. The magic of typecasting at usage IC4_(CPP_(... is that I don't ever have to build the headers. That is at least working out well. I do line by line to test in Wine, defer fail handling until later

![](https://pbs.twimg.com/media/HMUrDz2XsAA9JLP?format=png&name=orig)
**3/**

More on bring-up. I just run and check visually for output in the console (this time 'B055'). Since compile times are under a second, it is super fast to check as I go. Easy to see how much code bloat there is for C++ this way (doing it manually).

![](https://pbs.twimg.com/media/HMUs9oLWUAAaHx9?format=png&name=orig)
**4/**

Example below of how much header bloat I'm factoring out using my simple macros

![](https://pbs.twimg.com/media/HMUujnwWoAAUQd1?format=png&name=orig)