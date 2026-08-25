---
title: "[0] What a horrible term 'printf-debugging'"
type: archive
source: twitter
source_url: "https://x.com/NOTimothyLottes/status/1857803914604618029"
author: "NOTimothyLottes"
handle: NOTimothyLottes
post_id: "1857803914604618029"
date: 2024-11-16
archived: 2026-08-25
draft: false
tags:
  - archive
  - twitter
  - NOTimothyLottes
description: "[0] What a horrible term 'printf-debugging'"
in_reply_to: ""
---

## Source

- URL: https://x.com/NOTimothyLottes/status/1857803914604618029
- Author: NOTimothyLottes (@NOTimothyLottes)
- Posted: 2024-11-16 15:12:24

## Thread

**1/** **@NOTimothyLottes** ^1857803914604618029

[0] What a horrible term 'printf-debugging'
If you are debugger-free might as well at least be libc-free
Here is how I work CPU C code without any debugger in my engines, and how it works better than a debugger for me ...

Branches: [[archive/threads/NOTimothyLottes/2024-11-16-0-what-a-horrible-term-printf-debugging/2024-11-16-static_assert_0-this-is-super-cool-but-why-map-a-file-and-not]]

**2/** **@NOTimothyLottes** ^1857804669994565771

[1] First I map a '.log' file, so there is no other file IO
(a.) First half of this file (log2 sized file) contains lines of a fixed 64-character size (with the \n at the end)
(b.) Second half contains just one 32-bit atomic counter of where to write a line

Branches: [[archive/threads/NOTimothyLottes/2024-11-16-0-what-a-horrible-term-printf-debugging/2024-11-17-HerrUppoHoppa-curious-why-you-memory-map-the-32-bit-counter-to]]

**3/** **@NOTimothyLottes** ^1857805438151983120

[2] So writing a line to this log is 100% overhead-free and lock-free, one just increments the atomic counter, and dumps the comment line in the memory mapped file. Note the 64-byte line size matches a cacheline size, so no contention on the write of the line

Branches: [[archive/threads/NOTimothyLottes/2024-11-16-0-what-a-horrible-term-printf-debugging/2024-11-16-datenwolf-why-the-heck-do-you-care-about-cache-lines-if-you]]

**4/** **@NOTimothyLottes** ^1857806110687727898

[3] It's ideal for a multi-thread environment, you get correct temporal ordering captured in the log file without any real effect on the scheduling of threads.

**5/** **@NOTimothyLottes** ^1857806800663244889

[4] Lines are always in a fixed format
r|sc.milmic|line_|hex_____|0000000000-|string...
r ... reload count
sc.milmic ... time since launch (wraps)
line ... source line number (single file program)
hex ... hex print of number
000 ... decimal print of the number
string ... user msg

**6/** **@NOTimothyLottes** ^1857807155669225900

[5] I write a line with a simple function call
Tlk(__LINE__,n,"msg");
Where 'n' is the number, "msg" is a string
Don't need printf, this is way better

**7/** **@NOTimothyLottes** ^1857809793550872629

[6] Here is an example with a very simple program, just a few first lines. It's nice to automatically see exact timing. Timing since start
0.005478 sec ... mapping of the cartridge file
0.006850 sec ... page faulting the full cart file
0.008230 sec ... window creation done
etc

![](https://pbs.twimg.com/media/GchC4NwXQAAbDfS?format=png&name=orig)

**8/** **@NOTimothyLottes** ^1857812120823308592

[7] Another simple example of a fully pipelined startup, can instantly know where the primary cost is, 
"Instance begin" and "Instance end" wrap setup of the Vulkan instance, a process which took 2.4 seconds. The 4 PSOs hit in the shader cache at 3k microseconds each

![](https://pbs.twimg.com/media/GchFfI5WcAAZ_Al?format=png&name=orig)

**9/** **@NOTimothyLottes** ^1857813028349128825

[8] The log file keeps multiple runs, so it's easy to compare. Notepad2 it's F5 to reload the log file.

Branches: [[archive/threads/NOTimothyLottes/2024-11-16-0-what-a-horrible-term-printf-debugging/2024-11-16-bmcnett-so-each-line-is-63-spaces-followed-by-a-n-and]]

**10/** **@NOTimothyLottes** ^1857816126295548195

[9] The point: keep it minimal, keep it simple, and keep the number of required things that take human time to the smallest possible. If you don't fall off the 'compile-time' curve, and re-compile/re-start/re-load is 'key-press-time' this works amazingly well (interactive)
