---
title: "@CharlieMQV Parses the raw NTFS?  Installs a IO driver or the win32 apis have a mode?  I just have not heard of apps other than drivers looking at \"raw\" NTFS."
type: archive
source: twitter
source_url: "https://x.com/fluiddesign201/status/1957611955298181153"
author: "Your B⏱️ss 🇺🇸⚾💻🥩"
handle: fluiddesign201
post_id: "1957611955298181153"
date: 2025-08-19
archived: 2026-08-25
draft: false
tags:
  - archive
  - twitter
  - CharlieMQV
description: "@CharlieMQV Parses the raw NTFS?  Installs a IO driver or the win32 apis have a mode?  I just have not heard of apps other than drivers looking at \"raw\" NTFS."
in_reply_to: ""
parent_post_id: "1957552694186418228"
---

## Source

- URL: https://x.com/fluiddesign201/status/1957611955298181153
- Author: Your B⏱️ss 🇺🇸⚾💻🥩 (@fluiddesign201)
- Posted: 2025-08-19 01:13:55

## Branch

**1/** **@fluiddesign201** ^1957611955298181153

**@CharlieMQV**

Parses the raw NTFS?  Installs a IO driver or the win32 apis have a mode?  I just have not heard of apps other than drivers looking at "raw" NTFS.

**2/** **@CharlieMQV** ^1957745032284299281

**@fluiddesign201**

Windows API lets you CreateFile on a volume label to get a HANDLE that lets you read the entire partition from start to end. You do need admin rights though.

**3/** **@pthread_mutex_t** ^1957813670622253492

**@CharlieMQV** **@fluiddesign201**

You then need to backtranslate the VCN to filename and LCN. Something reciprocal to FSCTL_GET_RETRIEVAL_POINTERS.

**4/** **@CharlieMQV** ^1957814538952204492

**@pthread_mutex_t** **@fluiddesign201**

The only windows functions I use is CreateFile and ReadFile. Anything from the NT library is bad. I just parse the filesystem from scratch

**5/** **@pthread_mutex_t** ^1957815283705414089

**@CharlieMQV** **@fluiddesign201**

How do you backtranslate the offset on the volume to the filename and offset within a file?

**6/** **@CharlieMQV** ^1957816703175311679

**@pthread_mutex_t** **@fluiddesign201**

Back translate from what? And what do you mean by the offset on the volume? Offset to the file record?

**7/** **@pthread_mutex_t** ^1957819093316157885

**@CharlieMQV** **@fluiddesign201**

You read the volume cluster by cluster. You find that at offset 0x1'2345'6789 on the volume you have the string you are looking for. Now I'd want to present this info to the end user in the form "file c:\foo\bar.baz, line 123, col 45". How do you do that? It is not an easy thing.

**8/** **@CharlieMQV** ^1957902160059875771

The first sector is the "boot sector" where you can find the offset into the MFT which contains all the 1KiB file records. Each file record has a reference number to it's parent (which include an index i.e. offset from first file record). To produce the full path string you follow the parent references. Each file record (if it's representing a proper file), will contain a FILE_NAME attribute which stores the file name in the file record.

This is a simplification, but roughly how it looks.

There isn't a lot of proper documentation and what exists is rough (especially when you get into windows-specific stuff). But I figured most of it out from this website: https://flatcap.github.io/linux-ntfs/ntfs/index.html

## Related

- Spine: [[archive/threads/CharlieMQV/2025-08-18-existing-search-tools-on-windows-suck]]
