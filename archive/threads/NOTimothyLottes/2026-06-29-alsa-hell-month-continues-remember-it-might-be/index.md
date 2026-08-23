---
title: "ALSA hell month continues: remember it might be \"open source\" but it is definitely \"closed documentation\" [those docs are securely trapped in the minds of the authors]."
type: archive
source: twitter
source_url: "https://x.com/NOTimothyLottes/status/2071706805114216559"
author: "NOTimothyLottes"
handle: NOTimothyLottes
post_id: "2071706805114216559"
date: 2026-06-29
archived: 2026-08-23
status: draft
draft: true
tags:
  - archive
  - twitter
  - NOTimothyLottes
description: "ALSA hell month continues: remember it might be \"open source\" but it is definitely \"closed documentation\" [those docs are securely trapped in the minds of the authors]."
in_reply_to: ""
---

## Source

- URL: https://x.com/NOTimothyLottes/status/2071706805114216559
- Author: NOTimothyLottes (@NOTimothyLottes)
- Posted: 2026-06-29 21:26:07

## Thread

**1/**

ALSA hell month continues: remember it might be "open source" but it is definitely "closed documentation" [those docs are securely trapped in the minds of the authors]. Now that I have aplay playing a sound, it's time for garbage sifting through STRACE to see what is going on ...

Media (not lifted): `2071706805114216559_HMAt1GiXAAAoahX_orig.png`

Branches: [[2026-06-29-AlexABPerson-have-you-actually-reached-out-to-said-developers]]

**2/**

For devs working on linux, strace is a good friend, besides reverse engineering undocumented crap, it's useful to run on your own app as a bug test, like look what this idiot [me] did with nanosleep()

Media (not lifted): `2071710958397898929_HMAx0PmW0AAdUAy_orig.png`

**3/**

In my ALSA interface I war-dial the possible /dev/snd/pcm devices instead of just listing the directory. It's a lot easier in source code.

Media (not lifted): `2071714384225681440_HMA1CA9XIAAwRAB_orig.png`

**4/**

Using 'strace' showed another bug in my setting schedule priority code (I didn't yet validate that code and check for errors). Definitely my ALSA test app shows ZERO errors in ALSA system calls, but doesn't actually play anything. Broken without errors = crappy API.

Media (not lifted): `2071715941688258752_HMA2LibWMAAMW3O_orig.png`

**5/**

In theory a good API, SNDRV_PCM_IOCTL_PREPARE would fail if the next SNDRV_PCM_IOCTL_WRITEI_FRAMES wouldn't accept the write. And that WRITEI should also fail instead of pass and setting .result=0 (of the snd xferi structure).

**6/**

The best I can guess thus far is that the aplay app goes through some HW_REFINE ioctls before setting the HW_PARAMS, and perhaps the "magic missing thing" is in that process.

Media (not lifted): `2071717187623030935_HMA3sGVXwAAVDMT_orig.png`

**7/**

Best docs on REFINE that I've found yet is indirectly through this. Note tinyalsa doesn't seem to use this interface other than through pcm_params_get(), not the interative process seen in aplay strace. Maybe because tinyalsa is for android (different drivers)

Media (not lifted): `2071725181576319370_HMA-CDAXEAAw9ns_orig.jpg`

**8/**

SNDRV_PCM_IOCTL_HW_REFINE
If send out a zeroed snd_pcm_hw_params, the ioctl will fail. There is a special magic sauce to the structure that must be initialized correctly before you can even fetch hardware parameters. It's high level skill in Obfuscation. See *_any( in ALSA src

Media (not lifted): `2071759816725311959_HMBePMXXwAE5_1M_orig.png`

**9/**

magiz/
clear snd_pcm_hw_params
set masks[0 ... 2].bits[0]=~0
set intervals[0 ... 11].max=~0
set rmask=~0
set info=~0

**10/**

The rmask and cmask use bit indexed by the DEFINE so 
1<<SNDRV_PCM_HW_PARAM_{thing}

**11/**

Hats off to Abramo Bagnara of the ALSA project for the worst kernel system interface I have ever used in my life. This refinement required just to configure an audio device is a master class on the worst way to do something. And still have a few hours left in reverse engineering
