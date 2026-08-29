---
title: "One of the things I probably loathe most about the mentality of OOP that got pushed on the industry is that you need a different file for every object."
type: archive
source: twitter
source_url: "https://x.com/_rygo6/status/1767783595899515341"
author: "rygo6"
handle: _rygo6
post_id: "1767783595899515341"
date: 2024-03-13
archived: 2026-08-29
draft: false
tags:
  - archive
  - twitter
  - _rygo6
description: "One of the things I probably loathe most about the mentality of OOP that got pushed on the industry is that you need a different file for every object."
in_reply_to: ""
---

## Source

- URL: https://x.com/_rygo6/status/1767783595899515341
- Author: rygo6 (@_rygo6)
- Posted: 2024-03-13 05:23:47

## Thread

**1/** **@_rygo6** ^1767783595899515341

One of the things I probably loathe most about the mentality of OOP that got pushed on the industry is that you need a different file for every object.

OOP insinuates a view about the structure of code which is false, that being, code is composed of separate "objects" that send messages to each other. This conjures the image of a bunch of small organisms floating around an open space in a completely unstructured way sending messages to each other. 

When the truth is, code tends to be hierarchal. It has a root entry point, which call methods, which call other methods, forming a tree structure. Code is not a wide-open space of objects sending things everywhere. You can design a system to appear as such and abstract away the underlying hierarchal nature, but then you lose what is actually a good quality. The hierarchal tree structure enables a straighter forward structuring and tracking of lifetimes. In one parent method allocate everything you need, making their lifetimes dependent on the scope of that method. Then that method calls another, which could even go to a runtime loop, but upon exiting that parent method scope, it automatically can release everything in that branch of the hierarchal tree. If you make everything dependent on the scope of methods as they descend this hierarchy, you do end up with fully automatic memory management, never even needing to call 'free' or 'delete'. 

Keeping everything in a single file helps to reinforce this hierarchal structure, as any variable or method which some code relies on must be declared above it in the file. The downward flow of the file is forced to reflect the downward flow of the hierarchy of the program. 

This combined with lifetime and memory management all bound to method scopes creates such a simple and straightforward representation of what exactly is going on in a program. All dependencies must be declared higher up the file, and cleared higher up the file somehow, then as you scroll down everything below is dependent on everything above. Having to click through a dozen files tracing method calls to figure out what some object is dependent on is not an improvement over that. I would rather just scroll up. 

But you lose all of that when every granular chunk of logic, or "object" is put in a different file, when you try to abstract away the fact it is a hierarchy. Then you have to deal with more complex schemes of tracking memory use, and freeing memory. And for what? Because big files were bad? Because somehow an open space of "objects" flying about willy-nilly sending messages is a simpler mental model than a hierarchal tree structure? (It's not) 

I'm wondering was there some more objective reason in the 90's for this? Like were older source control schemes bad at merging large files or something? It seems like a major mistaken path the industry veered down. Or was it just because management wanted to maximally "Parallelize" development thinking it's better if people worked in many different files? Also, a terrible path the industry seemed to go down.

The top of a file should be an entry point into one significant chunk of functionality. Then everything below dependent on everything above. From there use structs, classes, instances, whatever, but leverage the fact it is hierarchal, don't abstract it away.

Branches: [[archive/threads/_rygo6/2024-03-13-one-of-the-things-i-probably-loathe-most-about/2024-03-13-Samueltates-ive-definitely-overindulged-in-oops-delights-to]]
