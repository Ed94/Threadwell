---
title: "The API is terrible."
type: archive
source: twitter
source_url: "https://x.com/oisyn/status/1958289693314892081"
author: "Sylvester Hesp"
handle: oisyn
post_id: "1958289693314892081"
date: 2025-08-20
archived: 2026-08-25
draft: false
tags:
  - archive
  - twitter
  - CharlieMQV
description: "The API is terrible."
in_reply_to: ""
parent_post_id: "1957552694186418228"
---

## Source

- URL: https://x.com/oisyn/status/1958289693314892081
- Author: Sylvester Hesp (@oisyn)
- Posted: 2025-08-20 22:07:00

## Branch

**1/** **@oisyn** ^1958289693314892081

The API is terrible. Even enumerating the MFT through the API takes longer than doing raw reads *AND* it provides you with less information (IIRC the creation and last modified timestamps are zeroed out in the data structs; the room to store those things is right there as they model the NTFS datastructures exactly, but they actively remove that info and they call the members "reserved".

For incremental game content builds we tracked file changes through the NTFs journal, but we need MFT records to build the file tree. Took about a minute to read the MFT through the API and then for each file do a call to get the timestamp info. Parsing the raw MFT only takes a couple of seconds. It's insane.

I know Everything (that instant file search took by Voidtools) also do their own raw NTFS parsing.

**2/** **@CharlieMQV** ^1958292591427912124

Yes. I first tried FindFirstFile/FindNextFile. Catastrophic. So I tried their more low level file system API. Still catastrophic. Just SLOW for no good reason.

If you just stream the MFT you can index file name at the speed of however fast your drive can read that amount of bytes. 1 million files == 1 second on 1GiB/s read drives (excluding hardware caching). No real excuse for it to take longer than that to build a data structure for instantly finding any of those files.

Everything finds file names instantly, but unfortunately fails severely at searching file contents.

## Related

- Spine: [[archive/threads/CharlieMQV/2025-08-18-existing-search-tools-on-windows-suck]]
