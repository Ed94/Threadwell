---
title: "@CharlieMQV How does this software avoid race conditions with raw disk access when the OS might be writing changes to disk at the same time? Is the search best effort and may miss some matches if you're unlucky?"
type: archive
source: twitter
source_url: "https://x.com/mtrantalainen/status/1957695235326111833"
author: "Mikko Rantalainen"
handle: mtrantalainen
post_id: "1957695235326111833"
date: 2025-08-19
archived: 2026-08-25
draft: false
tags:
  - archive
  - twitter
  - CharlieMQV
description: "@CharlieMQV How does this software avoid race conditions with raw disk access when the OS might be writing changes to disk at the same time? Is the search best effort and may miss some matches if you're unlucky?"
in_reply_to: ""
parent_post_id: "1957552694186418228"
---

## Source

- URL: https://x.com/mtrantalainen/status/1957695235326111833
- Author: Mikko Rantalainen (@mtrantalainen)
- Posted: 2025-08-19 06:44:50

## Branch

**1/** **@mtrantalainen** ^1957695235326111833

**@CharlieMQV**

How does this software avoid race conditions with raw disk access when the OS might be writing changes to disk at the same time? Is the search best effort and may miss some matches if you're unlucky?

**2/** **@CharlieMQV** ^1957768563986481248

**@mtrantalainen**

NTFS does a really good job of making this a minimal problem. Things very rarely move around in the MFT and whenever the purpose of a file record is changed, it has a sequence number that's updated.

**3/** **@CharlieMQV** ^1957769272811278833

If you're not updating according to the USN journal, you might end up using outdated data runs. But this is very rare and all that happens is you might miss a match or get a false positive. However, if you're constantly listening to the USN journal, this is so unlikely that I don't think it's worth considering.

**4/** **@mtrantalainen** ^1957778025300304350

**@CharlieMQV**

Yes, if you blindly accept rare misses or false positives, the task is much much easier.

Maybe you can run the same search a couple of times and see if the results are deterministic if the search is fast enough for that in practice.

**5/** **@CharlieMQV** ^1957779358963073049

The only possible problem is if a file is heavily modified at the exact time when the program is searching specifically the data run that changes (which it rarely does). Even if this ever happens, it is extremely unlikely to matter to the user. As someone who at this point is quite familiar with NTFS, I think this is a near-impossible case, and I'm pretty sure you can never finish and ship software if you optimize for near-impossible cases.

**6/** **@mtrantalainen** ^1957821577468297431

**@CharlieMQV**

I think the documentation should still explicitly point out this risk. As I see it, the only options on Windows are very slow and accurate, or this raw device level access but sometimes inaccurate. Most people will pick the fast option but they should be aware of the risks.

**7/** **@mtrantalainen** ^1957821729058820218

**@CharlieMQV**

Given enough users, even one in million events will happen regularly.

**8/** **@CharlieMQV** ^1957822844684906838

**@mtrantalainen**

I'm trying to tell you my prediction is that it would be rarer than that and even rarer that it impacted the user

## Related

- Spine: [[archive/threads/CharlieMQV/2025-08-18-existing-search-tools-on-windows-suck]]
