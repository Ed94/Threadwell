---
title: "Re John @dark1x and https://youtu.be/UxquMm5Aka8?si=cmuDThfWIdoAelOh&t=4233 covering the BlurBusters CRT sim in ShaderGlass from perspective of one of the co-authors for the shader BFI technique ..."
type: archive
source: twitter
source_url: "https://x.com/NOTimothyLottes/status/1963080343952433577"
author: "NOTimothyLottes"
handle: NOTimothyLottes
post_id: "1963080343952433577"
date: 2025-09-03
archived: 2026-08-25
draft: false
tags:
  - archive
  - twitter
  - NOTimothyLottes
description: "Re John @dark1x and https://youtu.be/UxquMm5Aka8?si=cmuDThfWIdoAelOh&t=4233 covering the BlurBusters CRT sim in ShaderGlass from perspective of one of the co-authors for the shader BFI technique ..."
in_reply_to: ""
---

## Source

- URL: https://x.com/NOTimothyLottes/status/1963080343952433577
- Author: NOTimothyLottes (@NOTimothyLottes)
- Posted: 2025-09-03 03:23:20

## Thread

**1/** **@NOTimothyLottes** ^1963080343952433577

Re John @dark1x and https://youtu.be/UxquMm5Aka8?si=cmuDThfWIdoAelOh&t=4233 covering the BlurBusters CRT sim in ShaderGlass from perspective of one of the co-authors for the shader BFI technique ... thread follows

Branches: [[archive/threads/NOTimothyLottes/2025-09-03-re-john-dark1x-and-https-youtu-be-uxqumm5aka8-si/2025-09-03-idoccor-does-bfi-matter-as-much-if-you-draw-the-two-crt]]

**2/** **@NOTimothyLottes** ^1963082512323801300

(1.) One variation of the technique is to simplify from a full fractional temporal frame rate expansion to an integer one. Meaning scale frame rate by {2x,3x,4x,etc}. BF2 https://www.shadertoy.com/view/l3tyRX is an example of a fixed 2x scalar. MIT ready for any dev to directly integrate.

![](https://pbs.twimg.com/media/Gz5FAiJWMAAvaoR?format=jpg&name=orig)

**3/** **@NOTimothyLottes** ^1963083235849867295

(2.) That BF2 supports a rolling frame as required for anti-static build up for LCDs. The actual in-game overheads for direct integration are minor
(a.) Write 2 swap targets during the last post pass
(b.) Use a simple inline function (small ALU)
(c.) Present both frames

**4/** **@NOTimothyLottes** ^1963083770275234221

(3.) So overheads in say a capture overlay tool like ShaderGlass wouldn't be what you would see in a direct integration. But you'd still need to be hitting v-sync in the game (for say integer temporal scaling).

**5/** **@NOTimothyLottes** ^1963084702471893289

(4.) Another option for direct in-game integration is full fractional frame rate temporal scaling. RBF is an MIT example of that: https://www.shadertoy.com/view/MXdyzS - similar to Mark's variation of the CRT beam sim with some changes (cleaner in the rolling transition, less 'graying')

![](https://pbs.twimg.com/media/Gz5GvFnWQAAB6JR?format=jpg&name=orig)

**6/** **@NOTimothyLottes** ^1963085923769352350

(5.) Something like RBF with the full fractional temporal expansion requires a bit more effort to integrate. It uses an extra full resolution feedback image acting an energy reservoir for energy redistribution across time.

![](https://pbs.twimg.com/media/Gz5H1LMWwAAU-9A?format=png&name=orig)

**7/** **@NOTimothyLottes** ^1963087284481212925

(6.) Of course one can mix CRT-like spatial scaling with the software BFI in multiple ways. Using both spatial and temporal energy redistribution. Example here mixing BDM and BF2 for 4x area spatial scaling and 2x temporal (8x area total): https://www.shadertoy.com/view/43VyRw

![](https://pbs.twimg.com/media/Gz5JE8hWoAAMECY?format=jpg&name=orig)

**8/** **@NOTimothyLottes** ^1963087705912352898

(7.) It is interesting to hear John's suggestion of using it at 60 Hz render rate. I was assuming maybe that would be too much visible flicker for people, but the rolling scan of the CRT sim certainly helps make it a lot better than in-monitor square-wave BFI.

**9/** **@NOTimothyLottes** ^1963088570475860228

(8.) Think the true power of mixing the spatial CRT and temporal BFI together to do fantasy display simulation is that games could instead reconfigure the display based on how many pixels the game can push, instead of say using more expensive stuff (scaling TAAs, framegen).

**10/** **@NOTimothyLottes** ^1963090107432333823

(9.) Also if anyone wants to use this stuff, feel free to contact me directly. It would be quite nice to get this stuff showcased in a real game. There is a bit more to making the experience good that is fully covered in say the shadertoy examples (like LCD vs OLED stuff)

**11/** **@NOTimothyLottes** ^1963090718597251329

(10.) Good example of this is DBM which is designed for LCD RGB triads, but could use perhaps a different variation for WOLED and QD-OLED. I've got some talk presentations on this stuff which I've been a little slow to get on youtube.

![](https://pbs.twimg.com/media/Gz5MVTgWAAUOsDL?format=jpg&name=orig)
