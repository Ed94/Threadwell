---
title: "@Jonathan_Blow What do you mean in a non-findable way anymore ? Is it in a custom path instead of the classic System32 / SysWOW64 ?"
type: archive
source: twitter
source_url: "https://x.com/MattyMSS/status/1906824954542461022"
author: "Matty"
handle: MattyMSS
post_id: "1906824954542461022"
date: 2025-03-31
archived: 2026-08-29
draft: false
tags:
  - archive
  - twitter
  - Jonathan_Blow
description: "@Jonathan_Blow What do you mean in a non-findable way anymore ? Is it in a custom path instead of the classic System32 / SysWOW64 ?"
in_reply_to: ""
parent_post_id: "1906823282915262657"
---

## Source

- URL: https://x.com/MattyMSS/status/1906824954542461022
- Author: Matty (@MattyMSS)
- Posted: 2025-03-31 21:44:30

## Branch

**1/** **@MattyMSS** ^1906824954542461022

**@Jonathan_Blow**

What do you mean in a non-findable way anymore ? Is it in a custom path instead of the classic System32 / SysWOW64 ?

**2/** **@Jonathan_Blow** ^1906825155994853542

**@MattyMSS**

I ran two different DirectX redistributable thingies and dsound.dll is still not installed as a system library anywhere that anyone can find, for some reason.

**3/** **@Jonathan_Blow** ^1906825685630660754

**@MattyMSS**

One of the installers is generating an error, and maybe this is causing everything to abort. I tried deleting most of the cabs and only installing stuff 2009 or later, but this didn't have dsound I guess.

**4/** **@MattyMSS** ^1906826466697806082

**@Jonathan_Blow**

I'm mostly surprised because afaik it's supposed to be bundled with Windows (albeit only the directX 9.0 version). I know that the runtimes overwrite it so it's probably an installer error that either deleted it or edited its permissions while overwriting and it's stuck in limbo

**5/** **@Jonathan_Blow** ^1906828063817785484

**@MattyMSS**

I am running a fresh install of Windows and it just does not seem to be there.

**6/** **@MattyMSS** ^1906829132840718686

**@Jonathan_Blow**

What is this command's output ? It should show you the registration path

reg query HKLM\SOFTWARE\Classes /s /f dsound.dll

**7/** **@Jonathan_Blow** ^1906831143347032225

**@MattyMSS**

Okay you know what, it says it's in system32, and it is. (I goofed and only searched in system).

As for why it can't be found when I run stuff, hmmmm.... maybe it is the thing where the DLL is found but it depends on DLLs that are not found.

**8/** **@MattyMSS** ^1906831674471559485

**@Jonathan_Blow**

Glad you found it ! It could be missing dependecies or that the dll isn't properly registered. Do this and try again to make sure : 

regsvr32 C:\Windows\System32\dsound.dll

Hit me up if it doesn't work

**9/** **@Jonathan_Blow** ^1906833077135200451

**@MattyMSS**

As I thought...

![](https://pbs.twimg.com/media/GnZukyOawAAs3Mf?format=png&name=orig)

**10/** **@MattyMSS** ^1906833384438972512

**@Jonathan_Blow**

Yeah it could be corrupted. You can grab one from another windows computer (or I can send you mine). You could also delete it and hope reinstalling will fix it

**11/** **@Jonathan_Blow** ^1906834221064491335

**@MattyMSS**

I'll try just copying it when I get home, but I suspect it's more like a problem with a dependency. I am just too lazy right now to download the sysinternals dependency viewer thing.

**12/** **@Jonathan_Blow** ^1906835652924297297

**@MattyMSS**

I tried copying it and now I have some access denied bullshit despite the fact that my account is supposed to have administrator permissions. Yay.

I am so ready to dump Windows, it's just not funny.

**13/** **@Jonathan_Blow** ^1906835992772071521

**@MattyMSS**

Maybe "access denied" actually means "file in use" because Windows is stupid. I feel my will to deal with this leaving my body rapidly.

**14/** **@MattyMSS** ^1906836736157851717

**@Jonathan_Blow**

It's a dll, it's supposed to be used by multiple programs at once. Could it be that because you copied it the system perceives you as not the owner ? Try editing the file permissions. (Wait til you see some Windows kernel parts rewrite in rust that will 100% kill our brains soon)

**15/** **@Jonathan_Blow** ^1906839285132825085

I didn't copy it. This is whatever the installer installed or whatever was on the system from initial Windows install last night.

Permissions for the file are grayed out, I can't change anything.

Years ago I would have pursued this but after so many years of fucking bullshit that always gets worse, I am ready to give up and completely bail. I hate this. I am trying to get actual work done. I don't know what Microsoft thinks they are doing.

**16/** **@MattyMSS** ^1906840423806402619

**@Jonathan_Blow**

You might try to use a mount on C through the recovery command line but at some point it's not worth the hassle. I'm not familiar with XAudio2 (heck haven't used DirectSound in a while) but that might be your best bet at the moment. Wish I could've been of more help though :(

## Related

- Spine: [[archive/threads/Jonathan_Blow/2025-03-31-for-years-i-have-used-dsound-dll-to-play-audio-on]]
