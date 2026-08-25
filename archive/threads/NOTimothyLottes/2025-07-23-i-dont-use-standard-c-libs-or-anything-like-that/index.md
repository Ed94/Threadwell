---
title: "\"nobody self includes with defines to reorder C code\" ..."
type: archive
source: twitter
source_url: "https://x.com/NOTimothyLottes/status/1947848281280631267"
author: "NOTimothyLottes"
handle: NOTimothyLottes
post_id: "1947848281280631267"
date: 2025-07-23
archived: 2026-08-24
draft: false
tags:
  - archive
  - twitter
  - NOTimothyLottes
description: "\"nobody self includes with defines to reorder C code\" ..."
in_reply_to: ""
---

## Source

- URL: https://x.com/NOTimothyLottes/status/1947848281280631267
- Author: NOTimothyLottes (@NOTimothyLottes)
- Posted: 2025-07-23 02:36:34

## Thread

**1/**

"nobody self includes with defines to reorder C code" ... Haha, apparently I'm not the only one, the File Pilot guy does it too :)

![](https://pbs.twimg.com/media/GwgkzCMWsAAnfS7?format=png&name=orig)

**2/**

@NOTimothyLottes Do you also automatically generate the include files or do you just write them yourself?

**3/**

@Karyuutensei I only include __FILE__ (self). For WIN32 and VK even, I recreate the parts of external headers I need (use) inside the 'one source file', typically with structural type changes to switch back to simple types like 64 bit intergers instead of pointers. Trying to get to C--

**4/**

@Karyuutensei One side effect, even with C code the compilation is perceptually instant for the whole program. The other thing I do is mix the GLSL and C all in the same file, so I share defines. I do have one external include for the compiled SPIR-V ...

**5/**

@Karyuutensei For the SPIR-V, I also have one program, but I use specialization constants set at PSO generation to select the code path for a specific 'shader'.  This requires spriv opt as a pre-processor else the IHV compilers tend to be 10x or more slower.

**6/**

@Karyuutensei During dev time I use 2 terminals each with their own shell scripts. The first is to just loop and keep regenerating the SPIR-V if anything in the 'one file' changes. This is unfortunately a mess to do in a batch file (below)

![](https://pbs.twimg.com/media/Gwi1pOOW4AEZDE5?format=png&name=orig)

**7/**

@Karyuutensei The second does the same for the C program, loops recompiling and running the program. So when I'm editing source I can just fast exit the program and it restarts [with instant restart/reload it is quite fast to restart]

![](https://pbs.twimg.com/media/Gwi23Q9WMAI4Grm?format=png&name=orig)

**8/**

@Karyuutensei I'm using GCC on Windows, because why bother with having to install Visual Studio or it's compiler tool chain mess. I just do MINGW64 and be done with it. My debugger is the instant restart for C code, and shader reload for GLSL

**9/**

@Karyuutensei I don't use standard C libs or anything like that. I just write my own stuff. For 'printf' style debugging I have macros that write to a memory mapped log file. They give {[restartNumber]|[msSinceLaunch]|[sourceLine]|[hex]|[dec]|[comment]}. Keeping multiple restarts in same log

![](https://pbs.twimg.com/media/Gwi4H27WgAAIgMN?format=png&name=orig)

**10/**

@Karyuutensei That log example is a simple test program, it starts in 0.3 ms for that run. The log tells all about how it pipelines start up {doing memory page warming, kart load, window setup, VK setup in parallel, getting to PSO gen as fast as possible [get layout done first]}

![](https://pbs.twimg.com/media/Gwi47owXQAEa2Ar?format=png&name=orig)
