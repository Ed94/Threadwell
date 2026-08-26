---
title: "@NOTimothyLottes You could maybe use a D3D9 swapchain to query this information..."
type: archive
source: twitter
source_url: "https://x.com/misyltoad/status/1739762141740065225"
author: "autumn"
handle: misyltoad
post_id: "1739762141740065225"
date: 2023-12-26
archived: 2026-08-26
draft: false
tags:
  - archive
  - twitter
  - NOTimothyLottes
description: "@NOTimothyLottes You could maybe use a D3D9 swapchain to query this information..."
in_reply_to: ""
parent_post_id: "1739759522401374467"
---

## Source

- URL: https://x.com/misyltoad/status/1739762141740065225
- Author: autumn (@misyltoad)
- Posted: 2023-12-26 21:36:32

## Branch

**1/** **@misyltoad** ^1739762141740065225

**@NOTimothyLottes**

You could maybe use a D3D9 swapchain to query this information... Not sure if this is emulated these days or if its backed by D3DKMT.

https://learn.microsoft.com/en-us/windows/win32/api/d3d9/nf-d3d9-idirect3dswapchain9-getrasterstatus

**2/** **@NOTimothyLottes** ^1739762925022142966

**@phys_ballsocket**

I've been going from this example (roughly): https://github.com/blurbusters/vsync_blurbusters/blob/main/platform_vsync_windows.cpp ... but definitely venturing into hard for Linux to emulate land

**3/** **@misyltoad** ^1739764028518322545

**@NOTimothyLottes**

s/hard/impossible

**4/** **@misyltoad** ^1739765008781750630

**@NOTimothyLottes**

And probably not worth it for front buffer vs double buffer rendering to save the .7ms present slop Gamescope has 🐸

**5/** **@NOTimothyLottes** ^1739765615663996963

**@phys_ballsocket**

It's not just about latency, it's also about having the GPU-side workload adapt to changing power state ... work until close to vsync (shade to object space) then start doing the rendering just in time :)

**6/** **@NOTimothyLottes** ^1739766833891144004

**@phys_ballsocket**

BTW, I think you'd get some memory savings on Linux by emulating standard 2-deep windows swap (for v-sync). Workaround via: alloc just 2 physical images in memory, but still use 4 or more separate logical images for swap each that alias the same 2 physical allocations.

**7/** **@NOTimothyLottes** ^1739767238381486387

**@phys_ballsocket**

... For front buffer on my Deck driver I did 8 or more images all with the same physical address. Then the latency problem of getting image done ack doesn't matter. Should work great with fixed {even, odd} pattern for double buffering too.

**8/** **@misyltoad** ^1739768088248148013

**@NOTimothyLottes**

You shouldn't need more than 4 images for perfectly consistent no-waiting forward progress with mailbox/immediate -- which is also the minimum.

**9/** **@misyltoad** ^1739767788477005960

**@NOTimothyLottes**

Oh trust me there are bigger memory savings on the table... DXVK and VKD3D-Proton already have this logical split but in another way: they just copy images :D
I seem to remember there are quirks of DX vs VK swapchains and recreation that make this hard to reconscile.

**10/** **@BlurBusters** ^1740159325912662324

**@phys_ballsocket** **@NOTimothyLottes**

At 4K scrolling at 3840 pixels/sec, a 0.7ms stutter = about 3 pixeljump error.  So 0.7ms = motion quality problem too, not just latency problem, when considering extreme resolutions at extreme motion clarity (< 0.7ms MPRT, from Hz or from strobe). Problem in VR

**11/** **@BlurBusters** ^1740159762342572251

**@phys_ballsocket** **@NOTimothyLottes**

Also, don't forget power management stutters. If you pause rendering for more than ~2ms, the GPU usually goes to sleep that takes 0.5ms-1ms to wake (0.7ms slop?). You can remove slop by dummy-rendering stuff ~2ms prior to real render, then begin your time-critical real-render.

**12/** **@misyltoad** ^1740164370595012766

**@BlurBusters** **@NOTimothyLottes**

On Steam Deck we don't have that problem (99%) because we use hardware scan-out for everything.

Unless you have FSR/NIS/Bandlimited Pixel Filter enabled at the compositor level, you are always going to be using hardware planes for game + Steam Overlay + Perf Overlay 1/2

**13/** **@misyltoad** ^1740164726812987648

**@BlurBusters** **@NOTimothyLottes**

This doesn't have a cost to wake up and start doing work like shader-based composition and is also much more power efficient.

I am so very grateful that we have full color management (Shaper + 3D LUT, etc) support at scanout time for every plane on the APU :)

**14/** **@NOTimothyLottes** ^1740180471936598056

**@phys_ballsocket** **@BlurBusters**

Big area tax, rather have the CUs instead personally. Bunch of post needs to be post-tonemap-linear (as in what the human sees) to be done correctly {localized tonemapping, sharpening, grain, etc}. One would have to invert whatever that HW is doing (2x the cost) to workaround

**15/** **@misyltoad** ^1740183731011567756

**@NOTimothyLottes** **@BlurBusters**

To be clear I am talking about from the compositor side -- and I would absolutely not like the CUs. Composition sucks, takes more power and requires much more slop/redzone adding latency.

**16/** **@misyltoad** ^1740184394516881420

**@NOTimothyLottes** **@BlurBusters**

We do a lot of things like PQ->Gamma 2.2, smooth gamut mapping, night light, handling scRGB, etc in the scanout hardware. It's actually great.

**17/** **@NOTimothyLottes** ^1740186603245687084

**@phys_ballsocket** **@BlurBusters**

PQ/scRGB/etc -> just engineered complexity: 10:10:10:2 gamma 2 with a trivial in-shader temporal dither provides more than enough precision for any display that will exist in a few hundred years.

**18/** **@misyltoad** ^1740187782218498522

**@NOTimothyLottes** **@BlurBusters**

It is not engineered complexity when you have content that is not necessarily for your screen, eg. random video/images.

The complexity is fine anyway -- it's just a LUT from one to the other, something we already need for other fx + blending

**19/** **@NOTimothyLottes** ^1740190015811109117

**@phys_ballsocket** **@BlurBusters**

Some day I'll have to do this topic justice, but twitter is way too limited for that. One very important point though: global operations are too limited for good color processing, the future is localized and done pre-shader-temporal-scale. HDR standards did it wrong too.

**20/** **@BlurBusters** ^1740232888057270666

**@NOTimothyLottes** **@phys_ballsocket**

While HDR is fantastic, it is indeed difficult to zero-latency beamrace some HDR processing "on the scanout fly" because need to buffer whole refresh cycle for some algos (brightest pixels used, ABL processing, dynamic tonemapping, sync between FALD scanout + panel scanout, etc)

**21/** **@NOTimothyLottes** ^1740233890068148514

**@BlurBusters** **@phys_ballsocket**

Ideally you'd get native panel brightness and gamut without any 'HDR' mode, with standard 10-bit/channel {sRGB, or gamma 2.2, or even better gamma 2.0 (faster on shader logic)}, and with no display side tonemapping. Don't need the rest of 'HDR' market logic

**22/** **@BlurBusters** ^1740234250216157436

**@NOTimothyLottes** **@phys_ballsocket**

It would be funny if we just end up using brute Hz (1000fps 1000Hz) to just naturally solve this by permitting global buffered processing within 1ms, via "strobeless motion blur reduction" via 10:1 reprojection http://blurbusters.com/framegen

**23/** **@NOTimothyLottes** ^1740235338776514899

**@BlurBusters** **@phys_ballsocket**

The real problem is lack of temporally linear response I think. Mitigation of that in shader software would be panel specific. So rather have good OEM BFI than high-rate across the board. High-rate has associated HW expense too.

**24/** **@BlurBusters** ^1740236119244169648

**@NOTimothyLottes** **@phys_ballsocket**

I adore BFI; it's BLUR busters DNA. But major problem is unable to five-sigma display comfort with BFI as BFI is flicker/PWM. A not-insignificant percentage of humankind get eyestrain from BFI/PWM/strobe. Eyes designed for real life with no framerate & no flicker.

**25/** **@BlurBusters** ^1740236956032999817

**@NOTimothyLottes** **@phys_ballsocket**

BFI is a great bandaid for now, especially for retro content. Longterm, there's appears an engineering path low-wattage 10:1 reprojection even within our slowed Moore's Law. Although it may not be till 2030s for standalone strobeless blurless mobile displays though.

**26/** **@BlurBusters** ^1740238378648691156

**@NOTimothyLottes** **@phys_ballsocket**

We successfully tested 10:1 reprojection on very old GPUs (GTX 1080 Ti), when testing on RTX 4090 it used only 10% GPU to do 10:1. We calculated future transistor/wattage requirements, and it's looking promising. Key is "Developer Best Practices" at https://blurbusters.com/framegen#dev

**27/** **@NOTimothyLottes** ^1740243378804269178

**@BlurBusters** **@phys_ballsocket**

Elephant of perceptual frame interpolation artifacts isn't solved by any means, and it comes with the latency tax. It's walking the wrong direction. The solution isn't the current screen-space pixel shaded games with temporal scaling and frame interpolation ...

**28/** **@NOTimothyLottes** ^1740244510867862008

**@BlurBusters** **@phys_ballsocket**

Amortized object space shading, with simple frame render at the display rate. Improves latency and scales by frame rate. Can already target the 360Hz displays with v-sync on with that tech, and don't need the 4090 to do it.

**29/** **@BlurBusters** ^1740244830171869351

**@NOTimothyLottes** **@phys_ballsocket**

Tomorrow, we won't need a 4090.  I only simply mention 4090 only to demonstrate that technology already exists to do 4K 1000fps path-traced graphics -- if Unreal Engine, for example, adds lagless 10:1 reprojection with between-frame inputread support.

**30/** **@BlurBusters** ^1740245671414796385

Reprojection is a game of pick-poisons that have extreme artifacts like MPEG1 today. But tomorrow's framegen will be perceptually lagless and lossless much like H.EVC (H.265) or H.VVC (H.266), both of which have interpolation mathematics built into the codec... Reprojection becomes less and less blackbox than blind-blackbox-in-middle interpolation like TVs.

![](https://pbs.twimg.com/media/GCaX-fQXsAApRRb?format=png&name=orig)

**31/** **@BlurBusters** ^1740246523244384708

I hate interpolation. But bear with me. Metaphorically  MPEG1 vs H.VVC tech in framegen upgrade!! GIANT diff in framegen quality & lag. Even today, we compromise by metaphorically (defacto) fakeframing representing real world via triangles/textures, then reducing rez & settings (=artifacts) to get more frames/sec.

**32/** **@BlurBusters** ^1740246786626003283

**@NOTimothyLottes** **@phys_ballsocket**

We are now witnessing, in the laboratory newer framegen that has perceptually fewer drawbacks (esports-ready framegen with less artifacts than the current game-settings fiddling we do today).  The future is coming within 10 years, the GPU/API vendors are a bit behind.

**33/** **@NOTimothyLottes** ^1740246923217617263

**@BlurBusters** **@phys_ballsocket**

With some exceptions like idTech, current AAA gfx tech trend is lower res and lower FPS. Gfx devs are eating more than all process advantages simply in the quest for realism, there won't be budget left for 1000hz, because non-BFI motion clarity isn't a dev priority.

**34/** **@BlurBusters** ^1740247204399628391

**@NOTimothyLottes** **@phys_ballsocket**

Correct. And we're spending lots behind the scenes to slowly change that. We started 10 years under different goals, and the next 10 years is this Blur Busters Master Plan. Working with many researchers! Fruits won't show for a while.

**35/** **@BlurBusters** ^1740247816050524283

There's a lot of valid approaches today, and BFI is definitely one of them.  BFI will never become obsolete.  And mobile/phone gaming will never become obsolete. However, several parties are actually working to produce proper demos long-term. Even grandma sees 240-vs-1000 OLED (VHS-vs-8K 'geometrics' effect) more clearly than 60-vs-120 LCD (720p-vs-1080p minor difference effect)

**36/** **@BlurBusters** ^1740248121500971435

**@NOTimothyLottes** **@phys_ballsocket**

There's a pretty big research rabbit hole involved, but we're the figurative equivalent of 1980s Japanese HDTV researchers.  4K was a $10K luxury in 2001 with the IBM T-221.

**37/** **@NOTimothyLottes** ^1740250610044486099

**@BlurBusters** **@phys_ballsocket**

Important to keep in mind, it's selective motion clarity that holds importance. Gaming content still needs runtime controlled tools like blur to break a fall into the uncanny valley. Uniform temporal interpolation won't fix that, it will make it worse.

**38/** **@NOTimothyLottes** ^1740251653918568576

**@BlurBusters** **@phys_ballsocket**

... Offline (effectively infinite cost) uniform temporal frame interpolation for 24 Hz film, often just makes it clear that a bunch of actors who don't know how to fight are not actually hitting each other. ...

**39/** **@BlurBusters** ^1740252171956785452

I enjoy my movies in Hollywood Filmmaker Mode, as a 24fps purist. Go Big or Go Home. For me, sample & hold 48-120 HFR is more nauseating than 24fps Hollywood or 1000fps UltraHFR, or just going 24fps Hollywood. But I'm not everyone; Even some of our audience even gets benefit from more motion blur, indeed. Switching display refresh rate to 24fps, which has an effect similar to iPhones' "Reduce Motion" accessibility setting. It solved a portion of our audience's display nausea/motionsick. I still acknowledge that. But it's just a Lowest Common Denominator when it comes to interactive content, when ultra high frame rate for *immersive* gaming, is much more ergonomic.

**40/** **@BlurBusters** ^1740252545036005406

At the end of the day, getting 1000fps with minimum possible GPU is a large reason why we're GPU-shaming the big GPU vendors (AMD, NVIDIA) that there are lagless & artifactless bigger-ratio ways that are simpler than what they're doing. Even LTT GPU-shamed too: https://www.youtube.com/watch?v=IvqrlgKuowE

**41/** **@BlurBusters** ^1740253162655683012

The key of my GPU-vendor-shaming is that absurdly simple minor modifications to reprojection solved >99% of reprojection artifacts:
(A) Sample and hold only (avoids double images)
(B) Starting pre-reprojection framerate above flicker fusion;
(C) Large reprojection ratios that produce mainstream visible benfits like 1/100sec camera exposure versus 1/1000sec camera exposure (10x blur differentials; geometrics for the win)... WHILE doing it on a display that doesn't throttle GtG (240-vs-360 is only 1.1x visible instead of 1.5x visible due to slow GtG).

**42/** **@BlurBusters** ^1740253843404021894

**@NOTimothyLottes** **@phys_ballsocket**

Further improvements can be added (e.g. Vulkan integration, engine integration, etc) to make it more properly native & more universal effects-compatible & easier for game developers. Will be more decadal progress (e.g. next major version number or two of graphics API).

**43/** **@BlurBusters** ^1740254319226540448

Only reason reprojection looks so bad today, is because we're starting from low framerates & reprojecting to strobed (Rift, PSVR, etc). But providing high-triple-digit Hz + sample and hold + starting min framerate ... was absolutely unexpected magical improvement for reprojection that looked better than DLSS3.

**44/** **@BlurBusters** ^1740254916143378742

**@NOTimothyLottes** **@phys_ballsocket**

And such shockingly absurdly simple; Optical Flow less needed when orig frames under 1/100sec apart, due to flicker fusion threshold. Artifacts much more faintly visible.
(A) Test on 240-480Hz+ OLED (CES 2024); and
(B) Input framerate=min 100
(C) Output framerate=display Hz

**45/** **@BlurBusters** ^1740255441480028401

**@NOTimothyLottes** **@phys_ballsocket**

Right Tool For Right Job though. 
BFI still has a place, but this is almost certain to be the ergonomic VR future beyond ten years (~2033 even for standalone headsets at least sometime shortly after that point, due to how revolutionary an improvement it was).

**46/** **@BlurBusters** ^1740256090624029115

**@NOTimothyLottes** **@phys_ballsocket**

We anticipate rich ergonomic-picky parties like Apple will attempt to rapidly escalate refresh rate of Apple Vision Pro to ~500Hz to remove the strobing requirement.  Not quite 1000, but only about 4 times more refresh rate, and roughly equal persistence to original Oculus Rift.

**47/** **@NOTimothyLottes** ^1740259486840066546

**@BlurBusters** **@phys_ballsocket**

Challenge though, it's specialization into a non-general local minima. Beam-racing and friends are post-free content. Post processing doesn't scale to 1000hz brute force, nor does it do parallax reprojection without artifact. Highend content is big-post.

**48/** **@BlurBusters** ^1740260579271663767

**@NOTimothyLottes** **@phys_ballsocket**

Yes, parallax is problem too. That's where Optical Flow can kick in. I even mention in Dev Best Practices; but less important for ever tinier intervals between frametimes than larger intervals. There's a dramatic cliff-falloff of artifacts there. This is a simple brute trick.

**49/** **@NOTimothyLottes** ^1740270919917212106

**@BlurBusters** **@phys_ballsocket**

Reprojection fail cases cannot be fixed by optical flow, because then it's either interpolation (back to the latency problem), or extrapolation (which is worse than reprojection). This doesn't ever converge to artifact-free with good latency and low power.

**50/** **@BlurBusters** ^1740271674929619146

**@NOTimothyLottes** **@phys_ballsocket**

Yes, correct. Optional settings for reprojection to add optional 10ms latency for 100->1000fps to enable improved parallax infill. However, brute is better: P\arallax artifacts of any 10:1 framegen (reprojection or otherwise) do have an apparent visibility cliff effect >100fps.

**51/** **@BlurBusters** ^1740272049816551569

**@NOTimothyLottes** **@phys_ballsocket**

Regardless of how multitiered you framegen it (spatial/temporal combos), the perceptual visibility cliff effect is similar. It's still there, but dramatically less so, when sample and hold + input rate of 100 min.

**52/** **@BlurBusters** ^1740274096091619462

**@NOTimothyLottes** **@phys_ballsocket**

Decision of what rendering compromises to make is astoundingly difficult >100fps. Sometimes it's just simpler to have the GPU/APIs help you fix these issues with brand new multitiered framgen+render workflow. Pick-poison compromises dramatically different 50->100 vs 200->1000fps

**53/** **@BlurBusters** ^1740274795558903910

**@NOTimothyLottes** **@phys_ballsocket**

Multiple sources over last many months tell me that 8:1+ framegen is coming from BOTH team red and team green eventually. Team blue will probably follow closely behind. It may or may not be reprojection, but large-ratio framegen is coming anyway regardless.

**54/** **@NOTimothyLottes** ^1740276763656401374

**@BlurBusters** **@phys_ballsocket**

Games cannot easily render motion vector fields at required frame rate, nor do they offer up re-skinning for existing pixel reprojection. So yeah, next step is bi-directional interpolation, just with more in-between frames. Artifacts will be more clear with less scan-and-hold.

**55/** **@BlurBusters** ^1740277247574200419

**@NOTimothyLottes** **@phys_ballsocket**

Terminology autocorrect: "Less sample and hold" = "more impulsing".
You're correct, impulsed displays show more artifacts.  120fps DLSS3 framegen artifacts definitely appear more if I turn ULMB ON instead of ULMB OFF. You are correct.

**56/** **@NOTimothyLottes** ^1740283362986877370

**@BlurBusters** **@phys_ballsocket**

Been fun, comment on BFI tollerence has been useful, and I get your perspective better than before. As one of the few that might end up having to write said 1000hz frame gen tech, I'd still choose BFI personally. Hope OEMs are aware BFI is ideal for some, not a bandaid.

**57/** **@BlurBusters** ^1740283685503750332

**@NOTimothyLottes** **@phys_ballsocket**

Datapoint: 7 Blur Busters Approved monitors were in the pipeline pre-pandemic. Only 2 made it through (XG270, XG2431). Mfrs don't implement algos correctly; so third-party box-in-middle approaches is a favourite BFI incubator now including future CRT beam sims.

**58/** **@BlurBusters** ^1740283938961326284

**@NOTimothyLottes** **@phys_ballsocket**

The Retrotink 4K "BYOBA" (Bring Your Own BFI Algorithm) is something I am going to iterate in future products, for people who want BFI more advanced than manufacturers want to correctly add to their displays.

**59/** **@BlurBusters** ^1740284481657852363

**@NOTimothyLottes** **@phys_ballsocket**

As displays rocket past 1000Hz this decade, one could technically emulate plasma subfields or DLP temporal dithers, or other retro algorithms. Brute Hz is great for retro display emulation!

**60/** **@NOTimothyLottes** ^1740286674679046244

**@BlurBusters** **@phys_ballsocket**

Maybe soft BFI is immune? but when I do extreme temporal dither with energy preserving maths, even on a calibrated display, the non-linear temporal panel response tends to regrade the image (not energy preserving in output). If that future is to be, linear response needed

**61/** **@BlurBusters** ^1740291757579874450

**@NOTimothyLottes** **@phys_ballsocket**

Linear response is challenging for box-in-middle advanced BFI algorithms, so have to do some workarounds and compensatory end-user gamma curve adjustments for a HDR-boosted CRT beam simulator algorithm.

**62/** **@BlurBusters** ^1740293944884514821

**@NOTimothyLottes** **@phys_ballsocket**

Squarewave BFI is purest (easy for "Blur Busters Law" mathematics) but harshest ergonomically, while fadein/fadeout algorithms, especially rolling scan (non-global), is the most ergonomic but even the sofest BFI is never 100% immune to ergonomic issues (flicker headaches/nausea).

**63/** **@BlurBusters** ^1740294604136554525

The most ergonomic BFI is generally fadein/fadeout rolling scan because it satisfies three important  checkboxes: 
(A) One brightness peak per pixel per Hz is always best motion quality (always); and 
(B) Slow ramp up/down to brightness peak
(C) Constant stream of photons hitting eyes (some part of screen is practically always illuminated).

**64/** **@NOTimothyLottes** ^1740238400962396197

**@BlurBusters** **@phys_ballsocket**

Would need to understand population comfort with respect to refresh rate at given display vs room ambient levels. And hard vs soft BFI, etc. It may be that localized contrast adaptive BFI is actually what you want (BFI tollerence is with respect to image intensity).

**65/** **@BlurBusters** ^1740238767313850572

**@NOTimothyLottes** **@phys_ballsocket**

That helps but doesn't solve 100%. We have 10 years of experience in display ergonomics, being Blur Busters a long-time brand name beacon for display ergonomics people (people who get more motionblur headaches than flicker headaches) so we get massive collateral data as a result;

**66/** **@NOTimothyLottes** ^1740240992257884419

**@BlurBusters** **@phys_ballsocket**

Suspect not everything has been tried yet in the BFI space. Not BFI, but I have a bunch of CRT shaders that are roughly energy preserving and still have quite visible scan emulation. That kind of logic didn't ship in RetroTink4K, so I'd bet not all of us are sharing knowledge

**67/** **@BlurBusters** ^1740241329064714315

**@NOTimothyLottes** **@phys_ballsocket**

I'm working in that space too, it will greatly help low framerate material. We're working on shader-based CRT electron beam simulators as a sequel to Retrotink 4K (which I helped) which has customizable monolithic BFI patterns.
https://www.retrotink.com/post/retrotink-4k-blur-buster-approved

**68/** **@BlurBusters** ^1740241741649735769

Incidentally, playing back a 1000fps high speed video of a CRT to a true 1000Hz display, preserves a CRTs' temporals pretty well (low blur, scanout flicker, soft phosphor fade). Trick is erasing the seams between adjacent refresh cycles, but easy with 480Hz+ OLEDs. Have TestUFO CRT beam simulator prototype using lookup tables sitting on my disk, but it requires 240Hz+ OLEDs to barely look good, and 360Hz+ OLEDs to begin to look like a real BFI replacement. Better to get >10:1 ratios in digital refresh cycles emulating a single analog refresh cycle.

**69/** **@BlurBusters** ^1740242217560617390

CRT beam simulators are not good enough at 4:1 ratios on LCDs, and barely good enough at 6:1 ratios on OLED. Tricky to get gamma-corrected HDR precisely to have the proper shingled overlapped rolling fadebehind BFI, without seams and without tearing artifacts, but I've come up with some solutions for that.

## Related

- Spine: [[archive/threads/NOTimothyLottes/2023-12-26-no-luck-getting-d3dkmtgetscanline-to-work-thus-far]]
