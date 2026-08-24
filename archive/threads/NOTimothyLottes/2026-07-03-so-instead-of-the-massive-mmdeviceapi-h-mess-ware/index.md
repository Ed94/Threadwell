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

Media (not lifted): `2073110092447203466_HMUqNm_XIAA0JEP_orig.png`

**2/**

Here is initial bring up, function call by function call. No headers, and no C++. The magic of typecasting at usage IC4_(CPP_(... is that I don't ever have to build the headers. That is at least working out well. I do line by line to test in Wine, defer fail handling until later

Media (not lifted): `2073111326981783629_HMUrDz2XsAA9JLP_orig.png`

**3/**

More on bring-up. I just run and check visually for output in the console (this time 'B055'). Since compile times are under a second, it is super fast to check as I go. Easy to see how much code bloat there is for C++ this way (doing it manually).

Media (not lifted): `2073113441959616958_HMUs9oLWUAAaHx9_orig.png`

**4/**

Example below of how much header bloat I'm factoring out using my simple macros

Media (not lifted): `2073114409270997497_HMUujnwWoAAUQd1_orig.png`
