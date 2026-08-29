---
title: "@VictorTaelin Ya compress the AST size not the character count.."
type: archive
source: twitter
source_url: "https://x.com/DaleCloudman/status/2078134295768486176"
author: "Dale Cloudman"
handle: DaleCloudman
post_id: "2078134295768486176"
date: 2026-07-17
archived: 2026-08-28
draft: false
tags:
  - archive
  - twitter
  - VictorTaelin
description: "@VictorTaelin Ya compress the AST size not the character count.."
in_reply_to: ""
parent_post_id: "2078110851123286452"
---

## Source

- URL: https://x.com/DaleCloudman/status/2078134295768486176
- Author: Dale Cloudman (@DaleCloudman)
- Posted: 2026-07-17 15:06:40

## Branch

**1/** **@DaleCloudman** ^2078134295768486176

**@VictorTaelin**

Ya compress the AST size not the character count.. 

Not just branches 

Foo(a(1,2))
Bar(a(1,2))

Is worse than

Z = a(1,2)
Foo(z)
Bar(z)

**2/** **@VictorTaelin** ^2078137866752864328

**@DaleCloudman**

no. number of branches.

ast size is not the true measure of complexity because non branching ast nodes can be inferred in linear time

**3/** **@DaleCloudman** ^2078142390586499488

**@VictorTaelin**

Didn’t follow, what it means to ‘infer’ an AST node in this context?

**4/** **@VictorTaelin** ^2078145575774494751

I mean quadratic time *

I just obsreve that any program without branching can be reconstructed in quadratic time given enough I/O pairs. So I believe measuring complexity from number of branches is more accurate

You can't build a complex algorithm without branches so, the more branches you have, the more complex your file / algorithm is. If you remove all branches, it becomes trivial and compressible, even if there are still lots of characters

Example:

foo = λa. a + a

and

foo = λa. a + a + a + a + a

have the same underlying complexity, despite one being larger.

or so I think (:

**5/** **@DaleCloudman** ^2078608651707625503

**@VictorTaelin**

So I'm trying this for Python and there's lot of edge cases... how do I handle calling foreign code, it 'optimized' a max-finding algo by just calling np.max instead of doing the py version lol. and using np.where to avoid ifs...

**6/** **@DaleCloudman** ^2078619365839192104

**@VictorTaelin**

Ok I think it’s more that a function call is not a branch…

## Related

- Spine: [[archive/threads/VictorTaelin/2026-07-17-read-this-and-your-next-model-will-be-10x-smarter]]
