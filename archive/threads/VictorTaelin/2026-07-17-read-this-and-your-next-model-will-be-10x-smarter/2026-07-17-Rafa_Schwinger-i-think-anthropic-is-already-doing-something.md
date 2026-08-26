---
title: "@VictorTaelin I think Anthropic is already doing something similar because they are compressing intelligence as much as possible for pretraining."
type: archive
source: twitter
source_url: "https://x.com/Rafa_Schwinger/status/2078114345477603691"
author: "Rafa Schwinger 🇻🇦"
handle: Rafa_Schwinger
post_id: "2078114345477603691"
date: 2026-07-17
archived: 2026-08-25
draft: false
tags:
  - archive
  - twitter
  - VictorTaelin
description: "@VictorTaelin I think Anthropic is already doing something similar because they are compressing intelligence as much as possible for pretraining."
in_reply_to: ""
parent_post_id: "2078110851123286452"
---

## Source

- URL: https://x.com/Rafa_Schwinger/status/2078114345477603691
- Author: Rafa Schwinger 🇻🇦 (@Rafa_Schwinger)
- Posted: 2026-07-17 13:47:24

## Branch

**1/** **@Rafa_Schwinger** ^2078114345477603691

**@VictorTaelin**

I think Anthropic is already doing something similar because they are compressing intelligence as much as possible for pretraining.

**2/** **@VictorTaelin** ^2078115018294341680

**@Rafa_Schwinger**

how so

**3/** **@Rafa_Schwinger** ^2078115738422824982

**@VictorTaelin**

You need minimum descriptions to maximize intelligence density. That implies that your internal data factory needs a model that is about to compress information losslessly or minimally lossy. They could adapt something similar for posttraining

**4/** **@VictorTaelin** ^2078116059035349109

**@Rafa_Schwinger**

I mean why do you think they're training on erasure seriously

**5/** **@Rafa_Schwinger** ^2078120963351187604

Because if you want to maximize intelligence density, let's say pre-training or in thinking traces, you of course need the least amount of tokens that represents the information. Suppose that you want to feed Wikipedia as a dataset to train a LLM. You can probably get 99% of the effective quality by trimming it at 10% of its size. You compress the text and you leave the most important articles a bit longer and the rarest articles shorter. The whole definition of entropy from info theory is about minimum length anyway so anyone working with synthetic data can have a preprocessing layer like this. 

It is more difficult to do that at scale because you need to QA reward hacking, but since GPT was a bit behind specifically in reward hacking despite being good at grind seems to suggest that Anthropic takes this point more seriously. In a way, elegant solutions is basically the same thing as avoiding reward hacking. 

Of course I could be wrong about all of this, but it seems to be pointing in this direction.

**6/** **@VictorTaelin** ^2078123440637194583

**@Rafa_Schwinger**

my point is that I think they're doing that accidentally

when you have 500000 B300, you will be training for erasure indirectly, because it IS needed for capabilities. but you're doing so innefficiently

my point is that minding erasure will 100x their effective FLOPS

**7/** **@Rafa_Schwinger** ^2078125069952315482

No, I think that everyone is relying heavily on synthetic data and internal RLVR pipelines rn and making sure that you have something closer to minimal descriptions would be a important part of this pipeline. So I think that they are aware of the issue even if they perhaps can't do that properly. 

The problem is also a matter of topology. Some operations are global in nature, but the training is still too local and iterative. So sometimes refactoring demands a global operation while adding is of course local. our current training methods. There are way too many physics systems where you would not be able to get to the minimum using naive gradient descent. An RL seems to enhance this issue.

The deeper issue that you're alluding to is that some compressions can't be found just by using a sequence of small local compressions, which is a hard problem. that is physically equivalent to these transitions in memory-shaped alloys. You need to heat it up to cool it down to a different local minimum again.

## Related

- Spine: [[archive/threads/VictorTaelin/2026-07-17-read-this-and-your-next-model-will-be-10x-smarter]]
